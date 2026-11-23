"""Exercise the real WSGI interface without opening network sockets."""
from contextlib import contextmanager
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from app import make_app, create_app
from test_publishing import PublicationFixture


class AppTests(PublicationFixture):
    def setUp(self):
        super().setUp()
        @contextmanager
        def reader():
            yield self.publisher
        self.app = make_app(reader)

    def request(self, path, method='GET', query='', etag=None, app=None):
        captured = {}
        def start(status, headers):
            captured.update(status=int(status.split()[0]), headers=dict(headers))
        env = {'PATH_INFO': path, 'REQUEST_METHOD': method, 'QUERY_STRING': query}
        if etag:
            env['HTTP_IF_NONE_MATCH'] = etag
        body = b''.join((app or self.app)(env, start))
        return captured['status'], captured['headers'], body

    def test_drafts_and_approvals_invisible_over_http(self):
        self.approve()
        for path in (f'/api/v1/stories/{self.story}', f'/api/v1/stories/{self.story}/versions',
                     f'/api/v1/stories/{self.story}/versions/1', f'/stories/{self.story}'):
            self.assertEqual(self.request(path)[0], 404)
        self.assertNotIn(self.story.encode(), self.request('/api/v1/feed')[2])

    def test_feed_story_and_published_versions(self):
        self.approve()
        self.publish()
        for path in ('/health', '/api/v1/feed', f'/api/v1/stories/{self.story}',
                     f'/api/v1/stories/{self.story}/versions', f'/api/v1/stories/{self.story}/versions/1'):
            status, headers, body = self.request(path)
            self.assertEqual(status, 200)
            json.loads(body)
            self.assertEqual(headers['X-Content-Type-Options'], 'nosniff')

    def test_mutations_are_rejected(self):
        for method in ('POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'):
            status, headers, _ = self.request('/api/v1/feed', method)
            self.assertEqual(status, 405)
            self.assertEqual(headers['Allow'], 'GET, HEAD')

    def test_etag_conditional_read_and_head(self):
        self.approve()
        self.publish()
        status, headers, body = self.request('/api/v1/feed')
        self.assertEqual(status, 200)
        status2, headers2, body2 = self.request('/api/v1/feed', 'HEAD')
        self.assertEqual(status2, 200)
        self.assertEqual(body2, b'')
        self.assertEqual(int(headers2['Content-Length']), len(body))
        self.assertEqual(self.request('/api/v1/feed', etag=headers['ETag'])[0], 304)
        self.payload['title'] = 'Updated fictional title'
        self.approve(2)
        self.publish(2, 1, 'update', 'A new fictional development')
        self.assertEqual(self.request('/api/v1/feed', etag=headers['ETag'])[0], 200)

    def test_reader_shows_correction_and_old_version_notice(self):
        self.approve()
        self.publish()
        self.approve(2)
        self.publish(2, 1, 'correction', 'Corrected the fictional route count')
        status, headers, body = self.request(f'/stories/{self.story}', query='version=1')
        self.assertEqual(status, 200)
        self.assertIn('text/html', headers['Content-Type'])
        for phrase in (b'earlier publication', b'Publication history', b'Corrected the fictional route count',
                       b'Historical context', b'Limitations:', b'Timeframe:', b'Original sources'):
            self.assertIn(phrase, body)

    def test_reader_escapes_editor_supplied_html(self):
        self.payload['title'] = '<script>alert(1)</script>'
        self.approve()
        self.publish(summary='<img src=x onerror=alert(1)>')
        for path in ('/', f'/stories/{self.story}'):
            body = self.request(path)[2]
            self.assertNotIn(b'<script>', body)
            self.assertNotIn(b'<img src=x', body)
            self.assertIn(b'&lt;script&gt;', body)
            self.assertIn(b'&lt;img', body)

    def test_invalid_requests_are_bounded(self):
        for query in ('limit=0', 'limit=101', 'limit=bad', 'cursor=broken', 'limit=1&limit=2',
                      'unexpected=1', 'a=1&'*20, 'cursor='+'x'*3000):
            self.assertEqual(self.request('/api/v1/feed', query=query)[0], 400, query)
        self.assertEqual(self.request('/no-such-route')[0], 404)
        self.assertEqual(self.request('/api/v1/stories/../../private')[0], 404)

    def test_unavailable_database_does_not_leak_errors(self):
        with TemporaryDirectory() as tmp:
            app = create_app(Path(tmp) / 'missing.sqlite')
            status, _, body = self.request('/api/v1/feed', app=app)
            self.assertEqual(status, 503)
            self.assertNotIn(tmp.encode(), body)
        with patch.dict('os.environ', {}, clear=True):
            status, _, body = self.request('/api/v1/feed', app=create_app(postgres=True))
            self.assertEqual(status, 503)
            self.assertNotIn(b'EPSTMC_DATABASE_URL', body)

    def test_empty_feed_has_useful_reader_state(self):
        # Other Postgres tests may leave publications, so use a deterministic empty reader.
        with patch.object(self.publisher, 'feed', return_value={'items': [], 'next_cursor': None}):
            status, _, body = self.request('/')
            self.assertEqual(status, 200)
            self.assertIn(b'No stories have been published yet', body)

    def test_real_read_connection_serves_published_content(self):
        self.approve()
        self.publish()
        if self.pg:
            with patch.dict('os.environ', EPSTMC_DATABASE_URL=__import__('os').environ['EPSTMC_TEST_DATABASE_URL']):
                status, _, body = self.request('/api/v1/stories/' + self.story, app=create_app(postgres=True))
        else:
            status, _, body = self.request('/api/v1/stories/' + self.story, app=create_app(self.path))
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)['story_id'], self.story)

    def test_fictional_demo_and_safe_existing_database_check(self):
        from demo import seed
        from app import create_app
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / 'demo.sqlite'
            seed(path)
            app = create_app(path)
            status, _, body = self.request('/stories/fictional-bus-pilot', app=app)
            self.assertEqual(status, 200)
            self.assertIn(b'Fictional correction: three routes, not two.', body)
            self.assertIn(b'name="viewport"', body)
            with self.assertRaises(FileExistsError):
                seed(path)
