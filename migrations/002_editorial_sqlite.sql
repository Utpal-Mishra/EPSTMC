BEGIN IMMEDIATE;
CREATE TABLE IF NOT EXISTS editorial_evidence (
    id TEXT PRIMARY KEY NOT NULL,
    payload TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS editorial_stories (
    id TEXT PRIMARY KEY NOT NULL,
    latest_version INTEGER NOT NULL CHECK (latest_version > 0)
);
CREATE TABLE IF NOT EXISTS editorial_versions (
    story_id TEXT NOT NULL REFERENCES editorial_stories(id),
    version INTEGER NOT NULL CHECK (version > 0),
    payload TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('draft', 'in_review', 'approved', 'rejected')),
    created_by TEXT NOT NULL,
    created_at TEXT NOT NULL,
    review TEXT,
    reviewed_by TEXT,
    reviewed_at TEXT,
    PRIMARY KEY (story_id, version),
    CHECK (status != 'approved' OR (review IS NOT NULL AND reviewed_by IS NOT NULL AND reviewed_at IS NOT NULL))
);
CREATE TABLE IF NOT EXISTS editorial_events (
    id INTEGER PRIMARY KEY,
    story_id TEXT NOT NULL,
    version INTEGER NOT NULL,
    action TEXT NOT NULL,
    actor TEXT NOT NULL,
    note TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (story_id, version) REFERENCES editorial_versions(story_id, version)
);
CREATE TRIGGER IF NOT EXISTS editorial_payload_immutable
BEFORE UPDATE OF payload, content_hash, story_id, version, created_by, created_at ON editorial_versions
BEGIN SELECT RAISE(ABORT, 'Create a new version to change editorial content'); END;
CREATE TRIGGER IF NOT EXISTS editorial_final_immutable
BEFORE UPDATE ON editorial_versions WHEN OLD.status IN ('approved', 'rejected')
BEGIN SELECT RAISE(ABORT, 'Final review records are immutable'); END;
CREATE TRIGGER IF NOT EXISTS editorial_version_no_delete
BEFORE DELETE ON editorial_versions BEGIN SELECT RAISE(ABORT, 'Preserve editorial versions'); END;
CREATE TRIGGER IF NOT EXISTS editorial_event_no_update
BEFORE UPDATE ON editorial_events BEGIN SELECT RAISE(ABORT, 'Preserve editorial audit events'); END;
CREATE TRIGGER IF NOT EXISTS editorial_event_no_delete
BEFORE DELETE ON editorial_events BEGIN SELECT RAISE(ABORT, 'Preserve editorial audit events'); END;
CREATE TRIGGER IF NOT EXISTS editorial_evidence_no_update
BEFORE UPDATE ON editorial_evidence BEGIN SELECT RAISE(ABORT, 'Register a new evidence ID'); END;
CREATE TRIGGER IF NOT EXISTS editorial_evidence_no_delete
BEFORE DELETE ON editorial_evidence BEGIN SELECT RAISE(ABORT, 'Preserve registered evidence'); END;
COMMIT;
