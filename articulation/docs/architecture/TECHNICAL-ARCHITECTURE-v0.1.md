# Articulation Technical Architecture v0.1

Date: 2026-10-01
Status: Proposed implementation baseline

## 1. Architecture decision summary

Recommended baseline:

- Mobile: Flutter, Android first, iOS-ready
- Backend: Python + FastAPI
- Primary database: PostgreSQL
- Real-time conversation transport: WebSocket
- Async/background work: Redis + worker process
- API style: REST for normal application operations, WebSocket for live sessions
- LLM: provider abstraction, cloud model initially with local Jetson provider
- STT: streaming provider abstraction
- TTS: streaming provider abstraction
- Avatar: external real-time avatar provider behind an adapter
- Deployment: Docker
- Jetson 1: CI/build/integration runner
- Jetson 2: local AI inference and experimentation
- Repository: existing bmicha4/ort, branch articulation-mvp, with Articulation isolated under articulation/
- Architecture style: modular monolith initially, not microservices

## 2. Why Flutter

Flutter is the proposed mobile framework because the product is fundamentally a real-time UI and audio experience and must eventually support Android and iOS.

The MVP remains Android-first.

Platform-specific code should be isolated behind small interfaces for:
- microphone/audio
- permissions
- notifications
- secure storage
- background behavior
- device-specific performance features

The application should keep business logic independent of Android APIs.

## 3. Why Python + FastAPI

The backend is AI-heavy and will integrate with:
- LLM SDKs
- speech processing
- model serving
- embeddings
- evaluation
- async workloads

Python keeps the AI and backend stack in one ecosystem.

FastAPI provides:
- typed request/response models
- async support
- WebSocket support
- straightforward testing
- OpenAPI documentation

The backend should be structured by domain rather than by framework layer.

## 4. Backend modules

Initial modules:

backend/
  api/
  auth/
  users/
  characters/
  conversations/
  training/
  profile/
  vocabulary/
  providers/
  persistence/

These are modules in one deployable application.

Do not create separate network services unless there is a demonstrated need.

## 5. Live conversation architecture

The live session is the critical path.

Conceptually:

Mobile
  |
  | WebSocket
  v
Conversation Gateway
  |
  +--> Session State
  |
  +--> Streaming STT
  |
  +--> Conversation Engine
  |       |
  |       +--> Character State
  |       +--> Training Objective
  |       +--> Communication Profile
  |       +--> LLM Provider
  |
  +--> Streaming TTS
  |
  +--> Avatar Provider
  |
  +--> Transcript/Event Store

The backend owns conversation state.

The mobile client should not contain the authoritative conversation state.

## 6. Streaming and latency

Latency is a first-class product requirement.

Do not implement the conversation as:

record entire answer -> upload -> wait -> generate -> download -> play.

Instead use streaming wherever provider capabilities permit:

user speech
  -> streaming STT
  -> partial transcript
  -> end-of-turn detection
  -> LLM streaming
  -> TTS streaming
  -> avatar/audio output

Measure each stage separately.

Initial engineering targets should be treated as targets to validate experimentally, not promises:
- Speech-to-first-response audio: target <= 1.5s
- End-of-user-speech to final response: target <= 3s for normal turns
- STT partial transcript: target < 300ms after speech begins
- UI must remain responsive during all processing

If a provider cannot meet the target consistently, the architecture must support switching providers.

## 7. Interruption handling

The system must support barge-in.

When the user starts speaking while the character is speaking:

1. Mobile detects user speech.
2. Current character audio playback is stopped or faded.
3. Active TTS generation is cancelled where supported.
4. Avatar playback is interrupted.
5. New user speech becomes the active turn.
6. Conversation state records the interruption.

This is necessary for realistic conversation and for later training around interruptions.

## 8. Conversation engine

The conversation engine should not be a generic chat completion wrapper.

It owns:

- Session state
- Turn state
- Character state
- Scenario constraints
- Training objectives
- Difficulty
- Interruption events
- Recent topics
- Repetition prevention
- Conversation recovery
- Provider orchestration

The LLM is a reasoning/generation component inside the engine, not the engine itself.

## 9. Character model

Character state should include:

- identity
- appearance reference
- voice reference
- personality
- communication style
- relationship
- current emotional state
- scenario role
- behavioral constraints

Character behavior must be configurable independently of visual appearance.

## 10. Communication Profile

The Communication Profile is a persistent domain model.

It should not be a single LLM-generated paragraph.

Use structured observations.

Conceptual model:

CommunicationProfile
  |
  +-- CrossLanguageBehavior
  |     +-- directness
  |     +-- conciseness
  |     +-- structure
  |     +-- response_speed
  |     +-- interruption_recovery
  |     +-- disagreement_handling
  |
  +-- LanguageProfile[language]
  |     +-- vocabulary
  |     +-- retrieval
  |     +-- fluency_signals
  |
  +-- PressureProfile
  |     +-- baseline
  |     +-- interruption
  |     +-- time_pressure
  |     +-- disagreement
  |
  +-- Evidence
        +-- observation
        +-- confidence
        +-- count
        +-- timestamp
        +-- context

A weakness should require repeated evidence.

## 11. Training engine

The training engine selects what to practice next.

Inputs:
- Communication Profile
- recent sessions
- previous challenges
- language
- character
- scenario
- recent failures
- recent successes

Output:
- training objective
- scenario constraints
- difficulty
- character behavior
- vocabulary targets
- success criteria

Example:

