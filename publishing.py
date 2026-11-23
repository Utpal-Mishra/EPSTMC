"""Publish approved editorial versions and expose only published public fields."""

import argparse
import base64
from contextlib import contextmanager
import json
from pathlib import Path
import sqlite3

from brief import required_text
from editorial import Store, encode, fingerprint, identifier, now, open_store, validate_draft, validate_review

SOURCE_FIELDS = ('id', 'title', 'url', 'publication_date', 'publisher', 'document_number',
                 'document_type', 'official_pdf_url', 'first_retrieved_at', 'last_retrieved_at')
SECTION_FIELDS = {'facts': ('text', 'source_ids'),
                  'history': ('text', 'source_ids', 'comparison', 'limitations'),
                  'scenarios': ('text', 'source_ids', 'condition', 'signal', 'timeframe')}


def init_publications(store):
    if store.postgres:
        raise ValueError('Apply migration 003 as schema owner for Postgres')
    store.db.executescript(Path(__file__).with_name('migrations').joinpath(
        '003_publication_sqlite.sql').read_text(encoding='utf-8'))


def public_payload(payload):
    # Editorial assessments, actor identities and arbitrary draft metadata stay private.
    result = {'title': payload['title'], 'sources': [
        {key: source[key] for key in SOURCE_FIELDS if key in source}
        for source in payload['sources']]}
    for section, fields in SECTION_FIELDS.items():
        result[section] = [{key: item[key] for key in fields if key in item}
                           for item in payload[section]]
    return result


