"""Create a NEW SQLite database with two explicitly fictional published versions."""
import argparse
import json
from pathlib import Path

from editorial import init_sqlite, open_store
from publishing import Publisher, init_publications


def seed(path):
    # Exclusive creation prevents demo data from being added to a real database.
    path = Path(path)
    with path.open('xb'):
        pass
    examples = Path(__file__).with_name('examples')
    read = lambda name: json.loads((examples / name).read_text(encoding='utf-8'))
    with open_store(path) as store:
        init_sqlite(store)
        init_publications(store)
        for file in ('proposal-evidence.json', 'archive-evidence.json'):
            store.register_evidence(read(file), 'fictional-demo', 'Fictional demo only')
        draft = read('editorial-draft.json')
        review = read('editorial-review.json')
        for version in (1, 2):
            if version == 2:
                draft['facts'][0]['text'] = 'Fictional correction: the council proposed a pilot covering three routes.'
            store.create('fictional-bus-pilot', draft, 'fictional-demo', 'Fictional demonstration',
                         version - 1 if version > 1 else None)
            store.transition('fictional-bus-pilot', version, 'submit', 'fictional-demo', 'Fictional review')
            store.transition('fictional-bus-pilot', version, 'approve', 'fictional-demo', 'Fictional review', review)
            Publisher(store).publish('fictional-bus-pilot', version, version - 1,
                                     'initial' if version == 1 else 'correction',
                                     'Fictional demo only' if version == 1 else 'Fictional correction: three routes, not two.',
                                     'fictional-demo')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', type=Path, required=True)
    args = parser.parse_args()
    try:
        seed(args.db)
    except (OSError, ValueError) as exc:
        parser.exit(1, f'Demo setup failed: {exc}\n')
    print('Fictional demo ready. Run: python app.py --db ' + str(args.db))


if __name__ == '__main__':
    main()
