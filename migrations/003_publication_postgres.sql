BEGIN;
CREATE TABLE IF NOT EXISTS epstmc.story_publications (
    story_id TEXT NOT NULL,
    version INTEGER NOT NULL,
    sequence INTEGER NOT NULL CHECK (sequence > 0),
    kind TEXT NOT NULL CHECK (kind IN ('initial', 'update', 'correction')),
    summary TEXT NOT NULL CHECK (length(trim(summary)) > 0),
    published_at TEXT NOT NULL,
    PRIMARY KEY (story_id, version),
    UNIQUE (story_id, sequence),
    FOREIGN KEY (story_id, version) REFERENCES epstmc.editorial_versions(story_id, version)
);
CREATE INDEX IF NOT EXISTS publications_feed ON epstmc.story_publications(published_at, story_id);
DROP TRIGGER IF EXISTS publication_immutable ON epstmc.story_publications;
CREATE TRIGGER publication_immutable BEFORE UPDATE OR DELETE ON epstmc.story_publications
FOR EACH ROW EXECUTE FUNCTION epstmc.guard_editorial_append_only();
CREATE OR REPLACE FUNCTION epstmc.guard_publication_approval() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM epstmc.editorial_versions v WHERE v.story_id = NEW.story_id
                   AND v.version = NEW.version AND v.status = 'approved') THEN
        RAISE EXCEPTION 'Only approved versions may be published';
    END IF;
    RETURN NEW;
END;
$$;
DROP TRIGGER IF EXISTS publication_approved_only ON epstmc.story_publications;
CREATE TRIGGER publication_approved_only BEFORE INSERT ON epstmc.story_publications
FOR EACH ROW EXECUTE FUNCTION epstmc.guard_publication_approval();
COMMIT;
