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
