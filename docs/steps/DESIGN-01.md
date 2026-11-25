# DESIGN-01 — Selected editorial design

Planned and recorded: 25 November 2026 (Europe/Dublin). Actual implementation: pending. Status: PLANNED.

Scope and acceptance: see STEP_TRACEABILITY.md. Dependencies: private v7 website; NEWS-02 depends on NEWS-01 and DESIGN-01; REL-09 depends on all three.

Evidence and implementation: pending. Per-step implementation commit retains the step ID.

Recovery: revert the bounded code step; preserve story history and editorial gates. New ingestion storage is additive. No schedule or audience change. Provider activation, publication and exhaustive coverage are not implied.

## Implementation — 25 November 2026

Restored the selected reference direction with self-hosted Playfair Display and DM Sans, warm editorial surfaces, restrained terracotta controls, visual-edition/timeline components and navy/mint market styling. Fonts are served from the same origin under CSP. Files: web/worker/editorial-design.js, fonts.js, site-assets.js, ui.js, index.js; docs/FONT_LICENSES.md. Reference inspected: EPSTMC_Selected_Design.png. No fictional oil-price data or headlines from the sample are carried into production. Browser verification follows the integrated NEWS-02 implementation. Rollback: revert this bounded styling step; no content mutation. Status: IMPLEMENTED, integrated visual QA pending.

Integrated preview evidence (NEWS-02): self-hosted font requests rendered successfully; computed headline font Playfair Display and body font DM Sans; visual edition, warm cards, Timeline Journal and navy/mint chart inspected in browser. Responsive CSS includes narrow single-column layouts; physical devices not tested.
