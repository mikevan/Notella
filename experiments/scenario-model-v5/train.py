"""Run fresh 4B scenario training from the frozen reviewed development corpus."""
import json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from notella import Notella
from notella.jobs import Jobs

def main():
 out=ROOT/'runtime/scenario-model-v5';prepared=json.loads((out/'prepared.json').read_text())
 if (out/'launch.json').exists():raise ValueError('Preserve launched run')
 api=Notella(out/'store');jobs=Jobs(api,ROOT/'training_engine',sys.executable,{'qwen3-4b':Path(prepared['model'])})
 job=jobs.start(prepared['planId']);(out/'launch.json').write_text(json.dumps(job,indent=2)+'\n');print(json.dumps(dict(jobId=job['id'],status=job['status'])),flush=True)
 while job['status'] in ('starting','running'):
  time.sleep(2);job=jobs.get(job['id'])
 if job['status']!='completed':raise RuntimeError('Inspect failed scenario job '+str(jobs.root/job['id']))
 adapter=jobs.root/job['id']/'adapter';steps=json.loads((adapter/'optimizer-stability.json').read_text());weights=json.loads((adapter/'weight-stability.json').read_text())
 result=dict(jobId=job['id'],applied=steps['appliedOptimizerUpdates'],skipped=steps['skippedOptimizerUpdates'],finite=weights['allWeightsFinite'],adapter=str(adapter),releaseEligible=False)
 (out/'training-result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
if __name__=='__main__':main()
