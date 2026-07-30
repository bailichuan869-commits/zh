# UI Source Rules

These rules apply to Vue application source under `frontend/src/`. Read `frontend/AGENTS.md` and the repository-root `AGENTS.md` first.

## Product Intent

This is a Chinese CPA knowledge-workbench browser. The interface should feel calm, precise, and reliable for reading regulations, searching knowledge assets, and comparing source-backed results. Use concise Chinese operational copy and preserve established terminology.

## UI Rules

1. Use Ant Design Vue as the primary visual and interaction system. Prefer its layout, form, navigation, table, feedback, and overlay components before custom implementations.
2. Each page has one clear primary action. Keep secondary actions visually quieter and avoid decorative UI that obscures reading or scanning.
3. Make loading, empty, error, disabled, and successful states explicit. Present request failures through appropriate Ant Design feedback and preserve a usable retry path where relevant.
4. Keep responsive behavior intentional: multi-column areas may collapse to one column, but text, controls, and reading content must remain legible and reachable on narrow screens.
5. Use semantic headings, visible labels, keyboard-reachable controls, and sufficient visual contrast. Do not communicate state through color alone.
6. Separate page views, reusable components, composables, services, and styles by responsibility. When a feature grows beyond a single component, colocate its parts in a clearly named feature folder.
7. Keep API calls out of templates. Use `services/api.ts` or a focused composable, and render untrusted Markdown only through the existing sanitization path.
8. Do not hand-edit router configuration, global styles, or shared shell components for a page-local need without first checking their cross-page impact.

## Delivery Checks

- Reopen changed Chinese text and confirm UTF-8 without BOM.
- Confirm the affected route handles loading, no-result, error, and populated data appropriately.
- Check desktop and mobile layouts without overlapping controls, clipped text, or horizontal overflow.
- Run the checks required by `frontend/AGENTS.md` for the change scope.
