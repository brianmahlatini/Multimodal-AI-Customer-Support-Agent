# Architecture

The platform separates multimodal intake, agent orchestration, deterministic support policy checks, storage, analytics, and the support console.

## Components

- FastAPI exposes authentication, cases, tickets, and analytics endpoints.
- LangGraph-compatible nodes pass a shared case state through specialist support agents.
- PostgreSQL stores customers, conversations, messages, artifacts, support cases, tickets, and audit events.
- Redis is the production target for conversation memory and workflow cache.
- S3-compatible storage holds uploaded audio, images, screenshots, and documents.
- React provides the operational support console.

## Extension Points

- Replace `MockOpenAIService` with live OpenAI Responses and transcription calls.
- Replace local object storage with AWS S3 or MinIO.
- Replace seeded account data with CRM and billing APIs.
- Replace local knowledge retrieval with pgvector or managed vector search.
