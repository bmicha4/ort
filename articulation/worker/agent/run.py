from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sqlite3
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import httpx
import trafilatura
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()\n\nROOT = Path(os.getenv("ARTICULATION_REPO", "/workspace/repo"))
RESEARCH_DIR = ROOT / os.getenv("RESEARCH_DIR", "articulation/docs/research")
DB_PATH = Path(os.getenv("STATE_DB", "/workspace/state/worker.db"))
BRANCH = os.getenv("ARTICULATION_BRANCH", "articulation-mvp")
MAX_SOURCES = int(os.getenv("MAX_SOURCES_PER_RUN", "12"))
MAX_CHARS = int(os.getenv("MAX_SOURCE_CHARS", "12000"))


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(DB_PATH)
    c.execute("""CREATE TABLE IF NOT EXISTS runs(
        id INTEGER PRIMARY KEY, job TEXT, started_at TEXT, finished_at TEXT,
        status TEXT, output_path TEXT, error TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS sources(
        id INTEGER PRIMARY KEY, url TEXT UNIQUE, title TEXT, domain TEXT,
        retrieved_at TEXT, content_hash TEXT, source_type TEXT)""")
    c.commit()
    return c


def git(*args: str) -> str:
    p = subprocess.run(["git", *args], cwd=ROOT, text=True,
                        capture_output=True, check=True)
    return p.stdout.strip()


def ensure_branch() -> None:
    branch = git("branch", "--show-current")
    if branch != BRANCH:
        raise RuntimeError(f"Refusing to run on branch {branch!r}; expected {BRANCH!r}")


def search_brave(query: str) -> list[dict]:
    key = os.getenv("BRAVE_SEARCH_API_KEY")
    if not key:
        raise RuntimeError("BRAVE_SEARCH_API_KEY is required for SEARCH_PROVIDER=brave")
    r = httpx.get(
        "https://api.search.brave.com/res/v1/web/search",
        params={"q": query, "count": 10},
        headers={"Accept": "application/json", "X-Subscription-Token": key},
        timeout=30,
    )
    r.raise_for_status()
    return [
        {"title": x.get("title", ""), "url": x.get("url", ""),
         "description": x.get("description", "")}
        for x in r.json().get("web", {}).get("results", [])
        if x.get("url")
    ]


def search(query: str) -> list[dict]:
    provider = os.getenv("SEARCH_PROVIDER", "brave")
    if provider == "brave":
        return search_brave(query)
    raise RuntimeError(f"Unsupported SEARCH_PROVIDER={provider!r}")


def fetch(url: str) -> dict:
    r = httpx.get(url, timeout=30, follow_redirects=True,
                  headers={"User-Agent": "ArticulationResearchWorker/0.1"})
    r.raise_for_status()
    text = trafilatura.extract(r.text, include_links=True, include_tables=True) or ""
    text = re.sub(r"\s+", " ", text).strip()
    return {
        "url": str(r.url),
        "title": "",
        "text": text[:MAX_CHARS],
        "status": r.status_code,
    }


def llm() -> OpenAI:
    return OpenAI(
        base_url=os.environ["LLM_BASE_URL"],
        api_key=os.getenv("LLM_API_KEY", "local"),
    )


def complete(client: OpenAI, prompt: str) -> str:
    r = client.chat.completions.create(
        model=os.environ["LLM_MODEL"],
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
    )
    return r.choices[0].message.content or ""


def plan(client: OpenAI, job: str) -> list[str]:
    prompt = f"""You are the Articulation research planner.
Job: {job}

Generate 8 precise web-search queries. The research must cover official
documentation plus real-world community evidence. Include relevant queries
for Reddit, GitHub issues/discussions, Hugging Face and public developer
reports where appropriate. Focus on current information and do not invent
facts.

Return JSON only:
{{"queries":["..."]}}
"""
    raw = complete(client, prompt)
    match = re.search(r"\{.*\}", raw, re.S)
    if not match:
        raise RuntimeError(f"Planner returned non-JSON: {raw[:500]}")
    data = json.loads(match.group(0))
    return [q for q in data["queries"] if isinstance(q, str)][:8]


