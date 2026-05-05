# GMA

GMA is the Game Modeling Agent for GRS. It produces reviewable game tag and weight modeling drafts for the existing GRS tag system.

## Current Stage

Stage 1 builds the backend foundation only:

- FastAPI app skeleton
- centralized settings
- PostgreSQL connection setup
- local PostgreSQL through Docker Compose
- first health-check test

It does not include LangGraph, Tavily, LangChain, database models, or frontend code yet.

## Local Backend Setup

```bash
cd backend
uv sync --dev
copy .env.example .env
```

Start local PostgreSQL from the repository root:

```bash
docker compose up -d postgres
```

Run the backend:

```bash
cd backend
uv run uvicorn app.main:app --reload
```

Run tests:

```bash
cd backend
uv run pytest
```

## Environment Variables

The backend reads configuration from environment variables or `backend/.env`.

- `ENVIRONMENT`: local, test, staging, or production
- `DATABASE_URL`: PostgreSQL connection string
- `OPENAI_API_KEY`: reserved for later LangChain/OpenAI stages
- `TAVILY_API_KEY`: reserved for later Tavily integration
