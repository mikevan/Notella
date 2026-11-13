"""Compare a local teacher on existing development controls; never builds training data."""
import argparse,hashlib,json,sys,time
from pathlib import Path

def main():
 p=argparse.ArgumentParser();p.add_argument('--notella',type=Path,default=Path('C:/workspace/Notella'));p.add_argument('--output',type=Path,required=True);p.add_argument('--model',required=True);p.add_argument('--base-url',default='http://127.0.0.1:8877/v1');p.add_argument('--export-only',action='store_true');a=p.parse_args()
 if a.output.exists():raise ValueError('Preserve previous runs; use a new output directory')
 sys.path.insert(0,str(a.notella))
 from notella import Notella
 from notella.core import canonical
 from notella.teachers import LocalTeacher,teaching_candidate
 from notella.scoring import score_output
 from profiles.layertime.decision_contract import inspect_warning_output
 prepared=json.loads((a.notella/'runtime/warning-v6-typed-training/prepared.json').read_text())
 api=Notella(a.notella/'runtime/warning-v6-typed-training/store');corpus=api.get('curricula',prepared['curriculumId']);ontology=api.get('ontologies',corpus['ontologyId'])
 states=json.loads((a.notella/'experiments/warning-v5-contracts/contract.json').read_text())['allowedStates']
 provider=LocalTeacher(a.model,a.base_url)
 a.output.mkdir(parents=True)
 examples=[ex for ex in corpus['examples'] if ex['split']=='validation']
 manifest=dict(curriculumId=prepared['curriculumId'],ontologyId=corpus['ontologyId'],model=a.model,baseUrl=a.base_url,
  evaluatorSha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),cases=[dict(id=ex['id'],messages=ex['messages'][:-1],expected=json.loads(ex['messages'][-1]['content'])) for ex in examples],
  limits=['Existing synthetic development controls; not independent evaluation.','Not a matched engine benchmark: teacher architecture, weights and runtime differ.','Targets are scoring references only and are never sent to the teacher.','No output repair, training, admission or phone qualification.'])
 (a.output/'manifest.json').write_text(json.dumps(manifest,indent=2))
 results=[]
 if not a.export_only:
  for i,ex in enumerate(examples):
   started=time.monotonic()
   try:
    candidate=teaching_candidate(provider,corpus['ontologyId'],ex['concepts'],ex['messages'][:-1],a.output/f'case-{i:02d}',max_tokens=384)
    text=candidate['output'];target=json.loads(ex['messages'][-1]['content'])
    score=score_output(text,target,ontology['outputSchema'],['posture','combinedTrigger','evidenceClass'])
    frame=json.loads(ex['messages'][-2]['content'])['observation']
    guard=inspect_warning_output(text,dict(eligibleForModel=True,modelInput=frame),ontology['outputSchema'],states)
    result=dict(id=ex['id'],seconds=time.monotonic()-started,candidateId=candidate['resultId'],score=score,guard=guard,output=text,finishReason=candidate.get('finishReason'))
   except Exception as e:result=dict(id=ex['id'],seconds=time.monotonic()-started,errorType=type(e).__name__,error=str(e))
   results.append(result)
   report=dict(model=a.model,curriculumId=prepared['curriculumId'],total=len(examples),completed=len(results),
    schemaPasses=sum(r.get('score',{}).get('schemaValid',False) for r in results),decisionMatches=sum(r.get('score',{}).get('decisionFieldsMatch',False) for r in results),
    guardPasses=sum(r.get('guard',{}).get('checksPassed',False) for r in results),errors=sum('error' in r for r in results),results=results,fieldQualified=False)
   (a.output/'report.json').write_text(json.dumps(report,indent=2))
   print(json.dumps({k:v for k,v in report.items() if k!='results'}),flush=True)
 print(json.dumps(dict(exportOnly=a.export_only,cases=len(examples),completed=len(results),output=str(a.output))),flush=True)
if __name__=='__main__':main()
