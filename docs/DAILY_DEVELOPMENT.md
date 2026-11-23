# EPSTMC daily development tracker

Each row is a bounded milestone work unit, not a claim that seven calendar days
have elapsed. The original Week 4 planning window is 28 November–4 December
2026. The owner requested accelerated Week 4 development on 23 November; all
local work below was performed on that date. Commits retain the Day 1–7 work
unit in their titles for granular Git history. Local completion, GitHub
integration and production verification are separate statuses.

| Unit | Planned outcome | Local evidence / status | GitHub / operational status |
| --- | --- | --- | --- |
| W4-D1 | Approved publication data and service | IMPLEMENTED: migration 003, `publishing.py`; version/sequence checks, immutable publications and audit transaction. | Local commit `7d3b1e8`; push blocked pending explicit approval. |
| W4-D2 | Publication boundaries and corrections | VALIDATED locally: unpublished approvals hidden, prior versions retained, private fields filtered, concurrent publication checked. | Local commit `62bccaa`; Postgres verification pending. |
| W4-D3 | Public read API | IMPLEMENTED: feed, story, versions, readiness, GET/HEAD, cache validation and sanitized failures. | Local commit `7dc8fe4`; hosted endpoint not deployed. |
| W4-D4 | Connected reader application | IMPLEMENTED: evidence desk, source links, historical comparison limits, scenario signals and publication history. | Local commit `c493137`; browser visual QA pending. |
| W4-D5 | End-to-end correction demonstration | VALIDATED locally: real WSGI interface tests and isolated fictional demo database with two published versions. | Local commit `52b2f8a`; no real editorial story approved or published. |
| W4-D6 | Regression and integration checks | VALIDATED locally: rollback, stale approved version, real read connections and demo safeguards; CI matrix prepared. | Local commit `9e12d1a`; remote CI not run. |
| W4-D7 | Release documentation and daily tracking | IMPLEMENTED: runbook, API contract, audit logs, truthful milestone statuses and daily task update. | Current release commit; push and merge remain blocked by approval review. |

## Next run procedure

1. Fetch current GitHub state and inspect relevant local/remote branches before
   selecting work. Never discard or recreate already completed units just because
   a push is blocked or a planned date has arrived.
2. Resolve the Week 3–4 integration blocker first. Automatic approval review
   requires explicit authorization to push the pending Week 3 code. Do not retry
   that rejected publication until authorization is recorded. Do not move the
   same code through another delivery route to bypass the rejection.
3. When authorized, push the tested integration branch, update PR #1 or use a
   clearly scoped successor PR, run SQLite/Postgres CI, fix failures and integrate
   only after checks pass. Preserve concurrent upstream work; no force push.
4. After integration, select exactly one next incomplete daily deliverable from
   the agreed roadmap. Week 5 is the account-free mobile feed; define and test a
   bounded vertical slice before marking it done. Do not treat the browser reader
   as a completed iOS/Android application.
5. Record real date, task ID, commit/PR, tests, files, blockers and next task. Use
   the README status markers for one idempotent entry per calendar date. Keep
   proposed, implemented, validated, integrated and deployed distinct. Preserve
   the structured audit logs. No invented progress, production approvals or
   deployment claims.

The existing daily task was updated on 23 November 2026 to implement a bounded next task rather
than only maintain the README. Its existing schedule is retained; no duplicate
recurring task is needed. If execution, credentials or authorization are missing,
report the blocker and perform only independently authorized work.
