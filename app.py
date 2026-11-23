"""Account-free EPSTMC reader and GET-only public WSGI API."""

import argparse
from contextlib import contextmanager
import hashlib
from http import HTTPStatus
import json
from pathlib import Path
import re
import sqlite3
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server

from publishing import open_reader

STORY_PATH = re.compile(r'/api/v1/stories/([a-z0-9][a-z0-9-]{0,119})(?:/versions(?:/([1-9][0-9]{0,8}))?)?')
SECURITY_HEADERS = [
    ('X-Content-Type-Options', 'nosniff'), ('Referrer-Policy', 'no-referrer'),
    ('Content-Security-Policy', "default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; frame-ancestors 'none'"),
]


def make_app(reader_factory):
    def application(environ, start_response):
        method = environ.get('REQUEST_METHOD', 'GET')
        headers = list(SECURITY_HEADERS)
        status = 200
        content_type = 'application/json; charset=utf-8'
        try:
            if method not in ('GET', 'HEAD'):
                status, result = 405, {'error': 'Read-only endpoint'}
                headers.append(('Allow', 'GET, HEAD'))
            else:
                path = environ.get('PATH_INFO', '/')
                query = environ.get('QUERY_STRING', '')
                if len(query) > 2048:
                    raise ValueError('Query too long')
                params = parse_qs(query, keep_blank_values=True, max_num_fields=10)
                if path == '/health':
                    # Readiness checks the database/migrations, without exposing rows.
                    with reader_factory() as reader:
                        reader.feed(1)
                    result = {'status': 'ok'}
                elif path == '/api/v1/feed':
                    if set(params) - {'limit', 'cursor'} or any(len(values) != 1 for values in params.values()):
                        raise ValueError('Unsupported query parameters')
                    with reader_factory() as reader:
                        result = reader.feed(int(params.get('limit', ['20'])[0]), params.get('cursor', [None])[0])
                elif STORY_PATH.fullmatch(path):
                    match = STORY_PATH.fullmatch(path)
                    story_id, version = match.groups()
                    with reader_factory() as reader:
                        if path.endswith('/versions'):
                            result = reader.history(story_id)
                        else:
                            result = reader.story(story_id, int(version) if version else None)
                elif path == '/' or re.fullmatch(r'/stories/[a-z0-9][a-z0-9-]{0,119}', path):
                    from reader import feed_page, story_page
                    content_type = 'text/html; charset=utf-8'
                    with reader_factory() as reader:
                        if path == '/':
                            if set(params) - {'cursor'} or any(len(values) != 1 for values in params.values()):
                                raise ValueError('Unsupported query parameters')
                            result = feed_page(reader.feed(20, params.get('cursor', [None])[0]))
                        else:
                            if set(params) - {'version'} or any(len(values) != 1 for values in params.values()):
                                raise ValueError('Unsupported query parameters')
                            version = int(params['version'][0]) if 'version' in params else None
                            if version is not None and not 1 <= version <= 999999999:
                                raise ValueError('Invalid version')
                            story_id = path.rsplit('/', 1)[-1]
                            result = story_page(reader.story(story_id, version), reader.history(story_id))
                else:
                    status, result = 404, {'error': 'Not found'}
        except LookupError:
            status, result = 404, {'error': 'Published story not found'}
        except ValueError:
            status, result = 400, {'error': 'Invalid request'}
        except (OSError, sqlite3.Error):
            status, result = 503, {'error': 'Reader temporarily unavailable'}
        # Backend connection failures are sanitized by open_store as ValueError.
        # A database ValueError must not be mistaken for invalid user input.
        if status != 200:
            content_type = 'application/json; charset=utf-8'
        body = (result.encode('utf-8') if isinstance(result, str) else
                json.dumps(result, ensure_ascii=False, sort_keys=True).encode('utf-8'))
        headers.append(('Content-Type', content_type))
        if status == 200:
            etag = '"' + hashlib.sha256(body).hexdigest() + '"'
            headers.extend((('ETag', etag), ('Cache-Control', 'no-cache')))
            requested_etags = [tag.strip() for tag in environ.get('HTTP_IF_NONE_MATCH', '').split(',')]
            if etag in requested_etags or '*' in requested_etags or 'W/' + etag in requested_etags:
                status = 304
                body = b''
        else:
            headers.append(('Cache-Control', 'no-store'))
        if status != 304:
            headers.append(('Content-Length', str(len(body))))
        start_response(f'{status} {HTTPStatus(status).phrase}', headers)
        return [b'' if method == 'HEAD' else body]
    return application


def create_app(path=None, postgres=False):
    @contextmanager
    def reader_factory():
        try:
            with open_reader(path, postgres) as reader:
                yield reader
        except ValueError as exc:
            # Connection setup/migration failures become availability errors.
            if str(exc).startswith(('Postgres operation failed', 'Apply migrations',
                                    'EPSTMC_DATABASE_URL', 'Install requirements')):
                raise OSError('Reader unavailable') from None
            raise
    return make_app(reader_factory)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    storage = parser.add_mutually_exclusive_group(required=True)
    storage.add_argument('--db', type=Path)
    storage.add_argument('--postgres', action='store_true')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8080)
    args = parser.parse_args()
    with make_server(args.host, args.port, create_app(args.db, args.postgres)) as server:
        print(f'EPSTMC development reader: http://{args.host}:{args.port}')
        server.serve_forever()


if __name__ == '__main__':
    main()
