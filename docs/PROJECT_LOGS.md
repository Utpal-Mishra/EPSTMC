# EPSTMC project audit trail

Private project record. Baseline for this work is the fetched prototype branch
plus main's status entries through 23 November 2026. Older conversations are not
reconstructed as verified implementation. Owner: Utpal Mishra; implementation:
Codex. Date: 23 November 2026. Change group: W3-20261123.

| ID / log | Context and decision | Rationale / evidence | Status / follow-up |
| --- | --- | --- | --- |
| W3-BL-01 Business Learning | Use the roadmap's editorial review completion check as the Week 3 boundary. | README separates editorial approval from Week 4 public publication. | AGREED/PLANNED scope; workflow implemented. |
| W3-SY-01 System | Add a private CLI for source registration, draft creation, submission, queue, review, revision, preview and history. | `editorial.py`; reproducible commands in `WEEK3.md`. | IMPLEMENTED; manual operation. |
| W3-AR-01 Architecture | Store story heads, immutable version payloads, registered evidence and append-only audit events. | Migrations 002; source snapshots plus content hashes; transactions. | IMPLEMENTED; protected publishing API remains Week 4. |
| W3-AU-01 Automation | Add SQLite and Postgres CI jobs. Keep approval explicitly operated by an editor. | `.github/workflows/editorial.yml`; tests use fictional attestations only. | IMPLEMENTED; no new schedule created. Existing daily task unchanged. |
| W3-RE-01 Recommendation | Review original sources and comparison limits before approval; use database roles for trusted editorial access. | Software reference checks do not establish factual support. | RECOMMENDED operational procedure; documented. |
| W3-EX-01 Experiment | Exercise draft → review → approval → revision and review → rejection → revision. | Behavioral tests and fictional CLI walkthrough. | VALIDATED locally on SQLite; Postgres tracked in CI. |
| W3-EE-01 External Evidence | Reuse the Federal Register intake integration. Additional historical metadata is manually registered with original links and dates. | `ingest.py`, migrations 001 and source snapshots. | No new live reporting claim introduced; tests are fictional. |
| W3-RA-01 Risk & Assumption | Operator may falsely attest source review. Method: workflow threat review; likelihood medium, impact high. | CLI cannot independently prove factual support or actor identity. | Mitigate with trusted credentials and explicit evidence checklist; owner Utpal; web authentication pending. |
| W3-RA-02 Risk & Assumption | Concurrent edits or upstream changes could invalidate approval. Likelihood medium, impact high. | Story row locks / SQLite write lock, latest-version checks, immutable payloads, review hash, atomic events. | IMPLEMENTED mitigation; concurrency regression included. |
| W3-DI-01 Data & Integration | Resolve draft source IDs directly from intake or historical evidence tables; preserve provenance per version. | Duplicate intake and source-snapshot regression tests. | IMPLEMENTED; hosted Postgres credentials absent, production verification pending. |
| W3-PF-01 Product / Feature | Require historical comparison and limitations plus conditional scenario trigger, timeframe and signal. | Draft validation and Markdown previews. | IMPLEMENTED; no reader UI in this milestone. |
| W3-MF-01 Merchant & Fulfilment | No merchant or fulfilment workflow in this milestone. | Editorial infrastructure only. | NOT APPLICABLE. |
| W3-EP-01 Expansion | Publication, corrections feed and public version history remain the next milestone. | Approved version contract supplies a stable input for Week 4. | AGREED/PLANNED; not claimed as shipped. |
| W3-DE-01 Decision | Integrate the workflow with the existing prototype and current status history; preserve earlier local worktrees. | New isolated worktree based on fetched origin refs; no reset or force push. | IMPLEMENTED; PR integration recorded in Git history. |
| W3-SP-01 Security & Privacy | No public endpoint or secrets in fixtures. Postgres errors expose error classes rather than connection strings. | CLI connection wrapper; ignored local environment/database files; fictional CI database. | IMPLEMENTED; trusted editorial roles required for hosting. |
| W3-QA-01 Validation / QA | Test missing evidence, incomplete approval, missing scenario/history fields, stale versions, rollback, immutable content, duplicate intake and revisions. | `tests/test_editorial.py`; CI runs both supported stores. | Local results and remote CI recorded in release follow-up below. |
| W3-CR-01 Change / Release | Week 3 implementation is code integration, not a production app launch or editorial publication. | No hosted database configured and reader application not yet implemented. | Production rollout pending setup and Week 4 onward. |

