#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/bmicha4/ort.git}"
REPO_DIR="${REPO_DIR:-$HOME/src/ort}"
BRANCH="${BRANCH:-articulation-mvp}"
WORKER_DIR="$REPO_DIR/articulation/worker"

if [ ! -d "$REPO_DIR/.git" ]; then
  mkdir -p "$(dirname "$REPO_DIR")"
  git clone --branch "$BRANCH" "$REPO_URL" "$REPO_DIR"
else
  git -C "$REPO_DIR" fetch origin "$BRANCH"
  git -C "$REPO_DIR" checkout "$BRANCH"
  git -C "$REPO_DIR" pull --ff-only origin "$BRANCH"
fi

python3 -m venv "$WORKER_DIR/.venv"
"$WORKER_DIR/.venv/bin/python" -m pip install --upgrade pip
"$WORKER_DIR/.venv/bin/pip" install -r "$WORKER_DIR/requirements.txt"

mkdir -p /opt/articulation/state

echo
echo "Articulation worker synced."
echo "Repository: $REPO_DIR"
echo "Branch:     $(git -C "$REPO_DIR" branch --show-current)"
echo
echo "Next:"
echo "  cp $WORKER_DIR/config/worker.env.example /etc/articulation/worker.env"
echo "  edit /etc/articulation/worker.env"
echo "  $WORKER_DIR/.venv/bin/python -m agent.run --job ai-stack-research"
