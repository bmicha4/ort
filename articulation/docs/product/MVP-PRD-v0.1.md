# Articulation MVP PRD v0.1

Status: Draft for implementation
Platform: Android first, iOS-ready architecture
Primary languages: Hebrew, Russian, English
Scope: First 10 minutes and the foundation of the ongoing training loop

## 1. Product objective

Articulation is a communication-training product built around realistic AI conversations.

The user practices speaking with photorealistic AI characters in realistic situations. The system observes communication behavior, identifies recurring patterns, provides focused coaching, and uses those observations to generate progressively more challenging future conversations.

The product is not primarily a chatbot, language translator, or static roleplay library.

The core loop is:

Install -> short onboarding -> first conversation -> observe -> light coaching -> replay -> update communication profile -> generate next challenge.

The first-session success criterion is behavioral: after completing the first conversation and replay, the user should understand what they can improve and have a clear reason to start another conversation.

## 2. Product principles

1. Conversation first
   The user should spend most of the experience speaking, not configuring.

2. Realistic before aggressive
   Early conversations should feel comfortable and natural. Pressure increases only as the system gathers evidence about the user's behavior.

3. Learn the user, not only the scenario
   A scenario ends, but communication patterns persist across conversations.

4. Training should be actionable
   Feedback should identify observable behavior and provide a concrete next attempt.

5. Separate language skill from communication behavior
   The system may track language-specific vocabulary and fluency while also tracking cross-language communication patterns.

6. Provider-independent AI architecture
   LLM, STT, TTS, and avatar providers must be replaceable behind interfaces.

7. Android first, not Android-only
   The client architecture must not prevent a later iOS client.

## 3. Target user

Initial target: adults who want to improve real-world spoken communication.

Examples:
- Explaining technical or professional topics
- Answering questions directly
- Responding under pressure
- Handling disagreement
- Finding words quickly
- Being concise
- Communicating with managers, teammates, partners, friends, or other people

The MVP does not target children.

## 4. First-launch experience

The first launch must be short.

### Step 1: Welcome

Explain the product in one or two screens.

Core message:

"Practice real conversations before they happen."

Avoid a long questionnaire.

### Step 2: Language

Allow the user to choose a primary conversation language:
- Hebrew
- Russian
- English

The user may change the language later.

The system should preserve language-specific learning data.

### Step 3: Two default characters

Two characters are created automatically.

Default contexts:
- Work character
- Personal character

The exact names, appearance, voice, and personality are implementation decisions during UX design.

The user should not need to create a character before their first conversation.

The user can customize, replace, or add characters later.

### Step 4: Start first conversation

The user selects one of the two characters and starts immediately.

No complex scenario builder is required.

The first conversation should establish a natural baseline rather than aggressively test the user.

## 5. AI character

The MVP character experience is:

- Photorealistic appearance
- Real-time facial animation
- Generated voice
- Lip synchronization
- Natural expressions
- AI-controlled gestures where supported
- Context-aware reactions
- Follow-up questions
- Ability to disagree or challenge the user when appropriate

The character should feel closer to a video conversation than an animated chatbot.

The visual layer must remain separate from the conversation engine.

Conceptual interface:

AICharacter
- appearance
- voice
- personality
- communication style
- relationship
- emotional state
- conversation behavior

## 6. First conversation behavior

The first conversation should prioritize observation.

The AI should:
- Ask natural questions
- Follow the user's answers
- Remember the immediate conversation context
- React appropriately
- Avoid unnecessary interruptions
- Avoid constant coaching
- Detect potential communication patterns

The system should collect evidence without making the user feel evaluated every few seconds.

Examples of observations:
- Response latency
- Excessive context before answering
- Difficulty finding a word
- Repetition
- Unclear structure
- Overly long answers
- Failure to answer the actual question
- Strong performance under no pressure
- Performance degradation when challenged

Observations are signals, not conclusions. The system should avoid treating a single occurrence as a stable weakness.

## 7. Adaptive difficulty

Difficulty starts low.

The system gradually becomes more demanding as sufficient evidence accumulates.

Possible progression:

Level 0: Natural conversation
- No pressure
- Normal turn-taking

Level 1: Mild challenge
- Follow-up questions
- Topic changes
- Light disagreement

Level 2: Communication pressure
- Interruptions
- Requests for concise answers
- Unexpected follow-ups
- Time constraints