## Release verification

- Local SQLite behavioral suite: 17 tests passed before release checks.
- Postgres verification: test suite and migrations prepared, but local server startup is blocked by the runtime's socket permissions. No Postgres behavioral result is claimed.
- Hosted production Postgres migration/intake: pending credentials and setup.
- GitHub push was blocked by automatic approval review: remote publication needs explicit user authorization. Local implementation is committed; remote CI and merge have not run.
- No real story was approved by automation. Examples and test approvals are explicitly fictional.

## Week 4 — W4-20261123

All seven work units below were implemented on 23 November 2026; day labels
identify the planned work breakdown, not seven elapsed days. Previous Week 3
status entries above describe that milestone's verification at the time.

| ID / log | Context and decision | Rationale / evidence | Status / follow-up |
| --- | --- | --- | --- |
| W4-BL-01 Business Learning | Separate approval from publication and explain corrections to readers. | `Publisher.publish`, public version history, tests for unpublished approvals. | IMPLEMENTED and VALIDATED locally. |
| W4-SY-01 System | Connect intake → editorial approval → publication → reader/API through one database. | `publishing.py`, `app.py`, `reader.py`; actual read-connection and demo tests. | IMPLEMENTED; GitHub integration blocked. |
| W4-AR-01 Architecture | Append-only publication records point to immutable editorial versions. | Migration 003; expected publication sequence, story lock and atomic event write. | IMPLEMENTED; SQLite tested, Postgres not executed. |
| W4-AU-01 Automation | Update the existing daily task from status-only to one bounded next development unit. | Automation update confirmed 23 Nov; existing flexible daily schedule preserved. | CONFIGURED; future execution is not guaranteed. Pending push rejection must not be bypassed. |
| W4-RE-01 Recommendation | Gate GitHub integration on backend CI and configure a read-only server database role before hosting. | WSGI application factory, provider-neutral runbook and CI matrix. | RECOMMENDED; production configuration pending. |
| W4-EX-01 Experiment | Simulate initial publication, correction and old-version reading using fictional evidence. | `demo.py`, API tests and public projection tests. | VALIDATED locally without real editorial approvals. |
| W4-EE-01 External Evidence | No new external reporting claims introduced. Source snapshots reuse ingested/registered provenance. | Public source field allowlist; fictional examples. | IMPLEMENTED; original-page review still belongs to an editor. |
| W4-RA-01 Risk & Assumption | Draft or private metadata might leak through the reader. Method: boundary tests; likelihood medium, impact high. | Explicit field projection, published-only queries and read-only connection. | Mitigated locally; owner Utpal; hosted review pending. |
| W4-RA-02 Risk & Assumption | Concurrent/stale publishers might overwrite content or lose audit events. Likelihood medium, impact high. | Lock/sequence checks, append-only triggers, concurrency and rollback tests. | VALIDATED locally on SQLite; Postgres CI pending. |
| W4-DI-01 Data & Integration | Reader returns published version content, dates, source links and public change summary. | Feed/story/history API contract and tests. | IMPLEMENTED; no public database API exposure. |
| W4-PF-01 Product / Feature | Account-free web evidence desk with scenario signals, comparison limits and correction history. | Responsive HTML template, viewport, escaped content and semantic headings. | IMPLEMENTED; browser visual QA pending. Does not complete native mobile Week 5. |
| W4-MF-01 Merchant & Fulfilment | No commerce or fulfilment requirement. | News publishing scope. | NOT APPLICABLE. |
| W4-EP-01 Expansion | Continue native mobile feed after integration; keep refresh/offline/alerts in their planned milestones. | Roadmap and daily tracker. | AGREED/PLANNED; no unsupported completion claims. |
| W4-DE-01 Decision | Deliver seven local day-labelled commits, retain actual implementation date and report remote blockers accurately. | Git history; `DAILY_DEVELOPMENT.md`. | IMPLEMENTED; requires explicit combined Week 3–4 push authorization. |
| W4-QA-01 Validation / QA | Exercise API routes, response codes, cache validation, private-field filtering, HTML escaping, publication history and demo safety. | 42 local tests pass; compilation and diff checks pass. | VALIDATED locally; remote/Postgres CI not run. |
| W4-SP-01 Security & Privacy | API supports only GET/HEAD; no public review/approval endpoint; database details do not appear in errors. | Method/status and missing-database tests; CSP, no-sniff and referrer headers. | IMPLEMENTED; production TLS/runtime configuration pending. |
| W4-CR-01 Change / Release | Local application integration completed; remote integration rejected by automatic approval review. | GitHub push rejected because pending Week 3 publication approval was unresolved. | BLOCKED: no further push/merge attempted through another route. |


