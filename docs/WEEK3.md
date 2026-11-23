# Week 3: editorial draft and review

Scope: an editor attaches stored current and historical evidence, reviews a story
with conditional scenarios, and approves a preserved version. This is a private
Python command-line workflow integrated with Week 2 ingestion. Public publishing,
reader APIs, and mobile screens belong to later weeks.

## Local walkthrough

Python 3.9+; no third-party packages needed for SQLite. Run from the repository
root. All supplied examples below are fictional and must never be published as
real reporting. Use a temporary database for the walkthrough.

```bash
python editorial.py --db /tmp/epstmc-demo.sqlite init
python editorial.py --db /tmp/epstmc-demo.sqlite add-evidence examples/proposal-evidence.json --actor demo-editor --note 'Fictional current source'
python editorial.py --db /tmp/epstmc-demo.sqlite add-evidence examples/archive-evidence.json --actor demo-editor --note 'Fictional historical source'
python editorial.py --db /tmp/epstmc-demo.sqlite create bus-pilot examples/editorial-draft.json --actor demo-editor --note 'Fictional initial draft'
python editorial.py --db /tmp/epstmc-demo.sqlite submit bus-pilot --version 1 --actor demo-editor --note 'Ready for source review'
python editorial.py --db /tmp/epstmc-demo.sqlite queue
python editorial.py --db /tmp/epstmc-demo.sqlite show bus-pilot --version 1 --markdown
python editorial.py --db /tmp/epstmc-demo.sqlite approve bus-pilot --version 1 --actor demo-reviewer --note 'Fictional review demonstration' --review examples/editorial-review.json
python editorial.py --db /tmp/epstmc-demo.sqlite revise bus-pilot examples/editorial-draft.json --version 1 --actor demo-editor --note 'Demonstrate a new version; first approval remains intact'
python editorial.py --db /tmp/epstmc-demo.sqlite history bus-pilot
```

For rejection, run `reject STORY --version N --actor EDITOR --note REASON` on an
`in_review` version. Revise to create a fresh draft, then submit again. `--version`
for revise, submit, approve and reject must equal the latest version. A stale
editor cannot overwrite or approve a superseded revision. Queue output contains
only each story's latest version; history includes every version and action.

## Connect real intake

```bash
python ingest.py --db /tmp/epstmc-evidence.sqlite --document 2025-05936
python editorial.py --db /tmp/epstmc-evidence.sqlite init
python ingest.py --db /tmp/epstmc-evidence.sqlite --list
```

Create an editorial JSON file following `examples/editorial-draft.json`. Use
`{"id": "fr-2025-05936"}` in its sources to attach the actual imported record.
Register any additional dated historical evidence using `add-evidence` first.
The source's stored title, URL, publication date and retrieval provenance are
resolved from the database; supplied draft metadata cannot replace them.
Historical sources need an ID, title, URL, publication date and publisher.
Registration records who supplied the metadata, when and why; it does not fetch
or verify the page. Correct registered metadata under a new source ID.

Every fact, historical comparison and scenario requires source references.
Historical entries require `comparison` and `limitations`; scenarios require
`condition`, `signal` and `timeframe`. All three sections must be present and
nonempty for this pilot's complete editorial brief. The original lightweight
`brief.py` format remains supported separately.

Human review determines whether the cited material supports the claims. Open and
check each original source, the dates, comparison limits and conditional wording.
Only then provide a review JSON with `evidence_checked: true`, every attached ID
in `checked_source_ids`, `scenarios_are_conditional: true`, and a written
`assessment`. The software checks these attestations and references; it does not
independently fact-check them or perform AI research.

## Shared Postgres

Install `requirements-postgres.txt`. As schema owner, apply migrations in order:

```bash
psql "$EPSTMC_DATABASE_URL" -v ON_ERROR_STOP=1 -f migrations/001_federal_register_evidence.sql
psql "$EPSTMC_DATABASE_URL" -v ON_ERROR_STOP=1 -f migrations/002_editorial_postgres.sql
python ingest.py --postgres --document 2025-05936
python editorial.py --postgres create STORY draft.json --actor EDITOR --note 'Initial draft'
python editorial.py --postgres queue
```

Use `--postgres` instead of `--db PATH` for other editorial commands. The local
`init` command is SQLite-only. Use provider TLS settings; keep the `epstmc`
schema outside public API exposure. The trusted editorial role needs schema
USAGE, SELECT on intake, SELECT/INSERT on editorial tables, UPDATE on stories and
versions, and USAGE/SELECT on the editorial event identity sequence. The intake
worker should retain only its existing evidence-table permissions. Do not give
reader clients these credentials. Actor names are audit labels supplied by a
trusted operator; this CLI does not implement user authentication or prove an
actor's identity. Future web endpoints must add authenticated editorial access.

Version writes and audit events commit atomically. SQLite serializes writers;
Postgres locks the story row before checking the latest version. Source snapshots
and SHA-256 content hashes preserve what was reviewed even when upstream intake
changes. Database triggers protect stored content, finalized reviews and audit
events from ordinary modification/deletion. Database owners remain able to
change schema and are trusted administrators. Approval creates editorial state;
it does not publish to a feed or send alerts.

## Verification

```bash
python -m unittest discover -s tests -v
python brief.py examples/brief.json
```

The same behavioral suite runs against a disposable Postgres database when
`EPSTMC_TEST_DATABASE_URL` is set. Never point that variable at production: tests
insert fictional evidence. GitHub Actions provisions its own Postgres 16 service
and runs both backends. A hosted production database is not configured in this
workspace; hosted migration and live production intake remain unverified.
