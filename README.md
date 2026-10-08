# Flash

Personal AI Copilot for WhatsApp.

## Current architecture

WhatsApp Cloud API -> FastAPI webhook -> persistence -> AgentRuntime -> tools/memory -> PostgreSQL

PostgreSQL -> persistent scheduler worker -> WhatsApp notification

## Included

- FastAPI application and health endpoint
- PostgreSQL persistence for users, messages and memories
- Persistent tasks/reminders
- Tool registry with READ/WRITE/DESTRUCTIVE/SENSITIVE categories
- WhatsApp webhook verification and text ingestion
- Webhook idempotency using WhatsApp message IDs
- WhatsApp Cloud API text client
- Separate scheduler worker
- Docker Compose for API, worker, PostgreSQL and Redis
- pytest foundation

## Development

Copy .env.example to .env, configure credentials, then run:

docker compose up --build

API health: GET /health

## Roadmap

1. Connect the LLM provider and structured tool calling.
2. Add confirmation policies for write/destructive actions.
3. Add recurring tasks and robust job delivery state.
4. Add calendar integration.
5. Add web search.
6. Add audio transcription.
7. Add email and document tools.
8. Add migrations, observability, rate limits and security hardening.