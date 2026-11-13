"""Two real updates on the longest graph target before the full memory retry."""
import json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from notella import Notella
from notella.jobs import Jobs
out=ROOT/'runtime/scenario-model-v2';prepared=json.loads((out/'prepared.json').read_text());api=Notella(out/'store');corpus=api.get('curricula',prepared['curriculumId'])
if (out/'memory-check-launch.json').exists():raise ValueError('Preserve earlier memory check')
rows=[]
for e in corpus['examples']:
 if e['split']=='train' and e['id']!='source-correction-step-4':continue
 rows.append(dict(id=e['id'],family=e['family'],split=e['split'],concepts=e['concepts'],source=e['source'],input=e['messages'][-2]['content'],target=json.loads(e['messages'][-1]['content'])))
cid=api.compile(corpus['ontologyId'],rows)['id'];pid=api.plan(cid,'qwen3-4b',steps=2,rank=16,learning_rate=0.0001)['id'];jobs=Jobs(api,ROOT/'training_engine',sys.executable,{'qwen3-4b':Path(prepared['model'])})
job=jobs.start(pid);(out/'memory-check-launch.json').write_text(json.dumps(job,indent=2));print(json.dumps(dict(jobId=job['id'],status=job['status'])),flush=True)
while job['status'] in ('starting','running'):time.sleep(2);job=jobs.get(job['id'])
if job['status']!='completed':raise RuntimeError('Longest-example memory check failed; inspect job')
adapter=jobs.root/job['id']/'adapter';steps=json.loads((adapter/'optimizer-stability.json').read_text());weights=json.loads((adapter/'weight-stability.json').read_text())
result=dict(jobId=job['id'],applied=steps['appliedOptimizerUpdates'],skipped=steps['skippedOptimizerUpdates'],finite=weights['allWeightsFinite']);(out/'memory-check-result.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)
if result['applied']!=2 or result['skipped'] or not result['finite']:raise RuntimeError('Numerical memory check failed')
