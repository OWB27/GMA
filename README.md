# GMA

GMA is the Game Modeling Agent for GRS. It helps produce reviewable game tag and weight data for the existing GRS recommendation system.

GMA is not a player-facing recommendation app. It is an upstream modeling tool: given a Steam game name and Steam URL, it collects Steam source data, retrieves the fixed GRS modeling context, asks an LLM for a structured draft, validates that draft, saves it for human review, and exports approved tags in a GRS-compatible format.

## Current Backend Shape

The backend currently includes:

- FastAPI API routes
- PostgreSQL persistence through SQLModel
- Alembic migrations
- Steam source collection
- GRS modeling rule-pack loading
- LangGraph workflow orchestration
- LangChain structured modeling chain
- business validation for modeling drafts
- human review and GRS export endpoints

The frontend starts later. Stage 8.5 cleans the backend architecture before Stage 9 frontend work.

## Main API Surface

```text
GET  /health
POST /modeling-jobs/run
POST /modeling-jobs/{job_id}/review
POST /modeling-jobs/{job_id}/export
```

`POST /modeling-jobs/run` is the main modeling entry point. It accepts:

```json
{
  "game_name": "Hades",
  "steam_url": "https://store.steampowered.com/app/1145360/Hades/"
}
```

`POST /modeling-jobs/{job_id}/review` accepts only `approved` or `rejected` as human review decisions.

`POST /modeling-jobs/{job_id}/export` returns a flat GRS-compatible payload:

```json
[
  {
    "game_code": "hades",
    "tag_code": "combat",
    "weight": 4
  }
]
```

## Backend Architecture

See [docs/backend-architecture.md](docs/backend-architecture.md) for the responsibility boundaries between routes, services, graph nodes, chains, validators, repositories, and modeling context.

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

Run database migrations:

```bash
cd backend
uv run alembic upgrade head
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

```text
ENVIRONMENT=local
DATABASE_URL=postgresql+psycopg://gma:gma@localhost:5432/gma
LLM_PROVIDER=openai_compatible
LLM_MODEL=gpt-4.1-mini
LLM_API_KEY=
LLM_BASE_URL=
LLM_TEMPERATURE=0
LLM_STRUCTURED_OUTPUT_METHOD=json_schema
```

For DeepSeek or another OpenAI-compatible provider, use the provider base URL and prefer `LLM_STRUCTURED_OUTPUT_METHOD=json_mode`.

## Project Boundaries

- GMA only accepts `game_name` and `steam_url`.
- GMA only models Steam games.
- GMA only selects from the existing fixed GRS tag set.
- GMA does not create new tags.
- GMA does not write directly into the GRS production database.
- GMA export is review-gated.
- Tavily is not part of the current source collection path.
