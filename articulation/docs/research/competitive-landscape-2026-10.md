# Articulation Competitive Research

Date: 2026-10-01

## Executive summary

The market already validates several pieces of Articulation:

- AI voice roleplay for language learning
- Real-time AI characters and avatars
- Difficult-conversation rehearsal
- Adaptive feedback and personalized practice
- Replay and repeated attempts
- Custom scenarios and personas

The closest product found is BetterSelf. It already combines voice-based AI avatars, real-life scenarios, unpredictable responses, hints, difficulty, and post-session feedback.

Articulation should therefore not differentiate by being another generic AI roleplay app. The intended differentiation is a persistent communication-training system that learns how the user communicates across conversations, languages, and recurring real-world relationships, then generates the next training challenge from observed weaknesses.

## Competitor observations

### BetterSelf

Closest conceptual competitor.

Observed capabilities:
- Voice-based AI conversation practice
- AI avatars
- 12 life categories and hundreds of situations
- Custom scenario generation
- Personality selection
- Difficulty adjustment
- Hints while stuck
- Post-session feedback
- Progress tracking
- Guided journeys
- Daily challenges
- Android and iOS availability claimed on its site

Useful ideas:
- Very simple entry point: choose a scenario and start talking
- Real conversations should be unpredictable rather than scripted
- Hints should be available during the conversation
- Feedback should cover communication dimensions, not only language correctness
- Repetition should be a first-class workflow

Gap for Articulation:
- Articulation should model persistent relationships and communication patterns, not just scenarios and personalities.
- Articulation should learn recurring weaknesses and automatically choose future exercises.
- Language should be a shared dimension of the communication profile rather than the entire product identity.

### ELSA Speak

Strong reference for language-learning mechanics.

Observed capabilities:
- AI roleplay for real-world scenarios
- Personalized learning paths
- Real-time feedback
- Workplace, interview, dating, meeting, and presentation scenarios
- Custom scenarios
- Vocabulary and pronunciation training
- Progress tracking
- Interactive avatars

Useful ideas:
- Combine conversation with immediate actionable feedback
- Extract vocabulary from actual conversations
- Reuse mistakes and weak vocabulary in later exercises
- Allow custom scenarios without requiring users to build complex configurations

Gap for Articulation:
- Broader communication training than English-language learning
- Persistent relationship simulation
- Training communication behavior such as concision, response speed, handling pressure, disagreement, and clarification

### Speak

Strong reference for adaptive voice-learning architecture.

Observed capabilities:
- Real-time voice roleplays
- Proficiency graph that tracks language knowledge
- Dynamic vocabulary and sentence-pattern adaptation
- Objectives inside roleplays
- Context-sensitive hints
- Custom lessons generated from goals, topics, mistakes, and interests
- Personalized review based on recurring errors
- Retry/correction loops

Useful ideas:
- Maintain an explicit skill/knowledge state behind the scenes
- Generate future practice from observed mistakes
- Use a Learn -> Practice -> Apply loop where appropriate
- Keep the user speaking instead of turning the product into a text exercise

Important architecture lesson:
The conversation engine and learning engine should be separate. The conversation should feel natural while a hidden training state tracks objectives, weaknesses, vocabulary, and progression.

### Praktika

Strong reference for persistent AI tutor relationships and avatar presentation.

Observed capabilities:
- Named AI tutors
- Context-aware tutor relationship
- Real-time feedback
- Pronunciation, grammar, vocabulary, and pace feedback
- Free Talk experience intended to feel like conversation with a friend

Useful ideas:
- Give characters continuity and recognizable identity
- Make feedback subtle enough not to destroy conversational flow
- Treat the character as a recurring interaction partner rather than a disposable chatbot

### Ovation

Strong reference for professional communication simulation.

Observed capabilities:
- Realistic AI avatars
- Presentations, interviews, roleplay, and difficult conversations
- Custom personas
- Avatar personality, mood, language, tone, role, and pushback controls
- Scenario modifiers controlling avatar behavior
- Custom evaluation factors
- Detailed post-session feedback
- Repeat practice
- Desktop and VR

Useful ideas:
- Separate character persona from scenario behavior
- Make pressure and pushback configurable internally
- Define explicit evaluation factors such as clarity, structure, empathy, relevance, and engagement
- Provide a concrete next attempt instead of only a report

### Real-time avatar infrastructure

HeyGen LiveAvatar is a relevant technical reference for the visual layer.

Observed capabilities:
- Real-time interactive photorealistic avatars
- Streaming video sessions
- Natural lip sync, expressions, and gestures
- API integration
- Ability to connect the avatar to an external LLM

Architecture implication:
Keep the avatar layer behind a provider interface. Do not make the conversation engine depend directly on a specific avatar vendor.

## Articulation differentiation

The product should be built around this model:

User
-> Communication Profile
-> Relationship Models
-> Conversation
-> Behavioral Analysis
-> Skill/Vocabulary Updates
-> Next Challenge

### Communication Profile

Tracks communication capabilities across languages:
- response latency
- concision
- clarity
- vocabulary retrieval
- explanation quality
- handling disagreement
- handling interruptions
- asking questions
- emotional communication
- confidence indicators
- language-specific vocabulary and fluency

### Relationship Model

A recurring person has:
- role
- relationship
- communication style
- known topics
- interaction history
- recurring friction points
- preferred response style
- current context

This is the strongest product-level distinction from generic scenario roleplay.

### Adaptive pressure

Do not expose traditional levels.

Start with natural conversation.

As the system obtains evidence that the user can handle the current interaction, gradually introduce:
- faster follow-ups
- interruptions
- disagreement
- unexpected questions
- topic changes
- requests for shorter answers
- deliberate misunderstandings
- emotional reactions
- time pressure

The system should increase pressure based on observed performance.

### Replay

Every important exercise should support:
1. Original attempt
2. Feedback
3. Targeted retry
4. Slightly different conversation
5. Updated profile

The goal is behavioral learning, not just scoring.

## MVP implications

Keep the first MVP focused on:

- Android
- Two default characters
- One short onboarding flow
- Voice-first conversation
- Photorealistic avatar provider abstraction
- One or two training objectives per session
- Adaptive pressure
- Lightweight hints
- Post-session coaching
- Retry/replay
- Personal communication profile
- Basic vocabulary extraction
- Session history

Do not attempt all integrations or a full social graph yet.

## Key product hypothesis

The strongest hypothesis to test is:

> Users will return because the system knows how they communicate and makes the next conversation specifically useful, rather than because it offers a large library of AI scenarios.

If this hypothesis is correct, the persistent profile and adaptive challenge generator become the core product moat.

## Sources

- BetterSelf: https://betterselfai.app/
- ELSA Speak: https://elsaspeak.com/en/
- Speak: https://www.speak.com/
- Praktika: https://praktika.ai/
- Ovation: https://www.ovationvr.com/
- HeyGen LiveAvatar: https://www.heygen.com/
