import hashlib,json,tempfile,unittest
from pathlib import Path
from notella import Notella,ValidationError
from notella.profile import prepare_profile
from examples.tutorial import teaching_material

class ProfileTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.api=Notella(self.root/'store')
  o,e=teaching_material();self.profile=dict(formatVersion='notella.profile.v1',training=dict(baseModel='local',steps=30,rank=16,learningRate=0.00005))
  for key,value in (('ontology',o),('examples',e)):
   file=self.root/(key+'.json');file.write_text(json.dumps(value));self.profile[key]=dict(file=file.name,sha256=hashlib.sha256(file.read_bytes()).hexdigest())
  self.save()
 def save(self):
  self.path=self.root/'profile.json';self.path.write_text(json.dumps(self.profile))
 def test_prepare_is_reproducible_and_does_not_train(self):
  a=prepare_profile(self.api,self.path);b=prepare_profile(self.api,self.path);self.assertEqual(a,b);self.assertFalse(a['trainingStarted']);self.assertEqual(a['splits'],dict(train=3,validation=1,test=1))
 def test_component_tampering_rejected(self):
  (self.root/'examples.json').write_text('[]')
  with self.assertRaisesRegex(ValidationError,'hash mismatch'):prepare_profile(self.api,self.path)
 def test_path_escape_rejected(self):
  self.profile['examples']['file']='../outside.json';self.save()
  with self.assertRaisesRegex(ValidationError,'escapes'):prepare_profile(self.api,self.path)
 def test_unknown_training_settings_rejected(self):
  self.profile['training']['shellCommand']='unwanted';self.save()
  with self.assertRaisesRegex(ValidationError,'supported training'):prepare_profile(self.api,self.path)
 def test_windows_utf8_bom_manifest(self):
  self.path.write_text(json.dumps(self.profile),encoding='utf-8-sig')
  self.assertFalse(prepare_profile(self.api,self.path)['trainingStarted'])
