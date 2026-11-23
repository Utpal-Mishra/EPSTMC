# EPSTMC daily development tracker

Each row is a bounded milestone work unit, not a claim that seven calendar days
have elapsed. The original Week 4 planning window is 28 November–4 December
2026. The owner requested accelerated Week 4 development on 23 November; all
local work below was performed on that date. Commits retain the Day 1–7 work
unit in their titles for granular Git history. Local completion, GitHub
integration and production verification are separate statuses.

| Unit | Planned outcome | Local evidence / status | GitHub / operational status (all units merged via PR #1) |
| --- | --- | --- | --- |
| W4-D1 | Approved publication data and service | IMPLEMENTED: migration 003, `publishing.py`; version/sequence checks, immutable publications and audit transaction. | GitHub commit `28c742d`; uploaded in PR #1; approval recorded 23 Nov. |
| W4-D2 | Publication boundaries and corrections | VALIDATED locally: unpublished approvals hidden, prior versions retained, private fields filtered, concurrent publication checked. | GitHub commit `5718cea`; Postgres 16 CI passed. |
| W4-D3 | Public read API | IMPLEMENTED: feed, story, versions, readiness, GET/HEAD, cache validation and sanitized failures. | GitHub commit `e445d07`; hosted endpoint not deployed. |
| W4-D4 | Connected reader application | IMPLEMENTED: evidence desk, source links, historical comparison limits, scenario signals and publication history. | GitHub commit `bab11fc`; browser visual QA pending. |
| W4-D5 | End-to-end correction demonstration | VALIDATED locally: real WSGI interface tests and isolated fictional demo database with two published versions. | GitHub commit `aadeb42`; no real editorial story approved or published. |
| W4-D6 | Regression and integration checks | VALIDATED locally: rollback, stale approved version, real read connections and demo safeguards; CI matrix prepared. | GitHub commit `322eccc`; CI runs on GitHub; all release CI jobs passed; merged via PR #1. |
| W4-D7 | Release documentation and daily tracking | IMPLEMENTED: runbook, API contract, audit logs, truthful milestone statuses and daily task update. | GitHub commit `b2ff7c6`; merged into main via PR #1 (`04f136e`). |

## Next run procedure

1. Fetch current GitHub state and inspect relevant local/remote branches before
   selecting work. Never discard or recreate already completed units just because
   a push is blocked or a planned date has arrived.
2. Publication of the combined Weeks 1–4 changes was explicitly authorised on
   23 November 2026. The branch is uploaded; the earlier approval blocker is
   resolved. PR #1 merged into main on 23 November (`04f136e`); all release
   CI jobs passed. Continue with the next genuinely incomplete work unit.
3. Fix any failing required CI checks before integration. Preserve concurrent
   upstream work and use fast-forward branch updates; never force push. Code
   integration does not imply a hosted deployment or real editorial publication.
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
