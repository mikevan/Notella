import json,tempfile,unittest,hashlib,threading
from notella import Notella,ValidationError,Client
from notella.http import server
from notella.semantic_reviews import record_review
from examples.tutorial import teaching_material

class ReviewTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.api=Notella(self.tmp.name)
  o,e=teaching_material();oid=self.api.register_ontology(o)['id'];self.c=self.api.compile(oid,e)['id'];self.output=json.dumps(e[-1]['target'])
  self.reviewer=dict(name='Test author',kind='agent',independent=False)
  self.criteria=[dict(id='meaning',description='Reading compared correctly against supplied threshold')]
  self.judgments=[dict(criterionId='meaning',status='pass',rationale='35 is strictly greater than 30.')]
 def review(self,**kwargs):
  params=dict(api=self.api,curriculum_id=self.c,example_id='test-warm',output=self.output,reviewer=self.reviewer,criteria=self.criteria,judgments=self.judgments,split='test');params.update(kwargs);return record_review(**params)
 def test_exact_output_hash(self):
  r=self.review()['artifact'];self.assertEqual(r['outputSha256'],hashlib.sha256(self.output.encode()).hexdigest());self.assertTrue(r['schemaValid']);self.assertFalse(r['automaticallyMeasuredSemanticAccuracy'])
 def test_whitespace_changes_review_identity(self):self.assertNotEqual(self.review()['id'],self.review(output=self.output+'\n')['id'])
 def test_missing_judgment_rejected(self):
  with self.assertRaises(ValidationError):self.review(judgments=[])
 def test_wrong_split_rejected(self):
  with self.assertRaises(ValidationError):self.review(split='validation')
 def test_unknown_criterion_rejected(self):
  with self.assertRaises(ValidationError):self.review(judgments=[dict(criterionId='other',status='pass',rationale='x')])
 def test_not_assessed_is_not_pass(self):
  r=self.review(judgments=[dict(criterionId='meaning',status='not_assessed',rationale='Needs independent review')]);self.assertFalse(r['artifact']['allCriteriaPassed'])
 def test_invalid_json_can_be_reviewed(self):
  r=self.review(output='Not JSON',judgments=[dict(criterionId='meaning',status='fail',rationale='Expected structured answer absent.')]);self.assertFalse(r['artifact']['schemaValid'])
 def test_http_review_roundtrip(self):
  token='review-test-token-at-least-24-characters';http=server(self.api,token,port=0);threading.Thread(target=http.serve_forever,daemon=True).start()
  try:
   client=Client(token,'http://127.0.0.1:'+str(http.server_address[1]))
   r=client.record_review(self.c,'test-warm',self.output,self.reviewer,self.criteria,self.judgments,split='test')
   self.assertEqual(client.get('interpretation-reviews',r['id'])['output'],self.output)
   self.assertIn('/v1/interpretation-reviews',client.request('/v1/openapi.json')['paths'])
  finally:http.shutdown();http.server_close()
