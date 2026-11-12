"""Actual HTTP-to-CUDA integration probe. Two updates verify plumbing, not model quality."""
import json,os,secrets,sys,threading,time,urllib.request
from pathlib import Path
from notella import Notella
from notella.jobs import Jobs
from notella.http import server

root=Path(__file__).resolve().parent
service=Notella(root/'runtime/backend-verification')
token=secrets.token_urlsafe(32)
model=Path(os.environ['NOTELLA_TEST_MODEL'])
jobs=Jobs(service,root/'training_engine',sys.executable,{'local-test-model':model})
http=server(service,token,port=0,jobs=jobs)
threading.Thread(target=http.serve_forever,daemon=True).start()
url='http://127.0.0.1:'+str(http.server_address[1])
def request(path,body=None):
 req=urllib.request.Request(url+path,data=json.dumps(body).encode() if body is not None else None,headers={'Authorization':'Bearer '+token,'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=30) as response:return json.load(response)
try:
 o=request('/v1/ontologies',json.loads((root/'examples/layertime.ontology.json').read_text()))
 c=request('/v1/curricula',dict(ontologyId=o['id'],examples=json.loads((root/'examples/layertime.examples.json').read_text())))
 p=request('/v1/plans',dict(curriculumId=c['id'],baseModel='local-test-model',steps=2))
 job=request('/v1/jobs',dict(planId=p['id']));print(json.dumps(job),flush=True)
 while job['status'] in ('starting','running'):
  time.sleep(2);job=request('/v1/jobs/'+job['id'])
 result=dict(job=job,httpRoundtrip=True,probeOnly=True,modelQualityMeasured=False)
 if job['status']=='completed':
  folder=jobs.root/job['id']/'adapter'
  result['optimizer']=json.loads((folder/'optimizer-stability.json').read_text())
  result['weights']=json.loads((folder/'weight-stability.json').read_text())
 (root/'runtime/backend-verification-result.json').write_text(json.dumps(result,indent=2))
 print(json.dumps(result,indent=2),flush=True)
 if job['status']!='completed':raise SystemExit(1)
finally:http.shutdown();http.server_close()
