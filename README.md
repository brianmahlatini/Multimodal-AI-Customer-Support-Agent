# Multimodal AI Customer Support Agent

Multimodal AI Customer Support Agent is a production-style support automation platform for repetitive customer calls, emails, chats, uploaded documents, and screenshots. It transcribes voice messages, classifies intent and sentiment, retrieves customer context, checks account information, creates tickets, recommends resolutions, and escalates complex cases to human agents.

The application is built as four containerized services:

- `backend`: FastAPI API, LangGraph-style support workflow, PostgreSQL persistence, Redis-ready conversation memory, OpenAI-ready multimodal provider abstraction, ticketing, account lookup, audit logs, and human handover policy.
- `frontend`: React and Vite support console for case triage, conversation review, uploaded artifact inspection, recommended resolutions, analytics, and escalation tracking.
- `postgres`: PostgreSQL database for customers, conversations, messages, artifacts, support cases, tickets, and audit events.
- `redis`: Conversation memory and workflow cache layer for production deployment.

## Highlights

- Multimodal intake for text, voice recordings, screenshots, and uploaded documents.
- Speech-to-text abstraction with mock mode and OpenAI transcription model configuration.
- Intent and sentiment detection for support prioritization.
- LangGraph-compatible workflow for intake, transcription, classification, account lookup, retrieval, resolution recommendation, ticket creation, and human handover.
- Customer authentication with JWT-ready settings and demo login flow.
- Conversation memory service with Redis-ready boundary and deterministic local fallback.
- Tool calling boundaries for account lookup, knowledge retrieval, ticket creation, and escalation.
- Human handover policy for angry sentiment, high severity, billing disputes, account risk, and low-confidence resolutions.
- Conversation analytics for volume, sentiment, intent mix, escalation rate, and SLA risk.
- S3-compatible artifact storage boundary with local object-store fallback.
- Dockerized backend, frontend, PostgreSQL, Redis, and MinIO-ready configuration.

## Screenshots

Add screenshots to `docs/screenshots/` after running the app:

- Support operations dashboard
- Multimodal case intake form
- Conversation timeline
- Intent and sentiment analysis
- Resolution recommendation panel
- Human handover queue
- Conversation analytics

## Tech Stack

| Layer | Technology |
| --- | --- |
| Frontend | React, Vite, TypeScript, CSS |
| Backend | FastAPI, Uvicorn, Pydantic |
| Agent Workflow | LangGraph-compatible orchestration |
| Multimodal AI | OpenAI-ready Responses and transcription provider boundary |
| Speech-to-Text | OpenAI transcription-ready service with mock fallback |
| Database | PostgreSQL, SQLAlchemy |
| Memory and Cache | Redis-ready service boundary |
| Object Storage | AWS S3-compatible storage, local fallback, MinIO-ready Docker config |
| Runtime | Docker, Docker Compose |
| Auth | JWT-ready authentication settings and demo customer auth |

## System Flow

1. A customer or support agent submits text, a voice recording, screenshots, documents, and account metadata.
2. The Intake Agent normalizes channel, files, customer identity, and message content.
3. The Transcription Agent converts voice attachments into text when audio is present.
4. The Understanding Agent detects intent, urgency, sentiment, and support category.
5. The Account Agent checks customer account information through a tool boundary.
6. The Retrieval Agent pulls relevant policy, billing, troubleshooting, or onboarding knowledge.
7. The Resolution Agent recommends a response and next best action.
8. The Ticket Agent creates or updates a support ticket with full context.
9. The Handover Agent escalates difficult or risky cases to a human support queue.
10. Analytics and audit events are persisted for operational reporting.

## Project Structure

```text
backend/
  app/
    agents/
      graph.py                 # Multi-agent support workflow orchestration
      nodes.py                 # Intake, transcription, intent, retrieval, ticket, handover nodes
      state.py                 # Shared workflow state contract
    api/
      routes/
        analytics.py           # Conversation and escalation metrics
        auth.py                # Demo authentication endpoint
        cases.py               # Multimodal case intake and case retrieval
        health.py              # Health endpoint
        tickets.py             # Ticket listing and updates
    core/
      config.py                # Environment-driven settings
      security.py              # JWT-ready token helpers
    data/
      demo_customers.json      # Seed customer account data
      knowledge_base.json      # Support policy and troubleshooting knowledge
    db/
      models.py                # SQLAlchemy models
      session.py               # Engine, session, and database bootstrap
    schemas/
      auth.py
      case.py
      ticket.py
    services/
      account_service.py       # Account lookup tool boundary
      analytics_service.py     # Support analytics aggregation
      audit_service.py         # Audit event logging
      intent_service.py        # Intent and sentiment classification
      memory_service.py        # Conversation memory boundary
      object_storage.py        # S3/local artifact storage
      openai_service.py        # OpenAI multimodal provider abstraction
      ticket_service.py        # Ticket creation and status updates
    main.py                    # FastAPI app setup
  tests/
    test_intent_service.py
  Dockerfile
  requirements.txt

frontend/
  src/
    components/
      CaseComposer.tsx
      Dashboard.tsx
      TicketQueue.tsx
    lib/
      api.ts
    App.tsx
    main.tsx
    styles.css
  Dockerfile
  package.json
  vite.config.ts

infra/
  docker-compose.yml
docker-compose.yml
scripts/
  generate_demo_data.py
docs/
  architecture.md
```