Level 3: Realistic difficult conversation
- Persistent disagreement
- Competing priorities
- Emotional reactions
- Strong interruptions
- Ambiguous questions
- Pressure to answer quickly

The user does not need to see numerical difficulty levels.

Difficulty should be selected by the training engine based on the user's observed behavior and recent performance.

## 8. Communication Profile

The Communication Profile is the core persistent model.

It contains evidence-backed observations such as:

### Communication behaviors
- Directness
- Conciseness
- Structure
- Response speed
- Handling interruptions
- Handling disagreement
- Ability to recover after losing a point
- Ability to adapt communication style

### Language-specific data
For each language:
- Vocabulary known
- Vocabulary being learned
- Frequently forgotten words
- Frequently misused words
- Domain vocabulary
- Retrieval difficulty
- Recent improvements

### Pressure response
- Baseline performance
- Performance under time pressure
- Performance after interruption
- Performance during disagreement

### Confidence and evidence
Every learned pattern should retain evidence and recency so that one unusual conversation does not permanently redefine the profile.

## 9. Coaching

Coaching should be light during the first session.

After the conversation, explain:

1. What happened
2. What pattern was observed
3. Why it matters
4. What to try differently

Example:

"You understood the question, but you gave the background before answering it."

Then:

"Next time, answer the question first. Add context only if they ask for it."

Avoid reducing the entire conversation to a single score.

## 10. Replay

The user should replay one important moment from the first conversation.

Replay means the system recreates a similar situation and gives the user another attempt.

Example:

Original:
The character asks a direct question.
The user gives a long explanation before answering.

Replay:
The character asks a similar direct question.
The user is encouraged to answer directly.

The replay should preserve the training objective while allowing the conversation to remain dynamic.

## 11. Next Challenge

After replay, Articulation generates one personalized next challenge.

Example:

"Your next challenge"

"Your teammate asks why the deployment is blocked. Answer in 15 seconds. They already know the background."

The challenge should be based on observed behavior from the first conversation and replay.

It should not require the user to manually configure training parameters.

## 12. Vocabulary

Vocabulary training is embedded into communication rather than being a separate flashcard-first experience.

The system can detect:
- Words the user searched for mentally
- Words replaced with simpler words
- Words repeatedly forgotten
- Words used incorrectly
- Useful new vocabulary

When appropriate, vocabulary should be reintroduced naturally in later conversations.

Vocabulary tracking is language-specific.

## 13. Training objectives

The MVP supports these training objectives:

- Faster responses
- Vocabulary retrieval
- Clarity
- Conciseness
- Handling pressure
- Handling difficult conversations

A conversation may combine multiple objectives.

The user should not need to manually select all objectives. The system can derive them from the training context and Communication Profile.

## 14. Two conversation modes

### Natural mode

The AI behaves naturally and minimizes coaching interruptions.

### Training mode

The AI may intervene when the training objective requires it.

Examples:
- "Try that again in one sentence."
- "Answer the question first."
- "You're losing the main point. Try again."
- Vocabulary hint when appropriate.

The MVP can begin with natural mode plus limited training interventions.

## 15. People and characters

MVP supports:

### Default characters
Two automatically created characters:
- Work
- Personal

### Custom people
Later in the MVP lifecycle, the user can create a person based on:
- Name
- Relationship
- Role
- Communication style
- Relevant context

The system must not assume that a generated character accurately represents a real person.

Imported communications and personal data require explicit user control and permissions.

## 16. Data and privacy principles

The architecture must treat conversation data as sensitive personal data.

Requirements:
- Explicit user consent for imported communications
- Clear separation of user data and system-generated character data
- Ability to delete user-generated conversation data
- Minimize retained raw audio where possible
- Avoid sending private communication data to third-party providers unless the user has knowingly enabled that provider
- Provider abstraction must allow private/local processing where feasible

Privacy implementation details are part of the technical architecture phase.

## 17. AI provider architecture

All major AI capabilities must be behind provider interfaces.

### LLM
- Local/private provider
- Cloud provider

### STT
- Local/private provider
- Cloud provider

### TTS
- Local/private provider
- Cloud provider

### Avatar
- External real-time avatar provider
- Future alternative provider
- Future local renderer

The MVP may use external providers where local hardware cannot provide sufficient quality or latency.

