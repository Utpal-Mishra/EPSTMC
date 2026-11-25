# History-to-present integration

Trace individual requirements and recording commits in [STEP_TRACEABILITY.md](STEP_TRACEABILITY.md). Historical status statements below retain their original date/context.

The seven requested units are implemented together following the owner's latest
instruction to develop and integrate the full set. They are no longer future
feature promises for seven separate dates. Actual implementation date:
23 November 2026. The existing private URL is retained.

## What is implemented

| Unit | Implementation | Evidence |
| --- | --- | --- |
| 1 — Real story | Federal-land AI infrastructure case with five original primary sources, January 2025 to November 2026 | `web/worker/case-study.json`; source review below |
| 2 — Evidence chronology | Separate event/publication/retrieval/research dates, chronology and reference validation, explicit coverage gaps | `timeline.py`, `web/worker/model.js`, regression checks |
| 3 — Year/month navigation | Year and month filtering, reset, source links and present-position summary | `web/worker/ui.js`; browser checked 2026 → November (one event) |
| 4 — Source intake | Bounded fixed Federal Register query, three-attempt retry, immutable evidence fingerprints, pending candidate queue, independent last-attempt/last-success fields | Worker intake and D1 tests |
| 5 — Browser review | Owner identity required, same-origin writes, draft revision, source checklist, assessment, submit/approve/reject and explicit publication | Worker review routes and browser UI; no real approval automated |
| 6 — Durable website | D1 story/version/evidence/check/audit tables; append-only publications; reader ETags, visible-page polling and resume refresh | D1 persistence-across-restart, concurrency and rollback tests |
| 7 — End-to-end checks | Python regression suite, Worker/D1 tests, browser timeline and review inspection, GitHub CI job | 45 Python tests and 18 Worker tests passed locally; release CI/deployment status recorded separately |

## Real source-backed case

The selected story is a thematic chronology rather than one construction
project. The website states explicitly that these events share a topic and are
not a proven causal chain. It distinguishes policy, information requests,
negotiation announcements and oversight. Source pages were read on 23 November.

| Event | Source publication | Original source |
| --- | --- | --- |
| 14 Jan 2025: EO 14141 | 17 Jan 2025 | https://www.govinfo.gov/content/pkg/FR-2025-01-17/html/2025-01395.htm |
| 7 Apr 2025: DOE RFI | 7 Apr 2025 | https://www.federalregister.gov/documents/2025/04/07/2025-05936/request-for-information-on-artificial-intelligence-infrastructure-on-doe-lands |
| 23 Jul 2025: EO 14318 | 23 Jul 2025 | https://www.whitehouse.gov/presidential-actions/2025/07/accelerating-federal-permitting-of-data-center-infrastructure/ |
| 20 Jul 2026: Savannah River negotiations | 20 Jul 2026 | https://www.energy.gov/nnsa/articles/nnsa-selects-amentum-ai-data-center-and-energy-project-savannah-river-site |
| 6 Nov 2026: oversight request | 6 Nov 2026 | https://www.heinrich.senate.gov/newsroom/press-releases/heinrich-demands-answers-on-trump-administrations-push-to-build-data-centers-on-public-lands |

The latest verified event in this case study is 6 November 2026. The source
research check is later; that does not create a newer event. A response to the
requested 20 November deadline was not verified here, and no absence of response
is asserted. A negotiation announcement is not proof of a completed lease or
operational facility. This selected-source story is not exhaustive coverage.

## Data and application integration

The original Python CLI, SQLite/Postgres workflow and public-reader tests remain
available. `timeline.py` validates the shared real-case contract and can filter
it (`python timeline.py --year 2026 --month 11`).

The hosted runtime is `web/worker/index.js`, bundled to a single Worker ES module.
It uses D1 rather than opening a Postgres TCP connection, which this hosting
runtime does not support. This is an additional connected web runtime, not a
claim that an unconfigured hosted Postgres instance is now connected. Stories
use the existing facts/history/scenarios/source structure plus a dated timeline.
Changes made in the hosted browser persist to D1; they do not silently overwrite
the GitHub research baseline or a separate Python database.