## Configuration

Create `.env` from `.env.example` for local configuration.

```env
APP_NAME=Multimodal AI Customer Support Agent
ENVIRONMENT=development
DATABASE_URL=postgresql+psycopg://support:support_password@postgres:5432/support_agent
REDIS_URL=redis://redis:6379/0
CORS_ALLOW_ORIGINS=http://localhost:5173
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
OPENAI_TRANSCRIPTION_MODEL=gpt-4o-mini-transcribe
LLM_PROVIDER=mock
JWT_SECRET=change-me
AWS_ACCESS_KEY_ID=minio
AWS_SECRET_ACCESS_KEY=minio_password
S3_BUCKET=support-artifacts
S3_ENDPOINT_URL=http://minio:9000
LOCAL_OBJECT_STORE=data/local_s3
```

Optional frontend environment:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Do not commit real `.env` files. The repository ignores local secrets, virtual environments, node modules, uploaded files, generated transcripts, local object storage, and build artifacts.

## Run With Docker

```bash
cp .env.example .env
docker compose up --build
```

Open:

- Frontend console: `http://localhost:5173`
- Backend health check: `http://localhost:8000/health`
- API docs: `http://localhost:8000/docs`

## Run Locally

### Backend

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## API Reference

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Backend health check |
| `POST` | `/auth/demo-login` | Create a demo access token |
| `POST` | `/cases` | Create a multimodal support case |
| `GET` | `/cases` | List support cases |
| `GET` | `/cases/{case_id}` | Get one support case |
| `GET` | `/tickets` | List support tickets |
| `PATCH` | `/tickets/{ticket_id}` | Update ticket status or owner |
| `GET` | `/analytics/summary` | Conversation and escalation analytics |

Example case request:

```bash
curl -X POST http://localhost:8000/cases \
  -H "Content-Type: application/json" \
  -d "{\"customer_id\":\"cus_1001\",\"channel\":\"chat\",\"message\":\"I was charged twice and need help today\",\"attachments\":[]}"
```

## Agent Decision Policy

The agent recommends resolutions automatically, but it escalates to a human agent when any of these are true:

- Sentiment is strongly negative.
- Intent is billing dispute, cancellation, fraud, security, or legal complaint.
- Account status is suspended, delinquent, or under review.
- The recommended resolution confidence is low.
- The customer explicitly asks for a human.

All escalated cases include customer context, detected intent, sentiment, conversation summary, artifacts, recommended response, and audit trail.

## Demo Scenarios

The seeded scenarios cover realistic customer support work:

- Duplicate billing complaint with negative sentiment.
- Password reset request from an authenticated account.
- Screenshot-based checkout failure.
- Uploaded invoice question.
- Voice-message refund request.
- Subscription cancellation with human handover.
- Shipping delay complaint with ticket creation.

## Security Notes

- Never commit real customer data, API keys, S3 credentials, or production JWT secrets.
- Treat uploaded documents, screenshots, and transcripts as sensitive customer data.
- Use least-privilege service accounts for object storage, database, and support APIs.
- Require human approval for refunds, cancellations, legal complaints, fraud, and account security changes.
- Persist audit events for every automated recommendation and handover decision.
- Use short-lived tokens and role-based access control before production use.

## Implemented Capabilities

- Clean FastAPI backend with typed schemas and SQLAlchemy persistence.
- LangGraph-compatible multimodal support workflow.
- Mock OpenAI provider with OpenAI-ready model and transcription configuration.
- Deterministic intent, sentiment, and urgency detection.
- Customer account lookup tool boundary.
- Knowledge retrieval from seeded support policies.
- Ticket creation and human handover policy.
- Conversation memory service boundary.
- S3-compatible artifact storage abstraction with local fallback.
- React support console with case composer, analytics, and ticket queue.
- Docker Compose for PostgreSQL, Redis, backend, and frontend.
- Backend smoke test for intent and sentiment detection.

## Future Improvements

- Connect the OpenAI Responses API for live multimodal reasoning.
- Connect OpenAI audio transcription for real voice recordings.
- Add authenticated customer portal and support-agent RBAC.
- Add direct integrations for Zendesk, Salesforce Service Cloud, HubSpot, and Intercom.
- Add MinIO service profile for local S3-compatible object storage.
- Add streaming voice support with realtime transcription.
- Add OpenTelemetry traces for agent nodes, tool calls, and escalation decisions.
- Add CI workflows for backend tests, frontend builds, and Docker image checks.
