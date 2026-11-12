import json,unittest
from notella.scoring import score_output
from notella import ValidationError

class ScoringTests(unittest.TestCase):
 def setUp(self):
  self.schema=dict(type='object',properties={'decision':dict(type='string',enum=['yes','no']),'reason':dict(type='string',maxLength=8)},required=['decision','reason'],additionalProperties=False)
  self.target=dict(decision='yes',reason='Evidence')
 def score(self,text,fields=None):return score_output(text,self.target,self.schema,fields or ['decision'])
 def test_format_failure_does_not_hide_correct_decision(self):
  r=self.score(json.dumps(dict(decision='yes',reason='A reason longer than the contract permits')))
  self.assertTrue(r['decisionFieldsMatch']);self.assertFalse(r['schemaValid']);self.assertFalse(r['schemaAndDecisionMatch'])
 def test_valid_json_can_have_wrong_decision(self):
  r=self.score(json.dumps(dict(decision='no',reason='Evidence')));self.assertTrue(r['schemaValid']);self.assertFalse(r['decisionFieldsMatch'])
 def test_invalid_json_retained_as_failure(self):
  r=self.score('not json');self.assertFalse(r['jsonValid']);self.assertFalse(r['decisionFieldsMatch'])
 def test_unknown_field_rejected(self):
  with self.assertRaises(ValidationError):self.score('{}',['missing'])
 def test_duplicate_field_rejected(self):
  with self.assertRaises(ValidationError):self.score('{}',['decision','decision'])
 def test_missing_output_field_is_a_mismatch(self):
  r=self.score('{}');self.assertFalse(r['fieldMatches']['decision'])
 def test_duplicate_output_keys_rejected(self):
  r=self.score('{"decision":"no","decision":"yes","reason":"Evidence"}');self.assertFalse(r['jsonValid']);self.assertIn('Duplicate',r['error'])