Schema changes are generated through `web/db/schema.js` and Drizzle; generated
SQL and metadata are tracked. Custom append-only/review guards are a separate
schema migration. Migrations contain no story seed. Setup inserts the bundled
research idempotently as a draft; no approval or publication is invented.

## Private access and review

The Site remains owner-only. Sites dispatch supplies authenticated user headers;
all browser review, draft and publishing actions require that identity and a
matching request Origin. The local QA adapter injects a development identity
only in the separate preview server; it is never bundled into production.
Anonymous API calls fail. Draft content and private review assessments stay out
of the approved reader projection and publication history. The owner-private
research preview is intentionally visible before a first approved publication.

Publication requires the latest approved version, complete source-review
attestation, conditional-scenario confirmation, written assessment and the
expected publication sequence. New drafts do not replace a published story.
Corrections require a public explanation and preserve earlier versions.
Atomic batches and conditional updates prevent stale or concurrent changes from
silently winning. Audit-write failure rolls back publication.

`EPSTMC_PRIVATE_UPDATES=enabled` allows only the narrowly scoped service setup,
intake and status routes behind the confirmed private Sites access boundary.
Unattended callers obtain the supported Sites bearer and send it only as
`OAI-Sites-Authorization` to this exact Site. No credential belongs in code,
URLs, schedule text or logs. These routes cannot approve or publish reporting.
Disable shared updates before any future audience change; a public deployment
needs explicit application roles and service authorization.

## Using the website

1. Sign in at the existing private review URL.
2. Explore the evidence desk and timeline; select a year and month.
3. Use **Check Federal Register** to fetch candidates. A search match alone is
   not confirmed relevance or support for a claim.
4. Open **Editorial review**. Attach relevant candidate metadata to a fresh
   draft, edit the structured claim/timeline content and record the reason.
5. Submit, then check original sources and complete the assessment before
   approving. Publish separately with a public explanation.
6. Reader refreshes pick up the new durable projection; publication history
   retains earlier approved publications.

The reader polls on a visible page every minute and refreshes on resume. Source
intake itself is explicit or run by the existing daily maintenance task. This is
not an assertion of continuous source monitoring, complete historical coverage,
or immediate event detection. Freshness and source errors are visible.

## Validation

Python: `python -m unittest discover -s tests -v`.
Web: from `web/`, `npm ci`, `npm run build`, `npm test`.
The Worker tests use a disposable local D1-compatible database, official runtime
emulation, fake remote responses and synthetic review/publication decisions.
No automated test approves the live researched story. Local persistence across
Worker restart, duplicate intake, failed-source recovery, stale edits,
publication rollback, access checks and immutable data are covered.

Browser QA checked the live rendered research preview, year/month filtering and
review controls without approving the real story. Responsive CSS is included;
physical iOS/Android device QA is not claimed. Production D1 and live source-check
results must be recorded after deployment rather than inferred from these tests.

## Hosted verification — 23 November 2026

The existing private origin was successfully upgraded to Worker version
`appgprj_6b04bdf51930819196bfe67273bccb48~appgver_4593c150a988819188be7da7a6bdabe9`.
The native database overview confirmed all six D1 tables. Private service
initialization returned HTTP 200 with a saved research-preview draft, version 1
and five timeline events. Live Federal Register intake returned HTTP 200 with
20 unreviewed candidates at `2026-11-23T23:15:22.748Z`; a separate status request
confirmed the successful check was stored. These candidates were not promoted
to claims, timeline events or publications. No real review approval was automated.


## GitHub integration

PR #3 merged into main on 23 November 2026 at
`3335c514907f531381fdd6254a175e4cda3b6ab6` after release CI run
45287420076 passed all four jobs: website (18 Worker/D1 tests), Python 3.9 SQLite,
Python 3.12 SQLite and Postgres (45 Python tests per job). Verified all 20 new
application/web files against the uploaded Git blobs with no content mismatch.
The existing 24–30 November task now checks source intake and reliability and
makes bounded follow-up fixes rather than rebuilding the delivered units.
