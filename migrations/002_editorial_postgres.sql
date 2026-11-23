BEGIN;
CREATE SCHEMA IF NOT EXISTS epstmc;
CREATE TABLE IF NOT EXISTS epstmc.editorial_evidence (
    id TEXT PRIMARY KEY NOT NULL,
    payload TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS epstmc.editorial_stories (
    id TEXT PRIMARY KEY NOT NULL,
    latest_version INTEGER NOT NULL CHECK (latest_version > 0)
);
CREATE TABLE IF NOT EXISTS epstmc.editorial_versions (
    story_id TEXT NOT NULL REFERENCES epstmc.editorial_stories(id),
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
CREATE TABLE IF NOT EXISTS epstmc.editorial_events (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    story_id TEXT NOT NULL,
    version INTEGER NOT NULL,
    action TEXT NOT NULL,
    actor TEXT NOT NULL,
    note TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (story_id, version) REFERENCES epstmc.editorial_versions(story_id, version)
);
CREATE OR REPLACE FUNCTION epstmc.guard_editorial_version() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        RAISE EXCEPTION 'Preserve editorial versions';
    END IF;
    IF OLD.status IN ('approved', 'rejected') OR
       (NEW.story_id, NEW.version, NEW.payload, NEW.content_hash, NEW.created_by, NEW.created_at)
       IS DISTINCT FROM
       (OLD.story_id, OLD.version, OLD.payload, OLD.content_hash, OLD.created_by, OLD.created_at) THEN
        RAISE EXCEPTION 'Create a new version to change editorial content';
    END IF;
    RETURN NEW;
END;
$$;
DROP TRIGGER IF EXISTS editorial_version_guard ON epstmc.editorial_versions;
CREATE TRIGGER editorial_version_guard BEFORE UPDATE OR DELETE ON epstmc.editorial_versions
FOR EACH ROW EXECUTE FUNCTION epstmc.guard_editorial_version();
CREATE OR REPLACE FUNCTION epstmc.guard_editorial_append_only() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
    RAISE EXCEPTION 'Preserve editorial audit and evidence records';
END;
$$;
DROP TRIGGER IF EXISTS editorial_events_guard ON epstmc.editorial_events;
CREATE TRIGGER editorial_events_guard BEFORE UPDATE OR DELETE ON epstmc.editorial_events
FOR EACH ROW EXECUTE FUNCTION epstmc.guard_editorial_append_only();
DROP TRIGGER IF EXISTS editorial_evidence_guard ON epstmc.editorial_evidence;
CREATE TRIGGER editorial_evidence_guard BEFORE UPDATE OR DELETE ON epstmc.editorial_evidence
FOR EACH ROW EXECUTE FUNCTION epstmc.guard_editorial_append_only();
COMMIT;
