# Website expansion: seven tracked work units

Owner selected continued website expansion over the original native-app Week 5
milestone. Implementation began 23 November 2026. W5-D1–D7 below are work-unit
identifiers, not seven elapsed calendar days or claims of native-app delivery.
Each unit has a separate Git commit with its actual timestamp. Native iOS/Android,
full offline reading and push notifications remain future work.

| Unit | Integrated behavior | Verification |
| --- | --- | --- |
| W5-D1 | Multiple stories in D1, isolated drafts/reviews/publications/history; owner-only story creation | Cross-story revision, publication and private-draft isolation tests |
| W5-D2 | Explicit region/category metadata and deterministic feed ordering | Shared model validation and feed-selection checks |
| W5-D3 | Evidence Desk feed with region/category filters and clear research/publication badges | Browser feed and empty-state inspection |
| W5-D4 | Search title/subtitle/summary; past month/3/6/12-month windows | Combined filters, inclusive event-date boundaries and future-event checks |
| W5-D5 | Saved reading list on this browser; remove and saved-only controls | Browser save/filter verified; storage failure uses a temporary in-tab list |
| W5-D6 | Story-specific links preserve timeline year/month; mobile controls; new research form | November 2026 link reload showed one event; editorial approval/publication buttons stayed disabled |
| W5-D7 | Regression tests, legacy taxonomy compatibility, polling/form protection, audit and release | 45 Python and 26 website tests passed locally; CI, merge and deployment recorded in the release follow-up |

## Reader and editorial behavior

The root opens the feed. A story opens at `#/story/<id>`. Year and month live in
its fragment query, so reload and browser navigation preserve the selected view.
Copy view link copies the private URL and never expands its audience. Timeline
and Editorial Review navigation carry the selected story ID. The feed sorts by
latest covered event, with stable ID ordering for ties. Recency uses event dates,
not publication, retrieval or intake timestamps; all-history remains available.

The saved list holds up to 500 story IDs in browser storage. It contains no story
content or credentials. It does not sync accounts/devices and does not provide
offline reading. Disabled or full storage falls back to a temporary in-tab list.
Reader polling avoids the editorial review and a focused feed form.

In Editorial Review, Add another research story accepts the existing structured
source-backed contract with a unique ID and revision context. Saving creates an
unapproved draft. Review and publication remain explicit owner actions. The
site still has only the original real case; synthetic second stories exist only
in isolated automated tests. This release does not claim broader live reporting.

## API compatibility

Existing endpoints default to the original story. `/api/story`, `/api/review`,
`/api/draft`, `/api/publish`, `/api/candidate` and `/api/history[/version]` accept
`?story=<id>` for a selected story. Unknown story reads return 404; malformed IDs
return 400. An older published version remains the reader projection while a
newer draft is edited. Draft creation and audit insert are one database batch.

- `GET /api/feed`: owner-private story summaries and research/publication status;
  never a public feed contract. No review notes, actor identifiers or payloads.
- `POST /api/stories`: authenticated same-origin editor; body `{payload,note}`;
  returns 201 for a new draft, 409 for an existing ID. Service access cannot use it.
- `region` and `category`: optional nonempty strings, at most 80 characters. Old
  stories without them remain valid. The bundled legacy case receives known
  catalogue labels at display time; stored evidence and approval hashes stay intact.

Existing D1 tables already key versions and publications by story. No migration
or rewrite of production story records was needed. Existing source candidates
are a shared intake queue and are attached explicitly to the selected draft.
The Python backend remains a separate runtime; these feed extensions are in the
hosted Worker. The original service status/intake endpoints retain their scope.

## Validation and limits

Local checks: `python -m unittest discover -s tests -q` (45 passed), hosted source
`npm run build` and `npm test` (26 passed). Browser preview verified search with
zero matches, reset, save + saved-only selection, story navigation, timeline
2026/November and link reload, plus new-story form and disabled approval buttons.
No real editorial approval or publication was made. Responsive controls and
wrapping are implemented; physical iOS/Android testing remains pending. The
preview uses an isolated local database and identity, never production records.

The existing seven morning follow-ups remain bounded reliability/intake/fix
runs. They should read this document as well as the historical plan, rather than
rebuilding completed work. Merge/deployment success must be recorded separately
from the local checks above.