class Publisher:
    def __init__(self, store):
        self.store = store

    def publish(self, story_id, version, expected_publication, kind, summary, actor):
        identifier(story_id)
        summary = required_text({'summary': summary}, 'summary')
        actor = required_text({'actor': actor}, 'actor')
        if kind not in ('initial', 'update', 'correction'):
            raise ValueError('Publication kind must be initial, update or correction')
        if type(version) is not int or version < 1 or type(expected_publication) is not int or expected_publication < 0:
            raise ValueError('version must be positive and expected publication must be nonnegative')
        with self.store.transaction():
            self.store.lock_story(story_id, version)
            editorial = self.store.get(story_id, version)
            if editorial['status'] != 'approved':
                raise ValueError('Only approved versions may be published')
            validate_draft(editorial['payload'])
            validate_review(editorial['payload'], editorial['review'])
            if fingerprint(editorial['payload']) != editorial['content_hash']:
                raise ValueError('Content hash mismatch')
            previous = self.store.execute(
                'SELECT sequence, version FROM {schema}story_publications WHERE story_id = ? '
                'ORDER BY sequence DESC LIMIT 1', (story_id,)).fetchone()
            sequence = previous['sequence'] if previous else 0
            if sequence != expected_publication:
                raise ValueError('Stale publication: reload publication history')
            if bool(previous) == (kind == 'initial'):
                raise ValueError('Use initial for first publication; update or correction thereafter')
            if previous and previous['version'] >= version:
                raise ValueError('Publish a newer approved version; existing publications cannot be replaced')
            self.store.execute(
                'INSERT INTO {schema}story_publications '
                '(story_id, version, sequence, kind, summary, published_at) VALUES (?, ?, ?, ?, ?, ?)',
                (story_id, version, sequence + 1, kind, summary, now()))
            self.store.event(story_id, version, 'published', actor, f'{kind}: {summary}')
        return self.story(story_id, version)

    def story(self, story_id, version=None):
        identifier(story_id)
        sql = ('SELECT p.*, v.payload FROM {schema}story_publications p '
               'JOIN {schema}editorial_versions v ON v.story_id = p.story_id AND v.version = p.version '
               'WHERE p.story_id = ?')
        params = [story_id]
        if version is not None:
            sql += ' AND p.version = ?'
            params.append(version)
        row = self.store.execute(sql + ' ORDER BY p.sequence DESC LIMIT 1', params).fetchone()
        if row is None:
            raise LookupError('Published story not found')
        return self.project(row)

    @staticmethod
    def project(row):
        result = {key: row[key] for key in ('story_id', 'version', 'sequence', 'kind', 'summary', 'published_at')}
        result['content'] = public_payload(json.loads(row['payload']))
        return result

    def history(self, story_id):
        identifier(story_id)
        rows = self.store.execute(
            'SELECT p.*, v.payload FROM {schema}story_publications p '
            'JOIN {schema}editorial_versions v ON v.story_id = p.story_id AND v.version = p.version '
            'WHERE p.story_id = ? ORDER BY p.sequence DESC', (story_id,)).fetchall()
        if not rows:
            raise LookupError('Published story not found')
        return {'story_id': story_id, 'versions': [self.project(row) for row in rows]}

    def feed(self, limit=20, cursor=None):
        if type(limit) is not int or not 1 <= limit <= 100:
            raise ValueError('limit must be between 1 and 100')
        params = []
        sql = ('SELECT p.*, v.payload FROM {schema}story_publications p '
               'JOIN {schema}editorial_versions v ON v.story_id = p.story_id AND v.version = p.version '
               'WHERE NOT EXISTS (SELECT 1 FROM {schema}story_publications newer '
               'WHERE newer.story_id = p.story_id AND newer.sequence > p.sequence)')
        if cursor:
            try:
                if not isinstance(cursor, str) or len(cursor) > 1000:
                    raise ValueError()
                stamp, story_id = json.loads(base64.urlsafe_b64decode(cursor.encode()).decode())
                identifier(story_id)
                if not isinstance(stamp, str) or not stamp:
                    raise ValueError()
            except (ValueError, TypeError, UnicodeError):
                raise ValueError('Invalid feed cursor') from None
            sql += ' AND (p.published_at < ? OR (p.published_at = ? AND p.story_id < ?))'
            params.extend((stamp, stamp, story_id))
        sql += ' ORDER BY p.published_at DESC, p.story_id DESC LIMIT ?'
        params.append(limit + 1)
        rows = self.store.execute(sql, params).fetchall()
        items = [self.project(row) for row in rows[:limit]]
        next_cursor = None
        if len(rows) > limit:
            last = items[-1]
            next_cursor = base64.urlsafe_b64encode(encode([last['published_at'], last['story_id']]).encode()).decode()
        return {'items': items, 'next_cursor': next_cursor}


@contextmanager
def open_reader(path=None, postgres=False):
    if postgres:
        with open_store(postgres=True) as store:
            store.db.execute('SET default_transaction_read_only = on')
            yield Publisher(store)
    else:
        db = sqlite3.connect(Path(path).resolve().as_uri() + '?mode=ro', uri=True)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA query_only = ON')
        try:
            yield Publisher(Store(db))
        finally:
            db.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    storage = parser.add_mutually_exclusive_group(required=True)
    storage.add_argument('--db', type=Path)
    storage.add_argument('--postgres', action='store_true')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('init')
    command = sub.add_parser('publish')
    command.add_argument('story')
    command.add_argument('--version', type=int, required=True)
    command.add_argument('--expected-publication', type=int, required=True)
    command.add_argument('--kind', choices=('initial', 'update', 'correction'), required=True)
    command.add_argument('--summary', required=True, help='Public explanation of this publication/change')
    command.add_argument('--actor', required=True)
    args = parser.parse_args()
    try:
        with open_store(args.db, args.postgres) as store:
            if args.command == 'init':
                init_publications(store)
                result = {'initialized': True}
            else:
                result = Publisher(store).publish(args.story, args.version, args.expected_publication,
                                                  args.kind, args.summary, args.actor)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (OSError, ValueError, LookupError, KeyError, TypeError, sqlite3.Error) as exc:
        parser.exit(1, f'Publishing failed: {exc}\n')


if __name__ == '__main__':
    main()
