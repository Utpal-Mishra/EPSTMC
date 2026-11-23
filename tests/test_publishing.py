"""Publication boundaries, correction lineage and read-only projection."""
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
import sqlite3
import os

from editorial import Store
from publishing import Publisher, init_publications, open_reader
from test_editorial import EditorialFixture


class PublicationFixture(EditorialFixture):
    def setUp(self):
        super().setUp()
        if self.pg:
            self.db.execute(Path('migrations/003_publication_postgres.sql').read_text())
        else:
            init_publications(self.store)
        self.publisher = Publisher(self.store)

    def approve(self, version=1):
        if version == 1:
            self.submit()
        else:
            self.store.create(self.story, self.payload, 'editor', 'New draft', version-1)
            self.store.transition(self.story, version, 'submit', 'editor', 'Ready')
        return self.store.transition(self.story, version, 'approve', 'reviewer', 'Private review', self.review)

    def publish(self, version=1, expected=0, kind='initial', summary='First publication'):
        return self.publisher.publish(self.story, version, expected, kind, summary, 'publisher')


class PublishingTests(PublicationFixture):
    def test_approval_is_not_publication(self):
        self.approve()
        self.assertNotIn(self.story, [x['story_id'] for x in self.publisher.feed()['items']])
        with self.assertRaises(LookupError):
            self.publisher.story(self.story)
        with self.assertRaises(LookupError):
            self.publisher.history(self.story)

    def test_publish_only_approved(self):
        self.create()
        with self.assertRaisesRegex(ValueError, 'approved'):
            self.publish()
        self.assertEqual(len(self.store.history(self.story)['events']), 1)

    def test_public_projection_does_not_expose_private_metadata(self):
        self.payload['internal_notes'] = 'DO NOT DISCLOSE'
        self.payload['facts'][0]['private_note'] = 'DO NOT DISCLOSE'
        self.approve()
        result = self.publish()
        rendered = json.dumps(result)
        for value in ('DO NOT DISCLOSE', 'registered_by', 'registration_note', 'reviewed_by', 'Private review', 'assessment'):
            self.assertNotIn(value, rendered)
        self.assertEqual(result['sequence'], 1)
        self.assertEqual(self.store.history(self.story)['events'][-1]['action'], 'published')

    def test_unpublished_new_draft_does_not_replace_live_story(self):
        self.approve()
        first = self.publish()
        self.payload['title'] = 'Unpublished draft'
        self.store.create(self.story, self.payload, 'editor', 'Private change', 1)
        self.assertEqual(self.publisher.story(self.story), first)
        with self.assertRaises(LookupError):
            self.publisher.story(self.story, 2)
        self.assertEqual(len(self.publisher.history(self.story)['versions']), 1)

    def test_correction_retains_old_publication_and_explanation(self):
        self.approve()
        first = self.publish()
        self.payload['facts'][0]['text'] = 'Corrected fictional claim'
        self.approve(2)
        corrected = self.publish(2, 1, 'correction', 'Corrected the fictional claim')
        self.assertEqual(corrected['kind'], 'correction')
        self.assertEqual(self.publisher.story(self.story, 1), first)
        self.assertEqual(self.publisher.story(self.story)['version'], 2)
        self.assertEqual([x['version'] for x in self.publisher.history(self.story)['versions']], [2, 1])

    def test_stale_duplicate_and_wrong_kind_rejected(self):
        self.approve()
        with self.assertRaises(ValueError):
            self.publish(kind='correction')
        self.publish()
        with self.assertRaises(ValueError):
            self.publish()
        self.approve(2)
        with self.assertRaises(ValueError):
            self.publish(2, 0, 'update')
        with self.assertRaises(ValueError):
            self.publish(2, 1, 'initial')
        with self.assertRaises(ValueError):
            self.publish(2, 1, 'correction', '  ')
        self.assertEqual(len(self.publisher.history(self.story)['versions']), 1)

    def test_publication_rows_are_immutable(self):
        self.approve()
        self.publish()
        for sql in ("DELETE FROM {schema}story_publications WHERE story_id = ?",
                    "UPDATE {schema}story_publications SET summary = 'tampered' WHERE story_id = ?"):
            with self.assertRaises(Exception):
                with self.store.transaction():
                    self.store.execute(sql, (self.story,))
        self.assertEqual(self.publisher.story(self.story)['summary'], 'First publication')

    def test_database_rejects_draft_publication(self):
        self.create()
        with self.assertRaises(Exception):
            with self.store.transaction():
                self.store.execute("INSERT INTO {schema}story_publications VALUES (?, 1, 1, 'initial', 'invalid', '2026-01-01')", (self.story,))

    def test_pagination_and_invalid_cursor(self):
        original = self.story
        for i in range(3):
            self.story = original + '-' + str(i)
            self.approve()
            self.publish()
        first = self.publisher.feed(1)
        second = self.publisher.feed(1, first['next_cursor'])
        self.assertNotEqual(first['items'][0]['story_id'], second['items'][0]['story_id'])
        for limit, cursor in ((0, None), (101, None), (1, 'not-a-cursor'), (1, 'e30=')):
            with self.assertRaises(ValueError):
                self.publisher.feed(limit, cursor)

    def test_read_connection_cannot_write(self):
        if self.pg:
            from unittest.mock import patch
            with patch.dict(os.environ, EPSTMC_DATABASE_URL=os.environ['EPSTMC_TEST_DATABASE_URL']):
                with open_reader(postgres=True) as reader:
                    with self.assertRaises(Exception):
                        reader.store.execute("INSERT INTO {schema}editorial_stories VALUES ('forbidden', 1)")
        else:
            with open_reader(self.path) as reader:
                with self.assertRaises(sqlite3.OperationalError):
                    reader.store.execute("INSERT INTO editorial_stories VALUES ('forbidden', 1)")

    def test_concurrent_publish_one_winner(self):
        self.approve()
        barrier = Barrier(2)

        def worker(_):
            if self.pg:
                import psycopg
                from psycopg.rows import dict_row
                db = psycopg.connect(os.environ['EPSTMC_TEST_DATABASE_URL'], autocommit=True, row_factory=dict_row)
            else:
                db = sqlite3.connect(self.path, timeout=5)
                db.row_factory = sqlite3.Row
            try:
                barrier.wait(timeout=5)
                try:
                    Publisher(Store(db, self.pg)).publish(self.story, 1, 0, 'initial', 'First', 'editor')
                    return 'saved'
                except ValueError:
                    return 'stale'
            finally:
                db.close()
        with ThreadPoolExecutor(max_workers=2) as pool:
            self.assertEqual(sorted(pool.map(worker, range(2))), ['saved', 'stale'])
        self.assertEqual(len(self.publisher.history(self.story)['versions']), 1)