## Weeks 1–4 integration follow-up — 23 November 2026

- INT-DE-01 Decision: owner explicitly authorised integration of all pending Weeks 1–4 work. Earlier push-approval blocker resolved; no production deployment requested.
- INT-SY-01 System / Data: transferred the complete source tree to the existing GitHub PR branch and verified its Git tree equals the tested local source. Git CLI lacked credentials; connected GitHub operations preserved the ten-commit development sequence without a force update.
- INT-AU-01 Automation: daily task will use current GitHub code and next unfinished work, with the obsolete approval blocker removed; existing cadence retained.
- INT-QA-01 Validation: all 42 local tests pass. The first Postgres 16 CI job passed all tests. Python 3.9 setup failed on the default Ubuntu 26.04 image; pinned CI to Ubuntu 22.04 and disabled matrix fail-fast, then reran checks. Final check and merge status are visible in PR #1.
- INT-PF-01 Product / Governance: added explicit launch scope, source review, update/correction and future alert rules in EDITORIAL_POLICY.md, closing the Week 1 policy documentation gap. Alerts remain unimplemented in this milestone.
- INT-RA-01 Risk & Assumption: hosted production database, public deployment and browser visual QA remain pending. CI uses disposable data; no real reporting was approved or published.
- INT-CR-01 Change / Release: PR #1 tracks final integration; daily milestone GitHub hashes updated to match the uploaded sequence. Retained earlier blocker entries above as historical audit evidence.


### Integration completed

INT-CR-02 — 23 November 2026: PR #1 merged successfully into main at
`04f136eea904724bf6efeaa6b2433049eab4d816`, with head
`3df8b88cd756cdb192f0dd6999e179986b5db9ac`. All three jobs in release CI run
45278577458 passed: SQLite/Python 3.9, SQLite/Python 3.12, Postgres 16. Each ran
the 42-test suite. Verified the release head is an ancestor of fetched main and
the application, migrations, tests and documentation are present there.
The daily task retains its schedule and now continues the next incomplete unit.
Hosted production setup, deployment and visual QA remain pending.

## Reader review — 23 November 2026

