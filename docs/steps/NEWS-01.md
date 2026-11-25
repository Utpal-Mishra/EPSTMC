# NEWS-01 — Regional ingestion

Planned and recorded: 25 November 2026 (Europe/Dublin). Actual implementation: 25 November 2026. Status: IMPLEMENTED / VALIDATED / DEPLOYED v8.

Scope and acceptance: see STEP_TRACEABILITY.md. Dependencies: private v7 website; NEWS-02 depends on NEWS-01 and DESIGN-01; REL-09 depends on all three.

Evidence and implementation: pending. Per-step implementation commit retains the step ID.

Recovery: revert the bounded code step; preserve story history and editorial gates. New ingestion storage is additive. No schedule or audience change. Provider activation, publication and exhaustive coverage are not implied.

## Implementation and live intake — 25 November 2026

Status: IMPLEMENTED / five focused parser/API/D1 tests passed, Worker build passed. Live retrieval at 2026-11-25T14:53:23.990628+00:00 imported 244 dated headline records from all eleven configured feeds and 64 exact ECB reference-rate observations. Titles and links are attributed; no full articles, generated claims, or sample oil-price series are imported. Deduplication is by canonical publisher link. The BBC US feed also includes Canada; international-context topic feeds are explicitly labelled. Coverage is selected and bounded, never exhaustive.

Files: web/worker/news.js, news-snapshot.json, index.js; web/db/schema.js; additive Drizzle migration 0005 and metadata; web/tests/news.test.mjs. Refreshes use allowlisted endpoints, byte/time/concurrency limits and an atomic 15-minute global lock. Partial errors preserve prior data and report source status. Reader opens may request refresh; no unattended schedule is changed. News never creates or approves EPSTMC story versions.

Checks cover malicious links, entity declarations, dated RSS/Atom, deduplication, ECB numeric data, private access, same-origin mutation, partial-source failure, retained snapshots, refresh throttling and separation from publication. A Worker-specific redirect-mode incompatibility was found and corrected to manual redirects. Unknown redirects remain failures rather than broadening network access.

Recovery: retain additive news tables; revert ingestion code while preserving the existing editorial database and records. Integrated browser/source activation is tracked in NEWS-02 / REL-09.
