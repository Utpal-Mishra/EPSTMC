BEGIN IMMEDIATE;
CREATE TABLE IF NOT EXISTS story_publications (
    story_id TEXT NOT NULL,
    version INTEGER NOT NULL,
    sequence INTEGER NOT NULL CHECK (sequence > 0),
    kind TEXT NOT NULL CHECK (kind IN ('initial', 'update', 'correction')),
    summary TEXT NOT NULL CHECK (length(trim(summary)) > 0),
    published_at TEXT NOT NULL,
    PRIMARY KEY (story_id, version),
    UNIQUE (story_id, sequence),
    FOREIGN KEY (story_id, version) REFERENCES editorial_versions(story_id, version)
);
CREATE INDEX IF NOT EXISTS publications_feed ON story_publications(published_at, story_id);
CREATE TRIGGER IF NOT EXISTS publication_no_update BEFORE UPDATE ON story_publications
BEGIN SELECT RAISE(ABORT, 'Publish a new approved version to change a story'); END;
CREATE TRIGGER IF NOT EXISTS publication_no_delete BEFORE DELETE ON story_publications
BEGIN SELECT RAISE(ABORT, 'Preserve publication history'); END;
CREATE TRIGGER IF NOT EXISTS publication_approved_only BEFORE INSERT ON story_publications
WHEN NOT EXISTS (SELECT 1 FROM editorial_versions v WHERE v.story_id = NEW.story_id
                 AND v.version = NEW.version AND v.status = 'approved')
BEGIN SELECT RAISE(ABORT, 'Only approved versions may be published'); END;
COMMIT;
