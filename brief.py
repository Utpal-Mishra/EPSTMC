"""Render an evidence-linked news brief from an editorial JSON file."""

import argparse
import json
from pathlib import Path
from urllib.parse import urlsplit


def required_text(record, field):
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def render_brief(brief):
    lines = [f"# {required_text(brief, 'title')}"]
    sources = {}
    for source in brief["sources"]:
        source_id = required_text(source, "id")
        if source_id in sources:
            raise ValueError(f"Duplicate source ID: {source_id}")
        url = required_text(source, "url")
        parsed = urlsplit(url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            raise ValueError(f"Source {source_id} requires an HTTP(S) URL")
        try:
            # urlsplit validates the port when it is accessed.
            _ = parsed.port
        except ValueError as exc:
            raise ValueError(f"Source {source_id} has an invalid URL port") from exc
        sources[source_id] = (required_text(source, "title"), url)

    for field, heading in (
        ("facts", "What happened"),
        ("history", "Historical context"),
        ("scenarios", "What could happen next"),
    ):
        items = brief[field]
        if not isinstance(items, list) or (field == "facts" and not items):
            raise ValueError(f"{field} must be a list with at least one item for facts")
        if not items:
            continue
        lines.extend(("", f"## {heading}", ""))
        for item in items:
            text = required_text(item, "text")
            refs = item.get("source_ids")
            if not isinstance(refs, list) or not refs:
                raise ValueError(f"Each {field} item requires source_ids")
            for ref in refs:
                if not isinstance(ref, str) or ref not in sources:
                    raise ValueError(f"Unknown source ID: {ref!r}")
            citations = ", ".join(f"[{ref}]" for ref in refs)
            if field == "scenarios":
                condition = required_text(item, "condition")
                signal = required_text(item, "signal")
                lines.append(f"- If {condition}, {text} Evidence: {citations}. Watch for {signal}.")
            else:
                lines.append(f"- {text} {citations}")

    lines.extend(("", "## Sources", ""))
    for source_id, (title, url) in sources.items():
        lines.append(f"- [{source_id}] {title} — {url}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief", type=Path)
    args = parser.parse_args()
    try:
        output = render_brief(json.loads(args.brief.read_text(encoding="utf-8")))
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        parser.exit(2, f"Invalid brief: {exc}\n")
    print(output)


if __name__ == "__main__":
    main()
