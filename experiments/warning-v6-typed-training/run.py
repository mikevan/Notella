"""Run the prepared training job, then matched base/adapter development generation."""
import json,os,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from notella import Notella
from notella.jobs import Jobs

def main():
 out=ROOT/'runtime/warning-v6-typed-training';prepared=json.loads((out/'prepared.json').read_text())
 model=Path(os.environ['NOTELLA_EXPERIMENT_MODEL']);api=Notella(out/'store');jobs=Jobs(api,ROOT/'training_engine',sys.executable,{'qwen3-4b':model})
 if (out/'launch.json').exists():raise ValueError('Existing experiment launch preserved; inspect it before creating another run')
 job=jobs.start(prepared['planId']);(out/'launch.json').write_text(json.dumps(job,indent=2)+'\n');print(json.dumps(dict(jobId=job['id'],status=job['status'])),flush=True)
 while job['status'] in ('starting','running'):
  time.sleep(2);job=jobs.get(job['id'])
 if job['status']!='completed':raise RuntimeError('Training failed; inspect '+str(jobs.root/job['id']))
 adapter=jobs.root/job['id']/'adapter'
 stability=json.loads((adapter/'optimizer-stability.json').read_text());weights=json.loads((adapter/'weight-stability.json').read_text())
 print(json.dumps(dict(applied=stability['appliedOptimizerUpdates'],skipped=stability['skippedOptimizerUpdates'],finite=weights['allWeightsFinite'])),flush=True)
 for name in ('base','adapted'):
  command=[sys.executable,str(Path(__file__).with_name('evaluate.py')),'--model',str(model),'--output',str(out/(name+'-validation.json'))]
  if name=='adapted':command+=['--adapter',str(adapter)]
  with (out/(name+'-evaluation.stdout.log')).open('wb') as stdout,(out/(name+'-evaluation.stderr.log')).open('wb') as stderr:
   subprocess.run(command,check=True,env=os.environ.copy(),stdout=stdout,stderr=stderr)
  print(name+' development evaluation complete',flush=True)
 base=json.loads((out/'base-validation.json').read_text());adapted=json.loads((out/'adapted-validation.json').read_text())
 if [r['promptSha256'] for r in base['results']] != [r['promptSha256'] for r in adapted['results']]:raise ValueError('Comparison prompts differ')
 result=dict(jobId=job['id'],appliedUpdates=stability['appliedOptimizerUpdates'],skippedUpdates=stability['skippedOptimizerUpdates'],allWeightsFinite=weights['allWeightsFinite'],matchedPrompts=True,
  baseDecisionMatches=base['decisionFieldMatches'],adaptedDecisionMatches=adapted['decisionFieldMatches'],developmentCases=base['total'],semanticAccuracyMeasured=False,releaseEligible=False)
 (out/'comparison.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2),flush=True)

if __name__=='__main__':main()
