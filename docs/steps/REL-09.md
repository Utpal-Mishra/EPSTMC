# REL-09 — Editorial regional release

Planned and recorded: 25 November 2026 (Europe/Dublin). Actual implementation: pending. Status: PLANNED.

Scope and acceptance: see STEP_TRACEABILITY.md. Dependencies: private v7 website; NEWS-02 depends on NEWS-01 and DESIGN-01; REL-09 depends on all three.

Evidence and implementation: pending. Per-step implementation commit retains the step ID.

Recovery: revert the bounded code step; preserve story history and editorial gates. New ingestion storage is additive. No schedule or audience change. Provider activation, publication and exhaustive coverage are not implied.

## Release checks — 25 November 2026

Implemented and locally validated. Worker build passed; 82 website and 54 Python tests passed. Browser verified the actual editorial page, Europe filter (78 past-month headlines), combined Europe/Economy filter (15), shareable route state, exact 64-row ECB table and computed Playfair Display / DM Sans fonts. Source snapshot: 244 records, 223 unique URLs, eleven successful source feeds, 64 market points; retrieval timestamps retained. Recent wording distinguishes publication windows from event dates. No synthetic story approval or public access change.

The command environment could not connect to the daemon preview over its loopback address; browser preview worked. This is not a live deployment or production refresh validation. Native/mobile QA and authenticated live-browser validation remain separate. GitHub transfer and deployment result will be appended after confirmation.

Recovery: deploy prior v7 for runtime rollback; preserve additive news tables and existing editorial data. No changes to existing schedules or audience.

Source-status correction during release: a failed first runtime refresh now retains the bundled snapshot’s previous successful timestamp and count. Regression assertion verifies it. No provider error details or credentials are displayed.
