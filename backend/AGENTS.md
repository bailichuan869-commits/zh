# Backend Rules

These rules apply to all work under `backend/`. Read the repository-root `AGENTS.md` first.

## Service Contract

`backend/` is the read-only FastAPI API for the CPA-ZH knowledge base. It may read `knowledge-base/CPA-ZH/` source assets and generated indexes, but it must not mutate raw materials, wiki pages, manifests, source registries, caches, or search indexes.

## Architecture Rules

- Keep route handlers in `app/api/v1/routers/`, request and response models in `app/schemas/`, application behavior in `app/services/`, filesystem/configuration safeguards in `app/core/`, and database access in `app/repositories/`.
- Keep routers thin: validate HTTP input, call a service, and return a typed result. Do not place filesystem traversal, SQL, or content-parsing logic directly in a route handler.
- Add or change API shapes through Pydantic models. Maintain stable JSON field names for the Vue client unless the related frontend is changed and verified in the same task.
- Preserve the local-only API design. Do not relax allowed origins, hosts, CORS methods, or file access controls without explicit user approval.
- Resolve all requested files through the existing safe path utilities. Reject traversal and avoid exposing arbitrary workspace files.
- Use UTF-8 text reads through the shared helpers. Treat missing, malformed, or stale knowledge-base artifacts as handled API errors, not server tracebacks.
- Keep SQLite connections short-lived and closed. Do not write to the search index from request handling.

## Validation

Run focused Python tests for changed behavior. For shared service, routing, validation, or path-safety changes, run:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"
```

When runtime verification is required, start the service locally and inspect the affected endpoint:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8765
```

Confirm API documentation remains available at `/api/docs` and that no endpoint writes into knowledge-base assets.
