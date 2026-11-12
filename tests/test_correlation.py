import unittest
from notella.correlation import temporal_link
from notella import ValidationError

class TemporalTests(unittest.TestCase):
 def test_supported_link(self):
  r=temporal_link(1000,19000,100,100);self.assertEqual(r['delayIntervalMs'],[17800,18200]);self.assertTrue(r['withinWindow']);self.assertFalse(r['causationEstablished'])
 def test_uncertain_order(self):self.assertIsNone(temporal_link(1000,1100,100,100)['withinWindow'])
 def test_reversed(self):self.assertEqual(temporal_link(2000,1000)['order'],'before')
 def test_missing(self):self.assertEqual(temporal_link(None,1000)['order'],'unknown')
 def test_boundary_uncertainty(self):self.assertIsNone(temporal_link(0,120000,0,1)['withinWindow'])
 def test_invalid(self):
  with self.assertRaises(ValidationError):temporal_link(0,100,-1)