The application must not couple business logic directly to a specific provider SDK.

## 18. Backend architecture direction

Use a monorepo with modular components.

Do not introduce microservices as an MVP requirement.

Initial logical modules:
- API
- Conversation engine
- Character engine
- Coaching engine
- Vocabulary engine
- Communication Profile
- AI provider adapters
- Persistence

These can initially run as one deployable backend and be extracted later when justified by scale, resource isolation, or operational requirements.

## 19. Platform

### MVP
Android.

### Architecture requirement
Keep business logic and APIs platform-independent so an iOS client can be added later.

The mobile client should use a cross-platform strategy where practical, while allowing platform-specific integrations for audio, permissions, notifications, and performance.

## 20. Home experience after first session

The home screen becomes a feed of recommended conversations.

Example card:

"Your next conversation"

"Explain a project delay without over-explaining."

Other cards may eventually include:
- Continue practicing
- Repeat a recent challenge
- Practice a weak vocabulary area
- Prepare for a difficult conversation
- Practice with a specific person

The recommendation engine should eventually generate these cards automatically from the Communication Profile.

## 21. MVP success criteria

The MVP should be considered successful if users can:

1. Install and start quickly.
2. Enter a conversation without complex configuration.
3. Have a convincing voice conversation with an AI character.
4. Complete a natural first conversation.
5. Receive useful, specific coaching.
6. Replay an identified weakness.
7. Receive a personalized next challenge.
8. Return for another conversation.

The primary product metric for the early MVP should be repeat practice, not the number of screens or AI features.

## 22. Explicitly out of scope for MVP v0.1

- Kids mode
- Full Gmail integration
- WhatsApp integration
- Slack integration
- Teams integration
- Large-scale contact synchronization
- Full meeting ingestion
- iOS release
- Microservices architecture
- Self-hosted photorealistic avatar as a requirement
- Complex gamification
- Public social features
- Marketplace for characters
- Advanced analytics dashboard
- Fully autonomous long-term relationship simulation

These may be added after the core training loop is validated.

## 23. Technical infrastructure direction

The existing two NVIDIA Jetson systems can be used for private development and AI workloads.

Initial intended roles:
- Jetson 1: build/CI/integration workloads
- Jetson 2: local AI experimentation and inference

The infrastructure must be reproducible through code and containers rather than relying on manually configured machines.

Cloud services may still be required for capabilities where the Jetsons cannot provide adequate latency, quality, or platform support.

## 24. Competitive lessons incorporated

Research into comparable products indicates that several individual components already exist in the market:
- AI conversation practice
- Adaptive language tutoring
- Persistent AI characters
- Persona-driven roleplay
- Communication simulation
- Photorealistic real-time avatars

Articulation's intended differentiation is the combination of these capabilities around a persistent Communication Profile and an adaptive training loop.

The product should learn from repeated behavior rather than treating each roleplay as an isolated exercise.

## 25. First implementation milestone

The first engineering milestone is a vertical slice, not a collection of disconnected screens.

Target flow:

Android app
-> onboarding
-> two default characters
-> conversation session
-> microphone input
-> STT
-> conversation engine
-> LLM response
-> TTS
-> avatar response
-> transcript
-> session analysis
-> coaching
-> replay
-> Communication Profile update
-> next challenge

The first vertical slice may use mocked or provider-backed components where necessary, but every interface should match the final architecture.

## 26. Open decisions for architecture phase

The following should be resolved before substantial implementation:

1. Flutter vs React Native vs native Android with a shared backend.
2. Backend language/framework.
3. Database.
4. Authentication.
5. Real-time transport.
6. STT provider and fallback.
7. TTS provider and fallback.
8. Photorealistic avatar provider for the first vertical slice.
9. Local LLM model and Jetson deployment strategy.
10. Conversation state model.
11. Communication Profile schema.
12. Privacy and data retention model.
13. CI/CD and Android signing strategy.
14. Observability.
15. Automated evaluation of conversation quality.

## 27. Definition of done for PRD v0.1

The PRD is complete enough to begin architecture work when:
- First-session behavior is unambiguous.
- The adaptive training loop is defined.
- The Communication Profile is a first-class product concept.
- Provider boundaries are explicit.
- MVP exclusions are explicit.
- The first vertical slice is defined.
- Remaining technology choices are listed as architecture decisions rather than silently assumed.
