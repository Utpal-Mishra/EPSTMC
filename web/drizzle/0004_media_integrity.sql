CREATE INDEX htp_media_story_version ON htp_media(story_id, version, status);
--> statement-breakpoint
CREATE INDEX htp_media_created ON htp_media(created_at, method);
--> statement-breakpoint
CREATE INDEX htp_feedback_story ON htp_feedback(story_id, created_at);
--> statement-breakpoint
CREATE TRIGGER htp_media_reference BEFORE INSERT ON htp_media
WHEN NOT EXISTS (SELECT 1 FROM htp_versions WHERE story_id=NEW.story_id AND version=NEW.version AND hash=NEW.story_hash)
BEGIN SELECT RAISE(ABORT, 'Media requires an existing matching story version'); END;
--> statement-breakpoint
CREATE TRIGGER htp_media_immutable BEFORE UPDATE ON htp_media
WHEN OLD.status IN ('ready','rejected') AND (
 NEW.story_id IS NOT OLD.story_id OR NEW.version IS NOT OLD.version OR NEW.story_hash IS NOT OLD.story_hash OR
 NEW.script_hash IS NOT OLD.script_hash OR NEW.metadata IS NOT OLD.metadata OR NEW.object_key IS NOT OLD.object_key OR
 NEW.mime IS NOT OLD.mime OR NEW.size IS NOT OLD.size OR NEW.kind IS NOT OLD.kind OR NEW.method IS NOT OLD.method OR
 NEW.request_key IS NOT OLD.request_key OR NEW.created_by IS NOT OLD.created_by OR NEW.created_at IS NOT OLD.created_at)
BEGIN SELECT RAISE(ABORT, 'Released media content is immutable'); END;
