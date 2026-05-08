# GMA Frontend Notes

This frontend is intentionally organized around the current GMA learning stages.

## State Boundary

- TanStack Query owns server request state:
  - run modeling job mutation
  - submit human review mutation
  - export GRS payload mutation
- React local state owns temporary UI state:
  - create job form
  - current result page data (`runResult`)
  - active result tab
  - human review tag drafts
  - reviewer notes
  - local pre-submit validation errors

`runResult` is intentionally kept in React state for now because it represents the currently displayed modeling result, not just a reusable server cache entry.

## Directory Shape

```txt
src/components/ui
```

Reusable shadcn-style primitive components.

```txt
src/components/modeling/create
```

Create modeling job UI.

```txt
src/components/modeling/result
```

Modeling result display UI, including Steam evidence, AI tags, tabs, and page background.

```txt
src/components/modeling/review
```

Human review draft editing, review submission, and GRS export actions.

```txt
src/hooks
```

TanStack Query hooks. Hooks wrap API functions and should not contain page-specific UI logic.

```txt
src/types/api
```

Backend request/response DTO types.

```txt
src/types/frontend
```

Frontend-only local state types.
