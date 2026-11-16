BEGIN;

CREATE SCHEMA IF NOT EXISTS epstmc;

CREATE TABLE IF NOT EXISTS epstmc.federal_register_evidence (
    id text PRIMARY KEY,
    document_number text NOT NULL,
    title text NOT NULL,
    url text NOT NULL,
    publication_date date NOT NULL,
    document_type text NOT NULL,
    official_pdf_url text,
    first_retrieved_at timestamptz NOT NULL,
    last_retrieved_at timestamptz NOT NULL,
    CHECK (first_retrieved_at <= last_retrieved_at)
);

COMMIT;