Objective:
Direct answers

Constraints:
Manager already knows background

Pressure:
15 seconds

Character behavior:
Interrupt if user begins unnecessary background

Success:
Answer question directly before adding context

## 12. Coaching engine

The coaching engine converts session evidence into:

- observations
- explanations
- replay targets
- future training signals

Do not produce a single opaque score as the primary result.

Every important coaching observation should be traceable to conversation evidence.

## 13. Repetition prevention

Store recent:
- prompts
- scenarios
- topics
- vocabulary targets
- character actions
- coaching observations

The training engine should avoid repeating the same content unless repetition is intentional reinforcement.

## 14. Provider abstraction

Use explicit interfaces.

LLMProvider:
- stream_response()
- cancel()
- health()

STTProvider:
- start_stream()
- send_audio()
- finalize()
- cancel()

TTSProvider:
- stream_audio()
- cancel()

AvatarProvider:
- create_session()
- send_audio_or_text()
- interrupt()
- close()

Provider adapters must live outside the domain logic.

## 15. Avatar strategy

For the first vertical slice, use a proven external real-time avatar provider.

Do not make local photorealistic rendering a blocker.

The application should support:

AvatarProvider
  -> external provider

Later:

AvatarProvider
  -> provider B
  -> local renderer

If avatar service fails:
voice conversation continues where possible.

## 16. Jetson architecture

### Jetson 1

Purpose:
- CI runner
- Docker builds
- Android builds
- integration tests
- backend test environment

The machine should be configured from Git and reproducible.

### Jetson 2

Purpose:
- local LLM experimentation
- embeddings
- local STT/TTS experimentation
- model serving

The exact model depends on available Jetson GPU memory and measured latency.

Do not select the model solely by benchmark size.

## 17. Local AI strategy

The product must work with a cloud provider during initial development if that gives better conversation quality.

At the same time, define provider interfaces so the following can be tested independently:

Cloud LLM
Local LLM on Jetson

The first local model should be selected based on:
- conversational quality
- Hebrew quality
- Russian quality
- English quality
- time-to-first-token
- tokens/sec
- context length
- VRAM requirements

## 18. Persistence

PostgreSQL stores durable application data.

Initial entities:

User
Character
ConversationSession
ConversationTurn
TranscriptSegment
TrainingObjective
CommunicationObservation
CommunicationProfile
LanguageProfile
VocabularyItem
Challenge
ProviderConfiguration

Raw audio should not automatically become permanent application data.

## 19. Redis/background work

Redis is for transient coordination and background work, not the source of truth.

Use it for:
- job queues
- temporary session state where appropriate
- rate limiting
- provider coordination

Do not put the permanent Communication Profile in Redis.

## 20. Security

Initial requirements:
- authentication tokens stored securely on device
- TLS for all network traffic
- secrets only in server-side configuration
- provider credentials never shipped in the mobile application
- least-privilege service credentials
- explicit consent for imported personal communications
- auditability for sensitive operations
- configurable data retention

## 21. Observability

Instrument the live path.

Metrics:
- STT latency
- LLM time-to-first-token
- LLM total latency
- TTS time-to-first-audio
- avatar connection latency
- full turn latency
- interruption rate
- provider errors
- conversation abandonment
- replay completion
- next-challenge completion

Structured logs should include a session ID but avoid raw sensitive conversation content by default.

## 22. Testing strategy

### Unit tests
- Conversation state transitions
- Profile updates
- Training selection
- repetition prevention
- provider adapters

### Integration tests
- STT -> conversation -> TTS
- provider failures
- interruption
- session recovery

### End-to-end tests
- onboarding
- character selection
- live conversation
- replay
- next challenge

### AI evaluation
Maintain deterministic scenario fixtures and evaluate:
- instruction adherence
- character consistency
- training objective adherence
- repetition
- unsafe/invalid behavior
- coaching correctness

AI quality tests should be versioned like software tests.

## 23. Initial repository structure

articulation/
  docs/
    product/
    research/
    architecture/
    decisions/
  apps/
    mobile/
  backend/
  ai/
  infrastructure/
    docker/
    jetson/
  tests/

The backend remains one deployable application initially.

## 24. Implementation sequence

Phase 1:
- Repository skeleton
- Flutter application
- FastAPI application
- PostgreSQL
- Authentication skeleton
- CI

Phase 2:
- WebSocket conversation session
- STT provider
- LLM provider
- TTS provider
- transcript events

Phase 3:
- Character model
- first scenario
- conversation engine
- avatar provider

Phase 4:
- session analysis
- Communication Profile
- coaching
- replay
- next challenge

Phase 5:
- Jetson local provider
- provider switching
- latency optimization
- reliability testing

## 25. Architecture decision records to create next

ADR-001: Flutter
ADR-002: FastAPI/Python
ADR-003: PostgreSQL
ADR-004: WebSocket live sessions
ADR-005: Modular monolith
ADR-006: Provider abstraction
ADR-007: External avatar for MVP
ADR-008: Jetson local AI strategy

## 26. Important non-decisions

The following should not be prematurely locked:
- exact LLM model
- exact avatar vendor
- exact STT vendor
- exact TTS vendor
- exact local model

These require current provider research and hardware benchmarks before implementation.

## 27. Architecture success criterion

The architecture is successful if we can replace an LLM, STT, TTS, or avatar provider without changing the core conversation/training domain.

The first vertical slice should prove that property while delivering an actual end-to-end spoken conversation.