- REVIEW-SY-01 System / Product: provide a private hosted reader snapshot with one clearly fictional story and two publications, plus a guided workflow page. Drafting/approval remain CLI-only; no live news claim.
- REVIEW-AR-01 Architecture / Data: export the actual WSGI-rendered HTML and the published public projection from a disposable SQLite database. Static navigation uses version pages and JSON snapshots; no database or private review fields are uploaded.
- REVIEW-EX-01 Experiment / QA: 43 local tests passed; exporter links and private-field filtering checked. Browser inspection verified the feed, corrected story and version 1 warning. The private deployed origin presents its expected ChatGPT sign-in gate.
- REVIEW-SP-01 Risk & Assumption / Decision: keep the review owner-only. Make fictional content and snapshot limitations explicit on every page. Hosted demo does not complete production hosting, live intake, ongoing refresh, or a web editorial console.
- REVIEW-AU-01 Automation / Recommendation / Expansion: generation is on demand; no new schedule or notification. Continue planned mobile/editorial work from the current main branch; do not treat this snapshot as a native app.
- REVIEW-EE-01 External Evidence / Business Learning: evidence links are explicitly fictional placeholders; this review validates navigation and provenance presentation, not source factual support. No real news was approved or published.
- REVIEW-MF-01 Merchant & Fulfilment: not applicable. REVIEW-CR-01 Change / Release: private review site version and reproducible export process recorded in REVIEW_SITE.md.


## Seven-day execution change — 23 November 2026

- NEXT7-DE-01 Decision / Business Learning: owner requests actual day-by-day code and website integration, rather than a single seven-day batch. Prioritise one real history-to-present story before native mobile work. Record the seven dated targets in NEXT_7_DAYS.md; all remain PLANNED.
- NEXT7-SY-01 System / Architecture / Product: use the current GitHub main and existing owner-private reader Site. The fictional snapshot remains the baseline. Plan evidence chronology, timeline navigation, reviewed updates, browser review and durable website data; no feature implementation is claimed during setup.
- NEXT7-AU-01 Automation: reconfigure the existing task for seven daily runs, 24–30 November, approximate 09:00 Europe/Dublin. One newly completed unit per date, idempotent reruns, no future-day code or backdating. It stops after the seven occurrences.
- NEXT7-RE-01 Recommendation / Experiment / External Evidence: verify one primary-source case study at run time, distinguish event/publication/retrieval dates, and label drafts and coverage gaps. Source selection is still pending, not fabricated or marked complete.
- NEXT7-RA-01 Risk & Assumption / Data: dates are targets; factual coverage, human review and hosting setup can block completion. Mitigate with explicit pending states, dependency checks and separate validation of source, code and website freshness. Owner: Utpal. Status: PLANNED.
- NEXT7-EP-01 Expansion / Merchant & Fulfilment: native mobile follows this prioritised phase; no commerce scope. No paid-service activation or access widening authorised.
- NEXT7-QA-01 Validation / Change: inspect branch/PR state, test each daily change, push that day's increment and merge after passing checks, then verify the private Site result. Preserve existing audit history. This setup commit contains documentation only.


## HTP implementation — 23 November 2026

