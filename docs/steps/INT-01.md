# INT-01 — Media integration readiness
Planned: 2026-11-28. Implemented: 2026-11-28. Recorded: 2026-11-28.
Scope: unify image/audio/video configuration checks and expose missing server settings without credentials.
Dependencies: existing D1/R2 and editorial identity. Acceptance: missing keys, disabled generation, zero budget and missing storage block provider actions; no secrets returned.
Files: worker/integrations.js, worker/media.js, worker/workspace.js, worker/workspace-ui.js, tests/integrations.test.mjs.
Status: implemented; local checks recorded in release record. Provider activation remains pending credentials.
Rollback: revert this step; no data migration. Existing uploaded/released media remain intact.
