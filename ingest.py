"""Collect U.S. AI infrastructure and policy documents for editorial review."""

import argparse
from contextlib import closing
from datetime import date, datetime, timezone
import json
from pathlib import Path
import re
import sqlite3
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen

from brief import required_text

API = "https://www.federalregister.gov/api/v1/documents"
DEFAULT_QUERY = '"artificial intelligence infrastructure"'
DOCUMENT_NUMBER = re.compile(r"[A-Za-z0-9]+(?:-[A-Za-z0-9]+)+")
RETRYABLE_STATUS = {500, 502, 503, 504}


def fetch_json(url):
    request = Request(url, headers={
        "Accept": "application/json",
        "User-Agent": "EPSTMC/0.1 (+https://github.com/Utpal-Mishra/EPSTMC)",
    })
    for attempt in range(3):
        try:
            with urlopen(request, timeout=15) as response:
                return json.load(response)
        except HTTPError as exc:
            exc.close()
            if exc.code not in RETRYABLE_STATUS or attempt == 2:
                raise
        except (URLError, TimeoutError):
            if attempt == 2:
                raise
        time.sleep(2 ** attempt)


def normalize_document(document):
    number = required_text(document, "document_number")
    if not DOCUMENT_NUMBER.fullmatch(number):
        raise ValueError(f"Invalid Federal Register document number: {number!r}")
    url = required_text(document, "html_url")
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.netloc not in {
        "www.federalregister.gov", "federalregister.gov",
    }:
        raise ValueError(f"Unexpected Federal Register document URL: {url}")
    return {
        "id": f"fr-{number}",
        "document_number": number,
        "title": required_text(document, "title"),
        "url": url,
        "publication_date": date.fromisoformat(
            required_text(document, "publication_date")
        ).isoformat(),
        "document_type": required_text(document, "type"),
        "official_pdf_url": document.get("pdf_url"),
    }


def collect_documents(document_number, query, limit):
    if document_number:
        document = normalize_document(fetch_json(f"{API}/{document_number}.json"))
        if document["document_number"] != document_number:
            raise ValueError("Federal Register returned a different document number")
        return [document]

    params = urlencode({
        "conditions[term]": query,
        "per_page": limit,
        "order": "newest",
    })
    payload = fetch_json(f"{API}.json?{params}")
    results = payload.get("results", [] if payload.get("count") == 0 else None)
    if not isinstance(results, list):
        raise ValueError("Federal Register results must be a list")
    return [normalize_document(document) for document in results]


def store_documents(db, documents):
    with db:
        db.execute("BEGIN IMMEDIATE")
        retrieved_at = datetime.now(timezone.utc).isoformat(timespec="microseconds")
        db.execute("""
            CREATE TABLE IF NOT EXISTS federal_register_evidence (
                id TEXT PRIMARY KEY NOT NULL,
                document_number TEXT NOT NULL,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                publication_date TEXT NOT NULL,
                document_type TEXT NOT NULL,
                official_pdf_url TEXT,
                first_retrieved_at TEXT NOT NULL,
                last_retrieved_at TEXT NOT NULL
            )
        """)
        db.executemany("""
            INSERT INTO federal_register_evidence (
                id, document_number, title, url, publication_date, document_type,
                official_pdf_url, first_retrieved_at, last_retrieved_at
            ) VALUES (
                :id, :document_number, :title, :url, :publication_date, :document_type,
                :official_pdf_url, :retrieved_at, :retrieved_at
            )
            ON CONFLICT(id) DO UPDATE SET
                title = excluded.title,
                url = excluded.url,
                publication_date = excluded.publication_date,
                document_type = excluded.document_type,
                official_pdf_url = excluded.official_pdf_url,
                last_retrieved_at = MAX(last_retrieved_at, excluded.last_retrieved_at)
        """, ({**document, "retrieved_at": retrieved_at} for document in documents))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", required=True, type=Path, help="SQLite database path")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--document", help="Fetch one published document by number")
    mode.add_argument("--query", help=f"Search published documents (default: {DEFAULT_QUERY})")
    mode.add_argument("--list", action="store_true", help="Export stored evidence as JSON")
    parser.add_argument("--limit", type=int, default=20, help="Latest search results, 1–100")
    args = parser.parse_args()
    if not 1 <= args.limit <= 100:
        parser.error("--limit must be between 1 and 100")
    if args.document and not DOCUMENT_NUMBER.fullmatch(args.document):
        parser.error("--document requires a Federal Register document number")

    try:
        if args.list:
            with closing(sqlite3.connect(args.db.resolve().as_uri() + "?mode=ro", uri=True)) as db:
                db.row_factory = sqlite3.Row
                rows = db.execute("""
                    SELECT * FROM federal_register_evidence
                    ORDER BY publication_date DESC, document_number DESC
                """)
                print(json.dumps([dict(row) for row in rows], indent=2, ensure_ascii=False))
            return

        documents = collect_documents(args.document, args.query or DEFAULT_QUERY, args.limit)
        with closing(sqlite3.connect(args.db)) as db:
            store_documents(db, documents)
    except (OSError, ValueError, KeyError, TypeError, AttributeError, sqlite3.Error) as exc:
        parser.exit(1, f"Evidence intake failed: {exc}\n")
    print(f"Processed {len(documents)} Federal Register documents.")


if __name__ == "__main__":
    main()
