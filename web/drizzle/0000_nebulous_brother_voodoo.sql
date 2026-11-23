CREATE TABLE `htp_audit` (
	`id` text PRIMARY KEY NOT NULL,
	`story_id` text,
	`version` integer,
	`action` text NOT NULL,
	`actor` text NOT NULL,
	`note` text NOT NULL,
	`created_at` text NOT NULL
);
--> statement-breakpoint
CREATE TABLE `htp_evidence` (
	`id` text PRIMARY KEY NOT NULL,
	`source_id` text NOT NULL,
	`fingerprint` text NOT NULL,
	`metadata` text NOT NULL,
	`first_retrieved_at` text NOT NULL,
	`last_retrieved_at` text NOT NULL,
	`state` text DEFAULT 'pending' NOT NULL
);
--> statement-breakpoint
CREATE UNIQUE INDEX `htp_evidence_revision` ON `htp_evidence` (`source_id`,`fingerprint`);--> statement-breakpoint
CREATE TABLE `htp_publications` (
	`story_id` text NOT NULL,
	`version` integer NOT NULL,
	`sequence` integer NOT NULL,
	`kind` text NOT NULL,
	`summary` text NOT NULL,
	`published_at` text NOT NULL,
	`token` text NOT NULL,
	PRIMARY KEY(`story_id`, `version`)
);
--> statement-breakpoint
CREATE UNIQUE INDEX `htp_publication_sequence` ON `htp_publications` (`story_id`,`sequence`);--> statement-breakpoint
CREATE TABLE `htp_runs` (
	`id` text PRIMARY KEY NOT NULL,
	`attempt_at` text NOT NULL,
	`completed_at` text,
	`status` text NOT NULL,
	`count` integer DEFAULT 0 NOT NULL,
	`detail` text
);
--> statement-breakpoint
CREATE TABLE `htp_stories` (
	`id` text PRIMARY KEY NOT NULL,
	`latest` integer DEFAULT 1 NOT NULL
);
--> statement-breakpoint
CREATE TABLE `htp_versions` (
	`story_id` text NOT NULL,
	`version` integer NOT NULL,
	`payload` text NOT NULL,
	`hash` text NOT NULL,
	`status` text DEFAULT 'draft' NOT NULL,
	`created_by` text NOT NULL,
	`created_at` text NOT NULL,
	`review` text,
	`reviewed_by` text,
	`changed_token` text NOT NULL,
	PRIMARY KEY(`story_id`, `version`)
);