def source_type(url: str) -> str:
    host = urlparse(url).netloc.lower()
    if "reddit.com" in host:
        return "reddit"
    if "github.com" in host:
        return "github"
    if "huggingface.co" in host:
        return "huggingface"
    return "web"


def save_source(c: sqlite3.Connection, item: dict, content: dict) -> None:
    digest = hashlib.sha256(content["text"].encode()).hexdigest()
    c.execute(
        """INSERT INTO sources(url,title,domain,retrieved_at,content_hash,source_type)
           VALUES(?,?,?,?,?,?)
           ON CONFLICT(url) DO UPDATE SET retrieved_at=excluded.retrieved_at,
           content_hash=excluded.content_hash""",
        (item["url"], item.get("title", ""), urlparse(item["url"]).netloc,
         now(), digest, source_type(item["url"])),
    )
    c.commit()


def synthesize(client: OpenAI, job: str, evidence: list[dict]) -> str:
    bundle = json.dumps(evidence, ensure_ascii=False)
    prompt = f"""You are the senior research analyst for the Articulation project.

Research job:
{job}

Use ONLY the supplied evidence. Do not invent benchmarks, prices, support,
licenses, capabilities or dates. Distinguish official documentation from
community reports. If sources conflict, explicitly say so. Treat Reddit,
GitHub issues and other community reports as evidence of reported experience,
not universal facts.

Produce a Markdown report with:
# Executive summary
# Findings
# Official evidence
# Community evidence
# Contradictions and uncertainty
# Implications for Articulation
# Recommended validation tests
# Sources

Every factual statement that depends on a source must include its URL inline.

Evidence:
{bundle}
"""
    return complete(client, prompt)


def run_job(job: str) -> Path:
    load_dotenv()
    ensure_branch()
    c = db()
    started = now()
    run_id = c.execute(
        "INSERT INTO runs(job,started_at,status) VALUES(?,?,?)",
        (job, started, "running"),
    ).lastrowid
    c.commit()

    try:
        client = llm()
        queries = plan(client, job)

        results = []
        seen = set()
        for q in queries:
            for item in search(q):
                url = item["url"]
                if url in seen:
                    continue
                seen.add(url)
                if len(results) >= MAX_SOURCES:
                    break
                try:
                    content = fetch(url)
                    if len(content["text"]) < 200:
                        continue
                    save_source(c, item, content)
                    results.append({
                        "query": q,
                        "title": item.get("title", ""),
                        "url": url,
                        "source_type": source_type(url),
                        "content": content["text"],
                    })
                except Exception as exc:
                    results.append({
                        "query": q, "url": url,
                        "error": f"fetch failed: {type(exc).__name__}: {exc}",
                    })

        report = synthesize(client, job, results)
        RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        safe = re.sub(r"[^a-z0-9]+", "-", job.lower()).strip("-")
        path = RESEARCH_DIR / f"worker-{safe}-{stamp}.md"
        path.write_text(report + "\n", encoding="utf-8")

        if os.getenv("AUTO_COMMIT", "false").lower() == "true":
            git("add", str(path.relative_to(ROOT)))
            git("commit", "-m", f"research: {job}")

        c.execute(
            "UPDATE runs SET finished_at=?,status=?,output_path=? WHERE id=?",
            (now(), "completed", str(path), run_id),
        )
        c.commit()
        return path
    except Exception as exc:
        c.execute(
            "UPDATE runs SET finished_at=?,status=?,error=? WHERE id=?",
            (now(), "failed", f"{type(exc).__name__}: {exc}", run_id),
        )
        c.commit()
        raise


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--job", required=True)
    args = parser.parse_args()
    print(run_job(args.job))


if __name__ == "__main__":
    main()
