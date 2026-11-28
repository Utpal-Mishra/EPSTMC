# WEB-09 — Align timeline filters

Planned: 2026-11-28. Implemented: 2026-11-28. Record date: 2026-11-28.

Scope: the Year and Month dropdowns and the Reset filters and Copy view link buttons in the story timeline. The shared toolbar centers buttons against the complete label and select groups, which places their edges above the selects.

Dependencies: existing timeline controls in `web/worker/ui.js` and the existing private Site deployment workflow.

Acceptance: align the control edges and heights on wide screens, keep the controls within the viewport on narrow screens, and preserve filter and link behavior.

Implementation: `web/worker/ui.js` scopes layout rules to the timeline filters and places the two dropdowns above the action buttons on narrow screens. The source change is in the GitHub commit with subject `WEB-09 Align story timeline filter controls`. The equivalent hosted source commit is `752d14ce85c36cf4104268ffd189fea7ce51af57`.

Evidence: the Worker build and all 93 website tests passed. The local browser measured identical 44 px control heights with matching top and bottom edges at a 1,348 px viewport. Selecting a year updated the story view, Reset filters cleared the selection, and Copy view link reported success.

Status: implemented and locally validated. Responsive browser verification and deployment are recorded in WEB-09-QA and WEB-09-REL in the traceability register.

Rollback: revert the dedicated layout commit or redeploy private Site version 9. No data migration is needed.