| Log / ID | Decision, change and rationale | Evidence / status |
| --- | --- | --- |
| Business Learning HTP-BL-01 | Deliver one real source-backed history-to-present case before native mobile. Selected events are related by topic, not asserted as one causal chain or one facility. | Five primary pages read; selected coverage and gaps explicitly labelled. IMPLEMENTED. |
| System HTP-SY-01 | Replace the hosted fictional snapshot with a private Worker-backed workspace: timeline, intake, review and reader. Preserve Python CLI functionality. | `web/worker`, `timeline.py`; local checks pass. Deployment tracked separately. |
| Architecture HTP-AR-01 | D1 provides durable hosted versions/evidence/checks/audit; a shared case contract retains facts/history/scenarios/source structure. Conditional SQL batches and immutable guards protect review/publication lineage. | Generated Drizzle schema migrations and rollback/concurrency tests. IMPLEMENTED / VALIDATED locally. |
| Automation HTP-AU-01 | Latest owner instruction requests the full seven-unit set now. Future scheduled runs perform intake/reliability checks and bounded fixes, rather than rebuild completed work. | Original plan retained as history; daily prompt updated at release. |
| Recommendation HTP-RE-01 | Review originals and coverage limitations before approving. A successful Federal Register query is not a full story fact-check. | Freshness scope is visible; owner-only review checklist. RECOMMENDED / IMPLEMENTED controls. |
| Experiment HTP-EX-01 | Exercise chronology, filters, stale writes, durable restart, source failures, corrections and rejected unauthorized actions. | 45 Python and 18 Worker/D1 tests passed; browser year/month and review screens inspected. VALIDATED locally. |
| External Evidence HTP-EE-01 | Use GPO/FR, White House, DOE/NNSA and Senate primary pages with distinct event/publication dates. Latest case event is 6 Nov 2026; research checked 23 Nov. | Source URLs and case boundaries recorded in HISTORY_TO_PRESENT.md. No claim of an unverified agency response. |
| Risk & Assumption HTP-RA-01 | Reader may confuse retrieval freshness with a new event, or negotiations with operational delivery. Likelihood medium, impact high. | Mitigate with separate dates, status labels, source attribution and explicit gaps. Owner Utpal. IMPLEMENTED. |
| Data & Integration HTP-DI-01 | Intake stores fingerprinted source revisions, preserves first retrieval and queues candidates without changing claims. Failed checks preserve the previous successful timestamp. | Retry/deduplication tests; source uses fixed approved API, not arbitrary URL fetching. IMPLEMENTED. |
| Product / Feature HTP-PF-01 | Year/month timeline, original-source links, source queue, browser review and publication history share durable data. Visible reader refreshes every minute and on resume. | Browser inspection and API tests; no automatic human approval. IMPLEMENTED. |
| Merchant & Fulfilment HTP-MF-01 | No merchant or fulfilment operations. | NOT APPLICABLE. |
| Expansion HTP-EP-01 | Broader archives, more topics and native apps remain subsequent work. No complete historical coverage or instant news detection is asserted. | AGREED/PLANNED boundaries retained. |
| Decision HTP-DE-01 | Preserve the existing owner-private Site and project ID. Narrow machine updater routes rely on its private platform gate; actual review/publication additionally requires browser identity and Origin checks. | Runtime shared-update flag configured; role/access policy unchanged. Do not reuse on a public Worker. |
| Security & Privacy HTP-SP-01 | No credentials or private review notes in browser bundles/publications. Preview identity injection exists only in the local QA adapter, outside the deployed bundle. | Auth/Origin tests, explicit projection and source URL validation. VALIDATED locally. |
| Change / Release HTP-CR-01 | Seven units implemented in one current session on the owner's latest request. Do not backdate or claim seven elapsed days. | GitHub integration and hosted D1 verification recorded after release. |

HTP-REL-01 — Hosted verification: the retained private Site deployment succeeded
with runtime environment revision 1 and D1 tables provisioned by migrations.
Idempotent service initialization saved the real research case as draft version 1
with five events. Live intake returned 20 pending candidates and a separate status
request confirmed the durable success timestamp `2026-11-23T23:15:22.748Z`.
No candidate was auto-attached and no real story was approved or published.


HTP-REL-02 — Integration complete: PR #3 merged at `3335c514907f531381fdd6254a175e4cda3b6ab6`.
Release CI run 45287420076 passed all four jobs (45 Python, 18 Worker/D1 tests).
Uploaded application/web blobs matched local files exactly. Hosted setup and
live intake independently verified D1 persistence. The private Site version is
`appgprj_6b04bdf51930819196bfe67273bccb48~appgver_4593c150a988819188be7da7a6bdabe9`.
The scheduled task retains its seven morning runs and now performs reliability
and source checks. Owner approval and physical mobile-device QA remain pending.


UI-TEXT-01 — 23 November 2026: owner requested the timeline heading change from “History to present” to “News Timeline”. Updated the reader template in GitHub and the existing private Site source. Copy-only change; build verification used.
