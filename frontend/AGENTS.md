# Frontend Rules

These rules apply to all work under `frontend/`. Read the repository-root `AGENTS.md` first. For application source changes under `src/`, also read `src/AGENTS.md`.

## Stack and Boundaries

- Use Vue 3, Vite, TypeScript, and Ant Design Vue. Do not introduce React, another UI library, JavaScript components, JSX, or TSX.
- Keep frontend code in `src/`; `dist/` is a generated static release artifact and must not be hand-edited.
- Read `package.json`, `vite.config.ts`, and `README.md` before changing build, dependency, environment, or API-proxy behavior.
- Use UTF-8 without BOM. Follow the root rules for Chinese copy and make scoped patches only.

## Implementation Rules

1. Vue components use `<script setup lang="ts">` and typed props, emits, and service responses where practical.
2. Prefer feature-oriented placement. Keep independent visual areas as components; put reusable state in composables and API access in services.
3. Keep `App.vue` limited to application composition and top-level coordination. Do not move page or feature logic into it.
4. Use Ant Design Vue for interaction controls and feedback. Custom CSS is for layout, spacing, information hierarchy, and necessary visual adjustments, not replacement widgets.
5. Use the `@` source alias and the shared API service. Do not duplicate API base URLs, request wrappers, or response types in views.
6. Treat `VITE_*` variables as public browser configuration. Never add credentials, personal paths, or server-side secrets to frontend environment files.
7. Do not automatically restart frontend or backend processes. Start them only when requested or needed for runtime verification.

## Verification

Run relevant checks from `frontend/`:

```powershell
npm run test
npm run build
```

For runtime verification, use `npm run dev`; it binds to `127.0.0.1:5173` and proxies `/api` to the FastAPI service on port `8765`. Verify the edited view at desktop and mobile widths, including loading, empty, error, and successful-data states.
