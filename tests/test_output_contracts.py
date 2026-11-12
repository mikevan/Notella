import json,unittest
from notella.output_contracts import inspect_output

class OutputContractTests(unittest.TestCase):
 def setUp(self):
  self.schema=dict(type='object',properties={'state':dict(type='string',enum=['known','unknown']),'result':dict(type='string',enum=['yes','review'])},required=['state','result'],additionalProperties=False)
  self.states=[dict(state='known',result='yes'),dict(state='unknown',result='review')]
 def inspect(self,text):return inspect_output(text,self.schema,self.states,['state','result'])
 def test_allowed_state(self):self.assertTrue(self.inspect('{"state":"unknown","result":"review"}')['checksPassed'])
 def test_individually_valid_fields_can_contradict(self):
  r=self.inspect('{"state":"unknown","result":"yes"}');self.assertTrue(r['schemaValid']);self.assertFalse(r['stateConsistent']);self.assertFalse(r['checksPassed'])
 def test_no_repair_or_ground_truth_claim(self):
  text='{"state":"unknown","result":"yes"}';r=self.inspect(text);self.assertEqual(r['value']['result'],'yes');self.assertFalse(r['rewritten']);self.assertFalse(r['groundTruthVerified'])
 def test_duplicate_json_rejected(self):self.assertFalse(self.inspect('{"state":"known","state":"unknown","result":"yes"}')['jsonValid'])
 def test_malformed_json_rejected(self):self.assertFalse(self.inspect('broken')['checksPassed'])
