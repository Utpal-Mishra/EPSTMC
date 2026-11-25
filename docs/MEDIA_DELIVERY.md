# EPSTMC pending work and media delivery

## Planning snapshot (superseded by accelerated implementation)

As of 24 November 2026. This is a delivery plan, not evidence of implemented media or a scheduled background build. Dates are proposed targets conditional on implementation sessions and prerequisite checks.

## Verified baseline and pending work

- Refreshed origin/main is 4863d32 (freshness documentation PR #4 merged).
- The history-to-present website, durable D1 data, source intake and protected editorial workflow are integrated. Latest recorded live verification: 24 November morning; no new live check performed for this plan.
- Website expansion W5-D1–D7 exists locally at ccd8508 on codex/next-phase. Multi-story feed, region/category filters, search, event-date windows, browser saved list and story deep links are implemented locally. Integration into current main, fresh release checks and deployment remain pending; do not describe them as live.
- Review candidate relevance, research coverage gaps and obtain actual owner editorial review. A successful source search does not verify story claims.
- Physical-device QA, native apps, full offline reading and push alerts remain open.
- No audio generation/player, image-with-content delivery pipeline or video explainer pipeline was found in the inspected hosted implementation.

## Proposed delivery targets

| Window (Europe/Dublin) | Deliverable | Exit check |
| --- | --- | --- |
| 25–26 November | Integrate and release existing website expansion; define shared media records and storage route | Reconcile latest main without losing freshness records; required CI passes; verify deployed feed and story isolation. Record media version, status and storage decisions. |
| 27–28 November | Image + content first slice | One reviewed story has a relevant rights-cleared or clearly labelled illustrative image, caption, alt text, credit and source links; mobile layout and missing-image fallback work. |
| 29–30 November | Audio listening first slice | Generate narration from one frozen reviewed script; provide play/pause, seek, speed and transcript; verify mobile playback, generation failure and stale-version behavior. |
| 1–4 December | Short video explainer pilot | One 60–90 second explainer with evidence-backed script, illustrative visuals, captions, narration, poster and accessible text fallback. Review rendered output before release. |
| 5–7 December | Media reliability and broader rollout | Verify version corrections, retries, cost limits, access boundaries, device behavior and honest availability states across formats. |

Before December target: image-with-content and one working audio pilot. Video is a following pilot; all formats are not promised production-ready by 30 November.

## Reader experience and content rules

A story offers Read, Listen and Watch only as each format becomes ready. Read includes image, context, sources and timeline. Listen explains the same current event, historical context and conditional scenarios. Watch provides an accessible visual explanation rather than just reading a headline. Interpret “understanding via video” here as reader-facing explainers; automatic analysis of uploaded video is a separate, unscheduled feature.

Each asset references story ID, immutable story version and approved script/content hash. Record type, status (queued/generating/review/ready/failed/stale), location, generation method, credits/rights, disclosure, duration or alt text, timestamps and reviewer decision. A corrected story flags older media as stale; no silent presentation as current. Reuse shared story facts across formats, but review each rendered asset. Private previews remain private and visibly unapproved. Never invent review attestations.

Use generated visuals only as labelled illustrations. Use exact plotting/rendering for factual diagrams and charts. Keep captions and transcripts available; no autoplay. Hide unavailable controls or explain the pending state. Provider choice, credentials, durable object storage, playback access and actual costs remain unresolved; no service purchase or provisioning is claimed.

## Immediate next task

Integrate the existing website expansion with current main, run release checks and verify the private deployment. Then implement the media data/storage contract and one image-backed story before adding narration. Existing daily reliability runs are unchanged by this document; no additional automation was created.

## Accelerated implementation — 24 November 2026

The owner subsequently requested development and integration of the full two-week scope in the current session. See MEDIA_INTEGRATIONS.md and the release entry in DAILY_DEVELOPMENT.md. The dates above remain original targets, not backdated completions. Provider activation, real editorial approval and physical-device QA remain distinct.
