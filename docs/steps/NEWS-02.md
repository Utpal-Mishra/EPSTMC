# NEWS-02 — Regional news desk

Planned and recorded: 25 November 2026 (Europe/Dublin). Actual implementation: 25 November 2026. Status: IMPLEMENTED / VALIDATED / DEPLOYED v8.

Scope and acceptance: see STEP_TRACEABILITY.md. Dependencies: private v7 website; NEWS-02 depends on NEWS-01 and DESIGN-01; REL-09 depends on all three.

Evidence and implementation: pending. Per-step implementation commit retains the step ID.

Recovery: revert the bounded code step; preserve story history and editorial gates. New ingestion storage is additive. No schedule or audience change. Provider activation, publication and exhaustive coverage are not implied.

## Implementation — 25 November 2026

Status: IMPLEMENTED / 82 website and 54 Python tests passed locally; Worker build passed. Integrates the selected reference into a visual regional edition, filterable publisher headline collection, retained Evidence Journal, Timeline Journal, and navy/mint ECB market panel. The 244 imported records deduplicate to 223 source URLs at release. Filters combine US/Europe/international context, category, publication window, search, year and month. Paging keeps every recorded result reachable. Source freshness and partial failure are visible; EPSTMC story approval remains separate.

Cloud-browser preview verified Europe selection, combined Economy & Markets filtering (15 matching headlines), route persistence and expansion of the exact ECB observation table. Computed typography is Playfair Display / DM Sans and the desktop screenshot matches the reference palette, hierarchy and three layout roles. The front illustration is a labelled editorial vector, not documentary photography or a geographic map. No fictional oil series was copied. Physical-device QA remains open.

Files: web/worker/news-ui.js, ui.js, editorial-design.js; web/tests/news-ui.test.mjs. Rollback: revert the UI step; source records remain stored. Deployment and GitHub integration are REL-09 events.
