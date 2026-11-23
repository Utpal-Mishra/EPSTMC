"""Validate the shared source-backed story contract and inspect its chronology."""
import argparse
from datetime import date, datetime
import json
from pathlib import Path
from brief import render_brief, required_text
from editorial import identifier

DEFAULT_CASE = Path(__file__).with_name('web') / 'worker' / 'case-study.json'


def validate_timeline(case):
    identifier(required_text(case, 'id'))
    render_brief(case)
    checked = datetime.fromisoformat(required_text(case, 'research_checked_at').replace('Z', '+00:00'))
    if checked.tzinfo is None:
        raise ValueError('Research check must include a timezone')
    source_ids = set()
    for source in case['sources']:
        source_id = identifier(required_text(source, 'id'))
        if source_id in source_ids:
            raise ValueError('Duplicate source ID')
        source_ids.add(source_id)
        published = date.fromisoformat(required_text(source, 'publication_date'))
        retrieved = datetime.fromisoformat(required_text(source, 'retrieved_at').replace('Z', '+00:00'))
        if retrieved.tzinfo is None or published > retrieved.date() or retrieved > checked:
            raise ValueError('Invalid source provenance dates')
        required_text(source, 'publisher')
    events = case.get('timeline')
    if not isinstance(events, list) or not events:
        raise ValueError('Provide a nonempty timeline')
    previous = None
    event_ids = set()
    for item in events:
        event_id = identifier(required_text(item, 'id'))
        if event_id in event_ids:
            raise ValueError('Duplicate event ID')
        event_ids.add(event_id)
        event_day = date.fromisoformat(required_text(item, 'event_date'))
        if previous is not None and event_day < previous:
            raise ValueError('Timeline must be chronological')
        if item.get('kind') not in ('fact', 'interpretation', 'planned'):
            raise ValueError('Invalid event kind')
        if item.get('kind') != 'planned' and event_day > checked.date():
            raise ValueError('Future facts require a planned-event label')
        if item.get('date_precision') != 'day':
            raise ValueError('Unsupported date precision')
        for key in ('title', 'text', 'connection'):
            required_text(item, key)
        refs = item.get('source_ids')
        if not isinstance(refs, list) or not refs or any(ref not in source_ids for ref in refs):
            raise ValueError('Unknown or missing event evidence')
        previous = event_day
    if case.get('coverage_start') != events[0]['event_date'] or case.get('coverage_end') != events[-1]['event_date']:
        raise ValueError('Coverage must match timeline endpoints')
    for item in case['history']:
        required_text(item, 'comparison')
        required_text(item, 'limitations')
    for item in case['scenarios']:
        required_text(item, 'timeframe')
    if not case.get('gaps') or any(not isinstance(x, str) or not x.strip() for x in case['gaps']):
        raise ValueError('State the coverage limitations')
    return case


def load_case(path=DEFAULT_CASE):
    return validate_timeline(json.loads(Path(path).read_text(encoding='utf-8')))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', type=Path, default=DEFAULT_CASE)
    parser.add_argument('--year', type=int)
    parser.add_argument('--month', type=int, choices=range(1, 13))
    args = parser.parse_args()
    try:
        case = load_case(args.case)
        events = [e for e in case['timeline'] if
                  (args.year is None or int(e['event_date'][:4]) == args.year) and
                  (args.month is None or int(e['event_date'][5:7]) == args.month)]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f'Invalid timeline: {exc}\n')
    print(json.dumps({'status': 'research_preview', 'id': case['id'], 'coverage_end': case['coverage_end'],
                      'research_checked_at': case['research_checked_at'], 'events': events}, indent=2))


if __name__ == '__main__':
    main()
