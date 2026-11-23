CREATE TRIGGER htp_payload_immutable BEFORE UPDATE OF payload,hash,story_id,version,created_by,created_at ON htp_versions BEGIN SELECT RAISE(ABORT,'Create a new draft to change content'); END;
--> statement-breakpoint
CREATE TRIGGER htp_final_immutable BEFORE UPDATE ON htp_versions WHEN OLD.status IN ('approved','rejected') BEGIN SELECT RAISE(ABORT,'Final review is immutable'); END;
--> statement-breakpoint
CREATE TRIGGER htp_status_transition BEFORE UPDATE OF status ON htp_versions WHEN NOT ((OLD.status='draft' AND NEW.status='in_review') OR (OLD.status='in_review' AND NEW.status IN ('approved','rejected'))) BEGIN SELECT RAISE(ABORT,'Invalid review transition'); END;
--> statement-breakpoint
CREATE TRIGGER htp_versions_no_delete BEFORE DELETE ON htp_versions BEGIN SELECT RAISE(ABORT,'Preserve version history'); END;
--> statement-breakpoint
CREATE TRIGGER htp_publication_approved BEFORE INSERT ON htp_publications WHEN NOT EXISTS(SELECT 1 FROM htp_versions WHERE story_id=NEW.story_id AND version=NEW.version AND status='approved') BEGIN SELECT RAISE(ABORT,'Only approved versions may be published'); END;
--> statement-breakpoint
CREATE TRIGGER htp_publication_no_update BEFORE UPDATE ON htp_publications BEGIN SELECT RAISE(ABORT,'Preserve publications'); END;
--> statement-breakpoint
CREATE TRIGGER htp_publication_no_delete BEFORE DELETE ON htp_publications BEGIN SELECT RAISE(ABORT,'Preserve publications'); END;
--> statement-breakpoint
CREATE TRIGGER htp_audit_no_update BEFORE UPDATE ON htp_audit BEGIN SELECT RAISE(ABORT,'Preserve audit events'); END;
--> statement-breakpoint
CREATE TRIGGER htp_audit_no_delete BEFORE DELETE ON htp_audit BEGIN SELECT RAISE(ABORT,'Preserve audit events'); END;
--> statement-breakpoint
CREATE TRIGGER htp_evidence_snapshot BEFORE UPDATE OF id,source_id,fingerprint,metadata,first_retrieved_at ON htp_evidence BEGIN SELECT RAISE(ABORT,'Evidence changes require a new fingerprint'); END;
