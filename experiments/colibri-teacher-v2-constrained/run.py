"""Run frozen constrained teaching requests; preserve, score and never auto-admit."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from notella.core import canonical,check,validate_schema
from notella.teachers import LocalTeacher,teaching_candidate
from notella.scoring import score_output
from profiles.layertime.decision_contract import inspect_warning_output

def main():
 folder=Path(__file__).resolve().parent;tasks=json.loads((folder/'tasks.json').read_text())['tasks']
 ontology=json.loads((ROOT/'experiments/warning-v6-typed-training/ontology.json').read_text())
 contract=json.loads((ROOT/'experiments/warning-v5-contracts/contract.json').read_text())
 oid=hashlib.sha256(canonical(ontology).encode()).hexdigest();out=ROOT/'runtime/teacher-constrained-v2'
 out.mkdir(parents=True,exist_ok=True)
 if (out/'summary.json').exists():raise ValueError('Preserve completed batch')
 provider=LocalTeacher('notella-teacher-qwen36','http://127.0.0.1:8877/v1')
 policy='These are synthetic supplied facts, not verified field events. Use only the supplied classifications. Critical/met/corroborated_drone requires ALL of ongoingThreat=true, disruption.classification=reviewed_deliberate_disruption, drone.classification=corroborated_drone_identity, sourceLineage.relationship=distinct_reviewed_origins for the DRONE reports, matching areaRef, time.order=after, withinWindow=true. outage_cause_unknown instead requires high/unconfirmed/cause_unresolved. unidentified_rf instead requires high/unconfirmed/unidentified_signal. shared_origin instead requires high/unconfirmed/dependent_reports. Separate asserted roots are not proof of statistical independence. No answer establishes causation, perpetrator or attack probability.'
 schema=dict(type='object',additionalProperties=False,required=['answers','contrast'],properties=dict(answers=dict(type='array',minItems=2,maxItems=2,items=dict(type='object',additionalProperties=False,required=['id','decision','reason'],properties=dict(id=dict(type='string',enum=['A','B']),decision=ontology['outputSchema'],reason=dict(type='string',minLength=1,maxLength=420)))),contrast=dict(type='string',minLength=1,maxLength=420)))
 results=[]
 for task in tasks:
  public=[dict(id=c['id'],observation=c['observation']) for c in task['cases']]
  messages=[dict(role='system',content=policy),dict(role='user',content=canonical(dict(task='Evaluate both fixed observations without changing facts. Explain the single changed factor. Return only JSON matching this schema. Keep each reason under 45 words; keep contrast under 45 words.',schema=schema,cases=public)))]
  candidate=teaching_candidate(provider,oid,[task['concept'],'warning_posture','causal_claim'],messages,out/task['id'],max_tokens=640)
  item=dict(id=task['id'],candidateResultId=candidate['resultId'],seconds=candidate['seconds'],finishReason=candidate['finishReason'],formatValid=False,decisionMatches=0,guardPasses=0,admittedForTraining=False,cases=[])
  try:
   def unique(pairs):
    check(len({k for k,_ in pairs})==len(pairs),'Duplicate JSON key');return dict(pairs)
   value=json.loads(candidate['output'],object_pairs_hook=unique);validate_schema(value,schema)
   check({a['id'] for a in value['answers']}=={'A','B'},'Missing or duplicate case id');item['formatValid']=True
   for c in task['cases']:
    answer=next(a for a in value['answers'] if a['id']==c['id']);text=canonical(answer['decision'])
    score=score_output(text,c['expected'],ontology['outputSchema'],['posture','combinedTrigger','evidenceClass'])
    guard=inspect_warning_output(text,c['projection'],ontology['outputSchema'],contract['allowedStates'])
    item['cases'].append(dict(id=c['id'],score=score,guard=guard,reason=answer['reason']))
   item['decisionMatches']=sum(c['score']['decisionFieldsMatch'] for c in item['cases']);item['guardPasses']=sum(c['guard']['checksPassed'] for c in item['cases']);item['contrast']=value['contrast']
  except (ValueError,TypeError,KeyError,StopIteration) as e:item['error']=str(e)
  results.append(item)
  (out/'progress.json').write_text(json.dumps(dict(results=results),indent=2)+'\n')
  print(json.dumps({k:v for k,v in item.items() if k not in ('cases','contrast')}),flush=True)
 summary=dict(formatVersion='notella.constrained-teacher-diagnostic.v1',tasksSha256=hashlib.sha256((folder/'tasks.json').read_bytes()).hexdigest(),runnerSha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),totalPairs=3,totalCases=6,formatValidPairs=sum(r['formatValid'] for r in results),decisionMatches=sum(r['decisionMatches'] for r in results),guardPasses=sum(r['guardPasses'] for r in results),results=results,reviewStatus='pending',trainingExamplesAdmitted=0,fieldQualified=False)
 (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({k:v for k,v in summary.items() if k!='results'}),flush=True)
if __name__=='__main__':main()
