"""Run the frozen robustness pair after primary generation has completed."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from notella import Notella
from notella.scoring import score_output

def main():
 primary=ROOT/'runtime/warning-v4-expanded';robust=ROOT/'runtime/warning-v4-robustness'
 comparison=json.loads((primary/'comparison.json').read_text())
 adapter=primary/'store/jobs'/comparison['jobId']/'adapter';model=Path(os.environ['NOTELLA_EXPERIMENT_MODEL'])
 if (robust/'comparison.json').exists():raise ValueError('Preserve completed robustness comparison')
 for name in ('base','adapted'):
  command=[sys.executable,str(Path(__file__).with_name('evaluate_robustness.py')),'--model',str(model),'--output',str(robust/(name+'-validation.json'))]
  if name=='adapted':command+=['--adapter',str(adapter)]
  with (robust/(name+'-evaluation.stdout.log')).open('xb') as stdout,(robust/(name+'-evaluation.stderr.log')).open('xb') as stderr:
   subprocess.run(command,check=True,stdout=stdout,stderr=stderr)
  print(name+' robustness evaluation complete',flush=True)
 summaries={}
 for group,folder in [('primary',primary),('robustness',robust)]:
  prepared=json.loads((folder/'prepared.json').read_text());api=Notella(folder/'store');corpus=api.get('curricula',prepared['curriculumId']);ontology=api.get('ontologies',corpus['ontologyId'])
  targets={r['id']:json.loads(r['messages'][-1]['content']) for r in corpus['examples'] if r['split']=='validation'}
  reports={name:json.loads((folder/(name+'-validation.json')).read_text()) for name in ('base','adapted')}
  assert [r['promptSha256'] for r in reports['base']['results']]==[r['promptSha256'] for r in reports['adapted']['results']]
  assert reports['base']['baseIntakeManifestSha256']==reports['adapted']['baseIntakeManifestSha256']
  assert reports['base']['evaluatorSha256']==reports['adapted']['evaluatorSha256']
  summaries[group]={}
  for name,report in reports.items():
   scores=[dict(id=r['id'],outputSha256=r['outputSha256'],score=score_output(r['output'],targets[r['id']],ontology['outputSchema'],['posture','combinedTrigger','evidenceClass'])) for r in report['results']]
   summaries[group][name]=dict(total=len(scores),schemaPasses=sum(s['score']['schemaValid'] for s in scores),
     decisionMatches=sum(s['score']['decisionFieldsMatch'] for s in scores),compliantMatches=sum(s['score']['schemaAndDecisionMatch'] for s in scores),cases=scores)
 result=dict(jobId=comparison['jobId'],matchedPrompts=True,scoreFields=['posture','combinedTrigger','evidenceClass'],
  scoringSourceSha256=hashlib.sha256((ROOT/'notella/scoring.py').read_bytes()).hexdigest(),groups=summaries,
  semanticAccuracyMeasured=False,fieldQualification=False,releaseEligible=False)
 (robust/'comparison.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({group:{name:{k:v for k,v in values.items() if k!='cases'} for name,values in conditions.items()} for group,conditions in summaries.items()},indent=2),flush=True)

if __name__=='__main__':main()
