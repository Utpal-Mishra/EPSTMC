"""Behavioral checks shared by SQLite and the CI Postgres service."""
import copy
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
import uuid

from editorial import Store, fingerprint, init_sqlite, open_store
from ingest import normalize_document, run_postgres, store_documents


class EditorialFixture(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / 'evidence.sqlite'
        self.pg = bool(os.getenv('EPSTMC_TEST_DATABASE_URL'))
        if self.pg:
            import psycopg
            from psycopg.rows import dict_row
            self.db = psycopg.connect(os.environ['EPSTMC_TEST_DATABASE_URL'], autocommit=True, row_factory=dict_row)
            self.store = Store(self.db, postgres=True)
            for filename in ('001_federal_register_evidence.sql', '002_editorial_postgres.sql'):
                self.db.execute(Path('migrations', filename).read_text())
        else:
            self.db = sqlite3.connect(self.path)
            self.db.row_factory = sqlite3.Row
            self.db.execute('PRAGMA foreign_keys = ON')
            self.store = Store(self.db)
            init_sqlite(self.store)
        self.story = 'test-' + uuid.uuid4().hex
        self.historical = 'archive-' + uuid.uuid4().hex
        self.document = normalize_document({
            'document_number': '2025-test', 'title': 'Fictional infrastructure notice',
            'html_url': 'https://www.federalregister.gov/d/2025-test',
            'publication_date': '2025-04-07', 'type': 'Notice', 'pdf_url': None})
        self.import_document()
        self.store.register_evidence({
            'id': self.historical, 'title': 'Fictional archive', 'publisher': 'Test archive',
            'url': 'https://example.com/archive', 'publication_date': '2020-01-01'}, 'tester', 'Test fixture')
        self.payload = {
            'title': 'Fictional editorial test',
            'sources': [{'id': 'fr-2025-test'}, {'id': self.historical}],
            'facts': [{'text': 'A notice was issued.', 'source_ids': ['fr-2025-test']}],
            'history': [{'text': 'An earlier project used a staged process.',
                         'comparison': 'Both require consultation.', 'limitations': 'Different legal setting.',
                         'source_ids': [self.historical]}],
            'scenarios': [{'text': 'a follow-up could appear.', 'condition': 'consultation continues',
                           'signal': 'a new notice', 'timeframe': 'within six months',
                           'source_ids': ['fr-2025-test']}]}
        self.review = {'evidence_checked': True, 'checked_source_ids': ['fr-2025-test', self.historical],
                       'scenarios_are_conditional': True, 'assessment': 'Fictional test review only.'}

    def tearDown(self):
        self.db.close()
        self.tmp.cleanup()

    def import_document(self):
        if self.pg:
            run_postgres(os.environ['EPSTMC_TEST_DATABASE_URL'], [self.document])
        else:
            store_documents(self.db, [self.document])

    def create(self):
        return self.store.create(self.story, self.payload, 'editor', 'Initial draft')

    def submit(self):
        self.create()
        return self.store.transition(self.story, 1, 'submit', 'editor', 'Ready for review')


class EditorialTests(EditorialFixture):
    def test_end_to_end_approval_and_history(self):
        self.submit()
        self.assertIn(self.story, [r['story_id'] for r in self.store.queue('in_review')])
        approved = self.store.transition(self.story, 1, 'approve', 'reviewer', 'Reviewed', self.review)
        self.assertEqual(approved['status'], 'approved')
        self.assertEqual(approved['reviewed_by'], 'reviewer')
        self.assertEqual(approved['content_hash'], fingerprint(approved['payload']))
        self.assertEqual([e['action'] for e in self.store.history(self.story)['events']], ['created', 'submit', 'approve'])

    def test_revision_preserves_approval_and_snapshots(self):
        self.submit()
        old = self.store.transition(self.story, 1, 'approve', 'reviewer', 'Reviewed', self.review)
        self.document['title'] = 'Changed upstream title'
        self.import_document()
        self.payload['title'] = 'Corrected draft'
        revised = self.store.create(self.story, self.payload, 'editor', 'Correction reason', 1)
        self.assertEqual(revised['version'], 2)
        self.assertEqual(revised['status'], 'draft')
        self.assertIsNone(revised['review'])
        self.assertEqual(self.store.get(self.story, 1), old)
        self.assertEqual(revised['payload']['sources'][0]['title'], 'Changed upstream title')

    def test_reject_then_revise(self):
        self.submit()
        self.store.transition(self.story, 1, 'reject', 'reviewer', 'Needs stronger evidence')
        self.assertEqual(self.store.create(self.story, self.payload, 'editor', 'Address review', 1)['version'], 2)

    def test_stale_revision_and_approval_blocked(self):
        self.submit()
        self.store.create(self.story, self.payload, 'editor', 'New version', 1)
        with self.assertRaisesRegex(ValueError, 'Stale'):
            self.store.create(self.story, self.payload, 'editor', 'Stale overwrite', 1)
        with self.assertRaisesRegex(ValueError, 'Stale'):
            self.store.transition(self.story, 1, 'approve', 'reviewer', 'Stale approval', self.review)

    def test_approval_requires_review_state(self):
        self.create()
        with self.assertRaisesRegex(ValueError, 'in_review'):
            self.store.transition(self.story, 1, 'approve', 'reviewer', 'Reviewed', self.review)

    def test_incomplete_review_rejected_without_audit_write(self):
        self.submit()
        for field in ('evidence_checked', 'checked_source_ids', 'scenarios_are_conditional', 'assessment'):
            review = dict(self.review)
            review.pop(field)
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.store.transition(self.story, 1, 'approve', 'reviewer', 'Incomplete', review)
        self.assertEqual(self.store.get(self.story, 1)['status'], 'in_review')
        self.assertEqual(len(self.store.history(self.story)['events']), 2)

    def test_scenario_fields_required(self):
        for field in ('condition', 'signal', 'timeframe', 'source_ids'):
            payload = copy.deepcopy(self.payload)
            payload['scenarios'][0].pop(field)
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.store.create(self.story, payload, 'editor', 'Invalid')

    def test_history_context_and_dated_evidence_required(self):
        for field in ('comparison', 'limitations'):
            payload = copy.deepcopy(self.payload)
            payload['history'][0].pop(field)
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.store.create(self.story, payload, 'editor', 'Invalid')
        with self.assertRaises(ValueError):
            self.store.register_evidence({'id': 'bad-date', 'title': 'Bad date', 'publisher': 'Test',
                                         'url': 'https://example.com', 'publication_date': 'yesterday'}, 'editor', 'Invalid')

    def test_unknown_evidence_rolls_back_story_creation(self):
        self.payload['sources'][0]['id'] = 'fr-missing'
        with self.assertRaises(ValueError):
            self.create()
        self.assertIsNone(self.store.execute('SELECT * FROM {schema}editorial_stories WHERE id = ?', (self.story,)).fetchone())

    def test_invalid_revision_does_not_advance_latest(self):
        self.create()
        self.payload['facts'][0]['source_ids'] = ['missing']
        with self.assertRaises(ValueError):
            self.store.create(self.story, self.payload, 'editor', 'Invalid', 1)
        self.assertEqual(self.store.execute('SELECT latest_version FROM {schema}editorial_stories WHERE id = ?',
                                            (self.story,)).fetchone()['latest_version'], 1)

    def test_cannot_replace_registered_evidence(self):
        with self.assertRaises(ValueError):
            self.store.register_evidence({'id': self.historical, 'title': 'Replacement', 'publisher': 'Test',
                                         'url': 'https://example.com', 'publication_date': '2020-01-01'}, 'editor', 'Replace')

    def test_database_preserves_content_and_audit(self):
        self.submit()
        self.store.transition(self.story, 1, 'approve', 'reviewer', 'Reviewed', self.review)
        statements = [
            ("UPDATE {schema}editorial_versions SET payload = '{}' WHERE story_id = ?", (self.story,)),
            ("UPDATE {schema}editorial_versions SET status = 'draft' WHERE story_id = ?", (self.story,)),
            ("DELETE FROM {schema}editorial_versions WHERE story_id = ?", (self.story,)),
            ("DELETE FROM {schema}editorial_events WHERE story_id = ?", (self.story,)),
            ("UPDATE {schema}editorial_events SET note = 'tampered' WHERE story_id = ?", (self.story,)),
            ("DELETE FROM {schema}editorial_evidence WHERE id = ?", (self.historical,))]
        for sql, params in statements:
            with self.subTest(sql=sql), self.assertRaises(Exception):
                with self.store.transaction():
                    self.store.execute(sql, params)
        self.assertEqual(self.store.get(self.story, 1)['status'], 'approved')

    def test_duplicate_import_preserves_one_record(self):
        first = self.store.evidence('fr-2025-test')['first_retrieved_at']
        self.import_document()
        self.assertEqual(self.store.evidence('fr-2025-test')['first_retrieved_at'], first)
        self.assertEqual(self.store.execute("SELECT COUNT(*) AS n FROM {schema}federal_register_evidence WHERE id = ?",
                                            ('fr-2025-test',)).fetchone()['n'], 1)

    def test_renderer_shows_timeframe_and_comparison_limits(self):
        from brief import render_brief
        rendered = render_brief(self.create()['payload'])
        self.assertIn('within six months', rendered)
        self.assertIn('Different legal setting.', rendered)

    def test_concurrent_revisions_only_one_wins(self):
        self.create()
        barrier = Barrier(2)

        def revise():
            if self.pg:
                import psycopg
                from psycopg.rows import dict_row
                db = psycopg.connect(os.environ['EPSTMC_TEST_DATABASE_URL'], autocommit=True, row_factory=dict_row)
            else:
                db = sqlite3.connect(self.path, timeout=5)
                db.row_factory = sqlite3.Row
                db.execute('PRAGMA foreign_keys = ON')
            try:
                store = Store(db, postgres=self.pg)
                barrier.wait(timeout=5)
                try:
                    store.create(self.story, self.payload, 'editor', 'Concurrent revision', 1)
                    return 'saved'
                except ValueError as exc:
                    return str(exc)
            finally:
                db.close()

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: revise(), range(2)))
        self.assertEqual(results.count('saved'), 1)
        self.assertTrue(any('Stale version' in result for result in results))
        self.assertEqual(len(self.store.history(self.story)['versions']), 2)

    def test_legacy_brief_and_invalid_url_port(self):
        from brief import render_brief
        legacy = json.loads(Path('examples/brief.json').read_text())
        self.assertIn('What happened', render_brief(legacy))
        legacy['sources'][0]['url'] = 'https://example.com:invalid/path'
        with self.assertRaises(ValueError):
            render_brief(legacy)

    def test_cli_invalid_input_has_no_traceback(self):
        result = subprocess.run([sys.executable, 'editorial.py', '--db', str(self.path),
                                 'approve', self.story, '--version', '0', '--actor', 'editor',
                                 '--note', 'Invalid', '--review', 'missing.json'], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('Traceback', result.stderr)


if __name__ == '__main__':
    unittest.main()
