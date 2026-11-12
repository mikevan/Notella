import copy,unittest
from profiles.layertime.temporal_features import derive_temporal_fact,SHARED_CLOCK
from notella import ValidationError

class TemporalFeatureTests(unittest.TestCase):
 def sample(self):return dict(timeBasis=SHARED_CLOCK,linkingWindowMs=120000,disruption=dict(timeMs=1000,uncertaintyMs=100),drone=dict(timeMs=19000,uncertaintyMs=100))
 def test_in_window_relation(self):
  o=self.sample();original=copy.deepcopy(o);r=derive_temporal_fact(o)['value'];self.assertTrue(r['measurement']['withinWindow']);self.assertEqual(o,original);self.assertNotIn('posture',r);self.assertFalse(r['clockAlignmentIndependentlyVerified'])
 def test_narrow_window(self):
  o=self.sample();o['linkingWindowMs']=10000;self.assertFalse(derive_temporal_fact(o)['value']['measurement']['withinWindow'])
 def test_unknown_clock_is_not_subtracted(self):
  o=self.sample();o['timeBasis']='two unaligned clocks';r=derive_temporal_fact(o)['value']['measurement'];self.assertEqual(r['order'],'unknown');self.assertIsNone(r['withinWindow']);self.assertNotIn('delayIntervalMs',r)
 def test_missing_timestamp(self):
  o=self.sample();o['drone']['timeMs']=None;self.assertEqual(derive_temporal_fact(o)['value']['measurement']['order'],'unknown')
 def test_overlap(self):
  o=self.sample();o['drone']['uncertaintyMs']=20000;self.assertEqual(derive_temporal_fact(o)['value']['measurement']['order'],'uncertain')
 def test_invalid_window_rejected_even_with_missing_time(self):
  o=self.sample();o['drone']['timeMs']=None;o['linkingWindowMs']=-1
  with self.assertRaises(ValidationError):derive_temporal_fact(o)
 def test_input_change_updates_receipt_hash(self):
  o=self.sample();a=derive_temporal_fact(o)['value']['sourceObservationSha256'];o['drone']['timeMs']+=1;self.assertNotEqual(a,derive_temporal_fact(o)['value']['sourceObservationSha256'])
