# Week 4 — publishing, corrections and the public reader

Week 4 is integrated with Week 3 in the application source. Editorial approval and
public publication are separate operations. Production hosting and hosted production Postgres verification remain pending;
GitHub CI now verifies the database workflow with disposable Postgres 16. This milestone provides a
working WSGI reader and public read API, not an app-store release.

## Try the complete reader locally

Python 3.9+, standard library for SQLite. Use a fresh path. Demo setup refuses to
modify an existing database. All demo publications and approvals are fictional.

```bash
python demo.py --db /tmp/epstmc-reader-demo.sqlite
python app.py --db /tmp/epstmc-reader-demo.sqlite
```

Open `http://127.0.0.1:8080/`. The evidence desk opens without an account. Open
the fictional story, follow its sources, and inspect version 1 and the version 2
correction. HTML and API read from the same publication service; no separate
mock feed is used. Layout includes a mobile viewport, responsive typography,
semantic headings, keyboard link focus, and escaped editorial text. Local HTTP
socket startup is restricted in this execution environment, so tests exercise
the WSGI application directly. A visual browser check remains pending.

## Publish real editorial work

Use the same SQLite database as `ingest.py` and `editorial.py`:

```bash
python editorial.py --db evidence.sqlite init
python publishing.py --db evidence.sqlite init
# Ingest evidence, create, submit and approve with the Week 3 workflow first.
python publishing.py --db evidence.sqlite publish STORY --version 1 --expected-publication 0 --kind initial --summary 'Public description of the first publication' --actor EDITOR
python app.py --db evidence.sqlite
```

`--summary` is public. Do not put private review notes in it. The actor is a
private audit label, supplied by a trusted operator. The read API provides no
editorial write or approval endpoint.

For a correction, revise the story, submit and approve the new editorial version,
then publish with `--kind correction`, a clear public correction summary, and
the current publication sequence. Example if the second editorial version is
also the second publication:

```bash
python publishing.py --db evidence.sqlite publish STORY --version 2 --expected-publication 1 --kind correction --summary 'Explain the specific factual correction' --actor EDITOR
```

Use `update` for new information and `correction` for fixing an earlier claim.
Editorial version numbers may skip when drafts are rejected or superseded;
publication sequence counts only actual publications. Neither approval nor a
new draft replaces the live story. Publication requires the latest editorial
version to be approved, a valid review and content hash, the expected publication
sequence and a newer version than the previous publication. Concurrent or stale
publish attempts cannot overwrite the first successful action. Publication and
its private audit event commit together. Published rows are append-only.

## Public routes

| Method | Route | Result |
| --- | --- | --- |
| GET / HEAD | `/` | Published feed HTML; `cursor` optional. |
| GET / HEAD | `/stories/ID` | Latest published story; `?version=N` opens a published older version. |
| GET / HEAD | `/api/v1/feed` | Latest publication per story; `limit` 1–100 and opaque `cursor` optional. |
| GET / HEAD | `/api/v1/stories/ID` | Latest published story JSON. |
| GET / HEAD | `/api/v1/stories/ID/versions` | Published versions, newest publication first, with update/correction explanations. |
| GET / HEAD | `/api/v1/stories/ID/versions/N` | A specific published editorial version. |
| GET / HEAD | `/health` | Database readiness; no evidence rows or internal error details. |

Unknown or unpublished stories/versions return 404. Invalid parameters return 400;
write methods return 405; missing database/schema returns 503. Success responses
have ETags and require revalidation (`Cache-Control: no-cache`); unchanged
conditional reads return 304. Errors use `no-store`. Feed pagination uses a
publication-time/story-ID cursor. It is a live feed rather than a frozen snapshot:
newly updated stories can move ahead of a previously obtained cursor; refresh
the first page to see them. No automatic refresh/offline claim is made here;
those remain Week 6.

Public JSON includes only approved published content fields and source provenance.
It excludes arbitrary extra draft fields, review assessments, operator identities
and registration notes. Responses include security headers. The application
renders text with HTML escaping and does not execute editor-supplied markup.

## Postgres and deployment

Apply migrations 001, 002, then `003_publication_postgres.sql` as schema owner.
Use `--postgres` instead of `--db PATH` for publishing and reader commands. Set
`EPSTMC_DATABASE_URL` privately using provider TLS settings. The server should
use a separate read-only database role with schema USAGE and SELECT on
`story_publications` and `editorial_versions`; never send database credentials
to browser or mobile clients. These tables are private server-side dependencies,
not a client database API. The reader also enables a read-only session. The
editorial publisher needs SELECT/INSERT on publications plus the existing Week 3
permissions. Keep the schema outside automatic public API exposure.

`app.create_app(path=...)` or `app.create_app(postgres=True)` returns the WSGI
application. `python app.py` uses the standard library development server bound
to localhost. For public hosting, configure a production WSGI server, TLS and
runtime secrets in the selected hosting environment. No hosting provider,
production URL or production credentials have been configured by this change.

## Verification and limits

Run `python -m unittest discover -s tests -v`. The suite covers editorial review,
publication gating, read isolation, stale/concurrent operations, rollback,
corrections, immutable history, private-field filtering, API status codes,
ETags, HTML escaping and the real reader connection. The same suite supports a
disposable Postgres database through `EPSTMC_TEST_DATABASE_URL`; never set this
test variable to production. CI is prepared for Python 3.9/3.12 and Postgres 16.
The Postgres 16 GitHub CI job passed; final Python/backend CI and merge status
are recorded in PR #1. GitHub integration was authorised on 23 November 2026. Local socket permissions prevent a local Postgres/browser server run.

See [daily development tracking](DAILY_DEVELOPMENT.md) for stages and blockers.
