import unittest
from examples.monitoring_replay import run_replay, project

class ReplayTests(unittest.TestCase):
    def test_broad_then_focus_then_expiry_keeps_incident(self):
        result = run_replay(); ticks = {r['endMs']:r for r in result['events']}
        self.assertEqual(ticks[4000]['plan']['mode'], 'broad')
        self.assertEqual(ticks[5000]['newEdges'], 1)
        self.assertEqual(ticks[5000]['plan']['mode'], 'focused')
        self.assertEqual(ticks[11000]['plan']['priorityIncidentIds'], ['incident:wifi-1->drone-1'])  # relevant expiry, not site-B addition
        self.assertEqual(ticks[16000]['plan']['priorityIncidentIds'], [])
        self.assertEqual(ticks[16000]['plan']['mode'], 'focused')
        self.assertTrue(all(e['plan']['broadMonitoring'] for e in result['events']))
        self.assertEqual(set(result['incidents']['incident:wifi-1->drone-1']['evidence']), {'wifi-1', 'drone-1', 'related-1'})
        self.assertEqual(sum(e['newEdges'] for e in result['events']), 1)

    def test_different_site_or_reversed_order_does_not_trigger(self):
        wifi = dict(id='w', observedAtMs=5000, payload=dict(kind='wifi_disruption', site='A'))
        drone = dict(id='d', observedAtMs=1000, payload=dict(kind='drone_signature', site='A'))
        self.assertEqual(project([wifi,drone])['edges'], [])
        drone['observedAtMs'] = 6000; drone['payload']['site'] = 'B'
        self.assertEqual(project([wifi,drone])['edges'], [])

if __name__ == '__main__': unittest.main()
