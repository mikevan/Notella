import unittest
from notella.focus import FocusMonitor
from notella.windows import RollingInterceptWindow

class FocusTests(unittest.TestCase):
    def open(self, monitor, identity='case', revision=1, evidence=None):
        return monitor.focus(identity, revision, 'Reviewed correlated signal sequence', ['site-A', 'signal-X'], evidence or [dict(id='r1', payload='trigger')])

    def test_focus_survives_window_expiry_and_keeps_background(self):
        w = RollingInterceptWindow(); w.ingest(dict(id='r1', observedAtMs=1000, availableAtMs=1000)); frame = w.advance(10000)
        m = FocusMonitor(); m.focus('case', 1, 'Reviewed trigger', ['site-A'], frame['added'])
        self.assertEqual(w.advance(11000)['expiredIds'], ['r1'])
        plan = m.plan(['site-A']); self.assertEqual(plan['priorityIncidentIds'], ['case']); self.assertTrue(plan['broadMonitoring'])
        self.assertIn('r1', m.snapshot()['case']['evidence'])

    def test_unrelated_changes_do_not_get_focus_priority(self):
        m = FocusMonitor(); self.open(m)
        self.assertEqual(m.plan(['site-B'])['priorityIncidentIds'], [])
        self.assertEqual(m.plan([])['mode'], 'focused')

    def test_resolution_is_explicit_and_preserves_evidence(self):
        m = FocusMonitor(); self.open(m)
        m.resolve('case', 2, 'Independent evidence reviewed', 'evidence_review')
        self.assertEqual(m.plan([])['mode'], 'broad'); self.assertIn('r1', m.snapshot()['case']['evidence'])
        with self.assertRaises(ValueError): self.open(m, revision=3)

    def test_multiple_incidents_resolve_independently(self):
        m = FocusMonitor(); self.open(m); self.open(m, 'other')
        m.resolve('case', 2, 'Policy-defined inactivity interval elapsed', 'timeout_policy')
        self.assertEqual(m.plan([])['activeIncidentIds'], ['other'])

    def test_conflicts_and_capacity_fail_without_partial_update(self):
        m = FocusMonitor(max_incidents=1); self.open(m); before = m.snapshot()
        with self.assertRaises(ValueError): self.open(m, evidence=[dict(id='r1', payload='changed')])
        with self.assertRaises(ValueError): self.open(m, 'other')
        self.assertEqual(m.snapshot(), before)
        tiny = FocusMonitor(max_evidence_bytes=1)
        with self.assertRaises(ValueError): self.open(tiny)
        self.assertEqual(tiny.snapshot(), {})

    def test_corrections_append_and_snapshots_are_detached(self):
        m = FocusMonitor(); self.open(m)
        self.open(m, revision=2, evidence=[dict(id='r2', retracts='r1')])
        view = m.snapshot(); view['case']['evidence'].clear()
        self.assertEqual(len(m.snapshot()['case']['evidence']), 2)
        with self.assertRaises(ValueError): m.resolve('case', 1, 'old', 'evidence_review')
        with self.assertRaises(ValueError): m.resolve('case', 2, '', 'timeout_policy')

if __name__ == '__main__': unittest.main()
