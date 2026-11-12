import copy,json,tempfile,threading,time,unittest,urllib.request,urllib.error
from pathlib import Path
from unittest.mock import patch
from notella import Notella,ValidationError
from notella.http import server
from notella.jobs import Jobs
from notella.training_profile import verify

ONTOLOGY=dict(name='Example',version='1',concepts={'evidence':'Observed facts','claim':'An interpretation'},
 relations=[dict(subject='claim',predicate='supportedBy',object='evidence')],instruction='Distinguish observation and claim.',
 outputSchema=dict(type='object',properties={'finding':dict(type='string',minLength=1)},required=['finding'],additionalProperties=False))
def examples():
 return [dict(id=str(i),family='family-'+str(i),split=split,concepts=['evidence','claim'],
  source=dict(id='authored',kind='synthetic',reference='case-'+str(i),permission='project development',labelAuthor='test-author',trainingAllowed=True),
  input='Observation '+str(i),target=dict(finding='Not proof of cause.')) for i,split in enumerate(['train','validation','test'])]

class CoreTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.api=Notella(self.tmp.name)
  self.o=self.api.register_ontology(copy.deepcopy(ONTOLOGY))
 def compile(self,rows=None):return self.api.compile(self.o['id'],rows or examples())
 def test_reproducibility(self):self.assertEqual(self.compile()['id'],self.compile()['id'])
 def test_relation_validation(self):
  o=copy.deepcopy(ONTOLOGY);o['relations'][0]['object']='missing'
  with self.assertRaises(ValidationError):self.api.register_ontology(o)
 def test_unsupported_schema_rejected_up_front(self):
  o=copy.deepcopy(ONTOLOGY);o['outputSchema']['properties']['finding']['pattern']='x'
  with self.assertRaises(ValidationError):self.api.register_ontology(o)
 def test_family_leakage(self):
  e=examples();e[1]['family']=e[0]['family']
  with self.assertRaisesRegex(ValidationError,'Family crosses'):self.compile(e)
 def test_prompt_leakage(self):
  e=examples();e[1]['input']=e[0]['input']
  with self.assertRaisesRegex(ValidationError,'Input crosses'):self.compile(e)
 def test_source_admission(self):
  e=examples();e[0]['source']['trainingAllowed']=False
  with self.assertRaises(ValidationError):self.compile(e)
 def test_schema_rejects_wrong_answer(self):
  e=examples();e[0]['target']={'finding':True}
  with self.assertRaises(ValidationError):self.compile(e)
 def test_exclusion(self):
  c=self.compile()
  with self.assertRaisesRegex(ValidationError,'Excluded'):self.api.compile(self.o['id'],examples(),[c['artifact']['examples'][0]['promptSha256']])
 def test_stored_tampering(self):
  p=self.api.root/'ontologies'/(self.o['id']+'.json');p.write_text('{}')
  with self.assertRaisesRegex(ValidationError,'integrity'):self.api.get('ontologies',self.o['id'])
 def test_path_escape(self):
  with self.assertRaises(ValidationError):self.api.get('ontologies','../secret')
 def test_evaluation_missing_and_wrong_split(self):
  c=self.compile();r=self.api.evaluate(c['id'],{})['artifact'];self.assertEqual(r['total'],1);self.assertEqual(r['schemaPasses'],0)
  with self.assertRaises(ValidationError):self.api.evaluate(c['id'],{'0':{'finding':'x'}})
 def test_exact_match_does_not_claim_semantics(self):
  c=self.compile();r=self.api.evaluate(c['id'],{'2':examples()[2]['target']})['artifact']
  self.assertEqual(r['exactTargetMatches'],1);self.assertFalse(r['semanticAccuracyMeasured'])
 def test_plan_bounds(self):
  c=self.compile()
  for kwargs in ({'steps':True},{'rank':129},{'learning_rate':float('nan')}):
   with self.assertRaises(ValidationError):self.api.plan(c['id'],'local',**kwargs)
 def test_training_disabled(self):
  c=self.compile();p=self.api.plan(c['id'],'local')
  with self.assertRaisesRegex(ValidationError,'not configured'):Jobs(self.api).start(p['id'])
 def test_backend_exports_and_runs_without_shell(self):
  engine=self.api.root/'engine';engine.mkdir();(engine/'train_lora.py').write_text('')
  model=self.api.root/'model';model.mkdir();c=self.compile();p=self.api.plan(c['id'],'local')
  gate=threading.Event()
  class Process:
   pid=123
   def wait(self):gate.wait(5);return 0
  jobs=Jobs(self.api,engine,models={'local':model})
  with patch('notella.jobs.subprocess.Popen',return_value=Process()) as spawn:
   j=jobs.start(p['id']);verify(jobs.root/j['id']/'dataset')
   self.assertIsInstance(spawn.call_args.args[0],list);self.assertNotIn('shell',spawn.call_args.kwargs)
   with self.assertRaisesRegex(ValidationError,'GPU lock'):jobs.start(p['id'])
   gate.set()
   for _ in range(100):
    if jobs.get(j['id'])['status']=='completed':break
    time.sleep(.01)
   self.assertEqual(jobs.get(j['id'])['status'],'completed')
 def test_http_auth_and_roundtrip(self):
  token='test-token-with-at-least-24-characters';http=server(self.api,token,port=0)
  thread=threading.Thread(target=http.serve_forever,daemon=True);thread.start()
  self.addCleanup(http.server_close);self.addCleanup(http.shutdown)
  url='http://127.0.0.1:'+str(http.server_address[1])
  self.assertEqual(json.load(urllib.request.urlopen(url+'/health'))['product'],'Notella')
  with self.assertRaises(urllib.error.HTTPError) as error:urllib.request.urlopen(url+'/v1/ontologies/'+self.o['id'])
  self.assertEqual(error.exception.code,401)
  req=urllib.request.Request(url+'/v1/ontologies',data=json.dumps(ONTOLOGY).encode(),headers={'Authorization':'Bearer '+token,'Content-Type':'application/json'})
  self.assertEqual(json.load(urllib.request.urlopen(req))['id'],self.o['id'])
  from notella import Client
  client=Client(token,url)
  self.assertEqual(client.register_ontology(ONTOLOGY)['id'],self.o['id'])
  self.assertEqual(client.request('/v1/openapi.json')['openapi'],'3.1.0')
 def test_non_loopback_rejected(self):
  with self.assertRaises(ValidationError):server(self.api,'x'*32,host='0.0.0.0')

if __name__=='__main__':unittest.main()
