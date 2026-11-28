# INT-02 — Hosted captioned video rendering
Planned: 2026-11-28. Record created before implementation: 2026-11-28.
Dependencies: INT-01; official Shotstack Edit API render/status, rich-text and destination contracts.
Scope: submit bounded, source-linked captioned MP4s; persist render ID; explicit status refresh imports validated MP4 into private storage for editorial review. No automatic publication or paid retry.
Acceptance: replayed request keys do not submit twice; daily cap includes all providers; output fetching is restricted to provider output hosts and matching render IDs; redirects and oversized/non-MP4 results rejected; failures stay private; story-version and approval rules preserved.
Limits: captioned explainer with no soundtrack; image and narration are separate jobs. Provider activation needs a server-side key. Provider temporary output is external to the private app; default permanent Shotstack hosting must be excluded.
Files: worker/hosted-video.js, worker/media.js, worker/media-ui.js, tests/hosted-video.test.mjs, tests/media.test.mjs, docs/MEDIA_INTEGRATIONS.md.
Implemented: 2026-11-28. Recorded: 2026-11-28.
Status: implemented and locally validated (93 website checks passed; all provider requests mocked). Browser verified missing setup and disabled paid controls. Live provider activation pending. Rollback: revert adapter/UI; existing jobs/assets preserved. Closing an interrupted job does not cancel provider billing.
