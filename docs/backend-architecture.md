# Backend Architecture

This document explains the current GMA backend shape before frontend work begins.

## Core Flow

```text
POST /modeling-jobs/run
  -> ModelingRunService
    -> LangGraph modeling workflow
      -> collect_sources
      -> retrieve_grs_context
      -> model_game_tags
      -> validate_result
      -> finish
    -> persist workflow outputs
    -> set job status

POST /modeling-jobs/{job_id}/review
  -> ModelingReviewService
    -> save approved or rejected human review result

POST /modeling-jobs/{job_id}/export
  -> ModelingReviewService
    -> require approved review
    -> return flat GRS-compatible game tag payload
```

## Responsibility Boundaries

### API Routes

Routes translate HTTP requests into application service calls and translate service results into responses. They should not contain workflow logic, database logic, LLM prompts, Steam parsing, or validation rules.

### Modeling Run Service

The modeling run service is an application use-case service. It creates a modeling job, runs the LangGraph workflow, saves source bundles and modeling drafts, updates job status, and records workflow events.

It is intentionally outside the graph. Graph nodes represent workflow steps; the modeling run service owns the larger business operation around the graph.

### LangGraph Workflow

The workflow owns state transitions and routing. It decides which node runs next after modeling and validation.
It does not decide whether a successful draft needs human review; every successful modeling run is persisted as a job that waits for review.

Current routing:

```text
model_game_tags
  failed -> finish
  modeled -> validate_result

validate_result
  -> finish
```

### Graph Nodes

Nodes are small adapters between graph state and focused backend units. A node should call one service, chain, or validator, then return state updates.

### Chains

Chains own LLM prompts and structured output. The modeling chain receives a source bundle and retrieved GRS context, then returns a Pydantic-validated modeling draft.

### Source Collection Services

Source collection uses Steam only in the current path.

- Steam store service extracts official descriptions, genres, categories, and popular user tags.
- Steam review service extracts English review score summaries and a small set of useful review snippets.
- Source collection service combines those into one source bundle.

### GRS Context Services

GRS context services load and lightly validate the JSON rule pack in `modeling_context/rules`. This gives the modeling chain the fixed tag definitions, weight scale, combination rules, and examples.

### Modeling Validation Services

The validator checks whether an LLM draft is legal and reviewable for GMA/GRS. Pydantic checks shape and field ranges; the validator checks business rules such as allowed tags, duplicates, tag count, low confidence, and soft conflicts.

### Review Services

Review services handle the human-in-the-loop boundary. Review submission accepts only `approved` or `rejected`. Export is separate and only works for approved results.

The export payload is a flat list:

```json
[
  {
    "game_code": "baldurs_gate_3",
    "tag_code": "story_rich",
    "weight": 5
  }
]
```

`game_code` is derived from the Steam URL slug when possible, with a slugified game-name fallback.

### Repositories

Repositories own database reads and writes. They should not decide workflow status, validation policy, LLM behavior, or export rules.

## Human Review Boundary

AI output is always a draft. The reviewed result is the boundary between GMA's AI-assisted modeling and GRS-compatible final data.

GMA does not write directly into GRS production tables. It exports a review-gated payload that a future GRS importer can consume.
