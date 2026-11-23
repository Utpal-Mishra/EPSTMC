import copy
import unittest
from timeline import load_case, validate_timeline

class TimelineTests(unittest.TestCase):
    def test_real_case_has_separate_dates_and_recent_evidence(self):
        c=load_case()
        self.assertEqual(c['timeline'][0]['event_date'],'2025-01-14')
        self.assertEqual(c['sources'][0]['publication_date'],'2025-01-17')
        self.assertEqual(c['coverage_end'],'2026-11-06')
        self.assertTrue(c['gaps'])
    def test_missing_evidence_and_reversed_events_rejected(self):
        c=load_case()
        broken=copy.deepcopy(c)
        broken['timeline'][0]['source_ids']=['missing']
        with self.assertRaises(ValueError): validate_timeline(broken)
        broken=copy.deepcopy(c)
        broken['timeline'].reverse()
        with self.assertRaises(ValueError): validate_timeline(broken)
