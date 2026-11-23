"""Private editorial queue, evidence attachments and immutable story versions."""

import argparse
from contextlib import contextmanager
from datetime import date, datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3

from brief import render_brief, required_text

IDENTIFIER = re.compile(r"[a-z0-9][a-z0-9-]{0,119}")


def now():
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def encode(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def fingerprint(payload):
    return hashlib.sha256(encode(payload).encode("utf-8")).hexdigest()


def identifier(value):
    if not isinstance(value, str) or not IDENTIFIER.fullmatch(value):
        raise ValueError("IDs require 1–120 lowercase letters, digits or hyphens")
    return value


class Store:
    def __init__(self, db, postgres=False):
        self.db = db
        self.postgres = postgres
        self.prefix = "epstmc." if postgres else ""

    def execute(self, sql, params=()):
        sql = sql.replace("{schema}", self.prefix)
        if self.postgres:
            sql = sql.replace("?", "%s")
        return self.db.execute(sql, params)

    @contextmanager
    def transaction(self):
        if self.postgres:
            with self.db.transaction():
                yield
        else:
            with self.db:
                self.db.execute("BEGIN IMMEDIATE")
                yield

    def lock_story(self, story_id, expected_version):
        suffix = " FOR UPDATE" if self.postgres else ""
        row = self.execute(
            "SELECT latest_version FROM {schema}editorial_stories WHERE id = ?" + suffix,
            (story_id,),
        ).fetchone()
        if row is None:
            raise ValueError("Unknown story")
        if row["latest_version"] != expected_version:
            raise ValueError("Stale version: reload the latest story before changing it")

    def event(self, story_id, version, action, actor, note):
        self.execute(
            "INSERT INTO {schema}editorial_events "
            "(story_id, version, action, actor, note, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (story_id, version, action, actor, note, now()),
        )

    def evidence(self, source_id):
        if source_id.startswith("fr-"):
            row = self.execute(
                "SELECT * FROM {schema}federal_register_evidence WHERE id = ?", (source_id,)
            ).fetchone()
            if row is None:
                raise ValueError(f"Import Federal Register evidence first: {source_id}")
            result = dict(row)
            for field, value in result.items():
                if isinstance(value, datetime):
                    result[field] = value.astimezone(timezone.utc).isoformat(timespec="microseconds")
                elif isinstance(value, date):
                    result[field] = value.isoformat()
            return result
        row = self.execute(
            "SELECT payload FROM {schema}editorial_evidence WHERE id = ?", (source_id,)
        ).fetchone()
        if row is None:
            raise ValueError(f"Register historical evidence first: {source_id}")
        return json.loads(row["payload"])

    def attach(self, payload):
        if not isinstance(payload, dict):
            raise ValueError("Draft must be a JSON object")
        supplied = payload.get("sources")
        if not isinstance(supplied, list) or not supplied:
            raise ValueError("Draft requires a sources list")
        result = dict(payload)
        result["sources"] = [self.evidence(identifier(required_text(s, "id"))) for s in supplied]
        validate_draft(result)
        return result

    def register_evidence(self, source, actor, note):
        source_id = identifier(required_text(source, "id"))
        if source_id.startswith("fr-"):
            raise ValueError("fr- IDs are reserved for the Federal Register importer")
        # Reuse URL and title validation; registration records provenance, not verification.
        render_brief({"title": "Evidence", "sources": [source], "facts": [
            {"text": "Registration", "source_ids": [source_id]}], "history": [], "scenarios": []})
        publication = date.fromisoformat(required_text(source, "publication_date")).isoformat()
        record = {"id": source_id, "title": required_text(source, "title"),
                  "url": required_text(source, "url"), "publication_date": publication,
                  "publisher": required_text(source, "publisher"),
                  "registered_at": now(), "registered_by": actor, "registration_note": note}
        with self.transaction():
            if self.execute("SELECT id FROM {schema}editorial_evidence WHERE id = ?", (source_id,)).fetchone():
                raise ValueError("Evidence ID already exists; register a new ID for changed evidence")
            self.execute("INSERT INTO {schema}editorial_evidence (id, payload) VALUES (?, ?)",
                         (source_id, encode(record)))
        return record

    def create(self, story_id, payload, actor, note, expected_version=None):
        identifier(story_id)
        with self.transaction():
            if expected_version is None:
                if self.execute("SELECT id FROM {schema}editorial_stories WHERE id = ?", (story_id,)).fetchone():
                    raise ValueError("Story exists; use revise with its latest version")
                version = 1
                self.execute("INSERT INTO {schema}editorial_stories (id, latest_version) VALUES (?, ?)",
                             (story_id, version))
            else:
                self.lock_story(story_id, expected_version)
                version = expected_version + 1
                self.execute("UPDATE {schema}editorial_stories SET latest_version = ? WHERE id = ?",
                             (version, story_id))
            attached = self.attach(payload)
            self.execute(
                "INSERT INTO {schema}editorial_versions "
                "(story_id, version, payload, content_hash, status, created_by, created_at) "
                "VALUES (?, ?, ?, ?, 'draft', ?, ?)",
                (story_id, version, encode(attached), fingerprint(attached), actor, now()),
            )
            self.event(story_id, version, "created" if version == 1 else "revised", actor, note)
        return self.get(story_id, version)

    def get(self, story_id, version):
        row = self.execute(
            "SELECT * FROM {schema}editorial_versions WHERE story_id = ? AND version = ?",
            (story_id, version),
        ).fetchone()
        if row is None:
            raise ValueError("Unknown story version")
        result = dict(row)
        result["payload"] = json.loads(result["payload"])
        result["review"] = json.loads(result["review"]) if result["review"] else None
        return result

    def transition(self, story_id, version, action, actor, note, review=None):
        states = {"submit": ("draft", "in_review"), "approve": ("in_review", "approved"),
                  "reject": ("in_review", "rejected")}
        before, after = states[action]
        with self.transaction():
            self.lock_story(story_id, version)
            current = self.get(story_id, version)
            if current["status"] != before:
                raise ValueError(f"{action} requires status {before}")
            validate_draft(current["payload"])
            if fingerprint(current["payload"]) != current["content_hash"]:
                raise ValueError("Content hash mismatch")
            if action == "approve":
                validate_review(current["payload"], review)
            self.execute(
                "UPDATE {schema}editorial_versions SET status = ?, review = ?, "
                "reviewed_by = ?, reviewed_at = ? WHERE story_id = ? AND version = ?",
                (after, encode(review) if action == "approve" else None,
                 actor if action != "submit" else None,
                 now() if action != "submit" else None, story_id, version),
            )
            self.event(story_id, version, action, actor, note)
        return self.get(story_id, version)

    def queue(self, status):
        rows = self.execute(
            "SELECT v.story_id, v.version, v.status, v.created_by, v.created_at "
            "FROM {schema}editorial_versions v JOIN {schema}editorial_stories s "
            "ON s.id = v.story_id AND s.latest_version = v.version "
            "WHERE v.status = ? ORDER BY v.created_at, v.story_id", (status,),
        ).fetchall()
        return [dict(row) for row in rows]

    def history(self, story_id):
        versions = self.execute(
            "SELECT version FROM {schema}editorial_versions WHERE story_id = ? ORDER BY version",
            (story_id,),
        ).fetchall()
        events = self.execute(
            "SELECT version, action, actor, note, created_at FROM {schema}editorial_events "
            "WHERE story_id = ? ORDER BY id", (story_id,),
        ).fetchall()
        return {"versions": [self.get(story_id, r["version"]) for r in versions],
                "events": [dict(row) for row in events]}


def validate_draft(payload):
    render_brief(payload)
    for section in ("history", "scenarios"):
        if not payload[section]:
            raise ValueError(f"Week 3 drafts require at least one {section} item")
    for source in payload["sources"]:
        date.fromisoformat(required_text(source, "publication_date"))
    for item in payload["history"]:
        required_text(item, "comparison")
        required_text(item, "limitations")
    for item in payload["scenarios"]:
        required_text(item, "timeframe")


def validate_review(payload, review):
    if not isinstance(review, dict) or review.get("evidence_checked") is not True:
        raise ValueError("Approval requires evidence_checked: true after human source review")
    required_text(review, "assessment")
    checked = review.get("checked_source_ids")
    expected = {source["id"] for source in payload["sources"]}
    if not isinstance(checked, list) or any(not isinstance(x, str) for x in checked) or set(checked) != expected:
        raise ValueError("Approval must record every attached source ID")
    if review.get("scenarios_are_conditional") is not True:
        raise ValueError("Approval requires confirmation that scenarios are conditional")


@contextmanager
def open_store(path=None, postgres=False):
    if postgres:
        dsn = os.getenv("EPSTMC_DATABASE_URL")
        if not dsn:
            raise ValueError("EPSTMC_DATABASE_URL must be set for --postgres")
        try:
            import psycopg
            from psycopg.rows import dict_row
        except ImportError:
            raise ValueError("Install requirements-postgres.txt for Postgres support") from None
        try:
            with psycopg.connect(dsn, connect_timeout=10, autocommit=True, row_factory=dict_row) as db:
                yield Store(db, postgres=True)
        except psycopg.errors.UndefinedTable:
            raise ValueError("Apply migrations 001 and 002 before editorial commands") from None
        except psycopg.Error as exc:
            raise ValueError(f"Postgres operation failed ({type(exc).__name__})") from None
    else:
        db = sqlite3.connect(path)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys = ON")
        try:
            yield Store(db)
        finally:
            db.close()


def init_sqlite(store):
    store.db.executescript(Path(__file__).with_name("migrations").joinpath(
        "002_editorial_sqlite.sql").read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    storage = parser.add_mutually_exclusive_group(required=True)
    storage.add_argument("--db", type=Path)
    storage.add_argument("--postgres", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init", help="Initialize local SQLite editorial tables")
    register = sub.add_parser("add-evidence", help="Register dated historical source metadata")
    register.add_argument("file", type=Path)
    for name in ("create", "revise", "submit", "approve", "reject", "show", "history"):
        command = sub.add_parser(name)
        command.add_argument("story")
        if name not in ("create", "history"):
            command.add_argument("--version", type=int, required=True)
        if name in ("create", "revise"):
            command.add_argument("file", type=Path)
        if name == "approve":
            command.add_argument("--review", type=Path, required=True)
        if name == "show":
            command.add_argument("--markdown", action="store_true")
        if name not in ("show", "history"):
            command.add_argument("--actor", required=True)
            command.add_argument("--note", required=True)
    register.add_argument("--actor", required=True)
    register.add_argument("--note", required=True)
    queue = sub.add_parser("queue")
    queue.add_argument("--status", choices=("draft", "in_review", "approved", "rejected"), default="in_review")
    args = parser.parse_args()
    try:
        if hasattr(args, "actor"):
            required_text(vars(args), "actor")
            required_text(vars(args), "note")
        if hasattr(args, "version") and args.version < 1:
            raise ValueError("version must be positive")
        with open_store(args.db, args.postgres) as store:
            if args.command == "init":
                if args.postgres:
                    raise ValueError("Use migrations/002_editorial_postgres.sql as schema owner")
                init_sqlite(store)
                output = {"initialized": True}
            elif args.command == "add-evidence":
                output = store.register_evidence(json.loads(args.file.read_text(encoding="utf-8")), args.actor, args.note)
            elif args.command in ("create", "revise"):
                output = store.create(args.story, json.loads(args.file.read_text(encoding="utf-8")),
                                      args.actor, args.note, getattr(args, "version", None))
            elif args.command in ("submit", "approve", "reject"):
                review = json.loads(args.review.read_text(encoding="utf-8")) if args.command == "approve" else None
                output = store.transition(args.story, args.version, args.command, args.actor, args.note, review)
            elif args.command == "queue":
                output = store.queue(args.status)
            elif args.command == "history":
                output = store.history(args.story)
            else:
                output = store.get(args.story, args.version)
                if args.markdown:
                    print(f"Editorial preview — {output['status']} — version {args.version}\n")
                    print(render_brief(output["payload"]))
                    return
        print(json.dumps(output, indent=2, ensure_ascii=False))
    except (OSError, ValueError, KeyError, TypeError, AttributeError, sqlite3.Error) as exc:
        parser.exit(1, f"Editorial operation failed: {exc}\n")


if __name__ == "__main__":
    main()
