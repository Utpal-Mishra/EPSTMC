CREATE TABLE `htp_feedback` (
	`id` text PRIMARY KEY NOT NULL,
	`story_id` text NOT NULL,
	`version` integer NOT NULL,
	`category` text NOT NULL,
	`message` text NOT NULL,
	`source_url` text,
	`state` text DEFAULT 'pending' NOT NULL,
	`resolution` text,
	`created_at` text NOT NULL,
	`resolved_at` text
);
--> statement-breakpoint
CREATE TABLE `htp_media` (
	`id` text PRIMARY KEY NOT NULL,
	`story_id` text NOT NULL,
	`version` integer NOT NULL,
	`story_hash` text NOT NULL,
	`script_hash` text NOT NULL,
	`kind` text NOT NULL,
	`method` text NOT NULL,
	`status` text NOT NULL,
	`metadata` text DEFAULT '{}' NOT NULL,
	`object_key` text,
	`mime` text,
	`size` integer,
	`attempts` integer DEFAULT 0 NOT NULL,
	`error` text,
	`created_by` text NOT NULL,
	`created_at` text NOT NULL,
	`updated_at` text NOT NULL,
	`reviewed_by` text,
	`review_note` text,
	`request_key` text NOT NULL
);
--> statement-breakpoint
CREATE UNIQUE INDEX `htp_media_request` ON `htp_media` (`story_id`,`request_key`);--> statement-breakpoint
CREATE TABLE `htp_metrics` (
	`day` text NOT NULL,
	`story_id` text NOT NULL,
	`version` integer NOT NULL,
	`event` text NOT NULL,
	`count` integer DEFAULT 0 NOT NULL,
	PRIMARY KEY(`day`, `story_id`, `version`, `event`)
);
