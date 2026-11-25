CREATE TABLE `regional_market` (
	`id` text PRIMARY KEY NOT NULL,
	`payload` text NOT NULL
);
--> statement-breakpoint
CREATE TABLE `regional_news` (
	`id` text PRIMARY KEY NOT NULL,
	`source_id` text NOT NULL,
	`published_at` text NOT NULL,
	`payload` text NOT NULL
);
--> statement-breakpoint
CREATE TABLE `regional_refresh` (
	`id` integer PRIMARY KEY NOT NULL,
	`last_attempt` text NOT NULL
);
--> statement-breakpoint
CREATE TABLE `regional_source_status` (
	`id` text PRIMARY KEY NOT NULL,
	`status` text NOT NULL,
	`last_attempt` text,
	`last_success` text,
	`item_count` integer DEFAULT 0 NOT NULL,
	`error` text
);
