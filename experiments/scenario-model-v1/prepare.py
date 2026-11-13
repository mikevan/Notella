"""Freeze scenario review, explicit admission and new evaluation families before training."""
import copy,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from notella import Notella
from notella.core import canonical,fingerprint
from notella.scenarios import validate_scenario_set,compile_scenario_examples
from profiles.network_scenarios.reference import rule_state,POLICY_ID

def narrative(s,cutoff):
 state=rule_state(s,cutoff);visible=[e for e in s['evidence'] if e['availableAtMs']<=cutoff];latest=max(e['availableAtMs'] for e in visible);new=[e for e in visible if e['availableAtMs']==latest]
 if any(e.get('retracts') for e in new):why='The newly available correction withdraws the originating access observation and all its reposts. Reassess remaining evidence; retain withdrawn nodes and inactive support.'
 elif all(e['assetRef']!=s['primaryAsset'] for e in new):why='The new evidence concerns another asset. Preserve its observation but do not add a link to the primary-asset hypothesis without an explicit bridge.'
 elif any(e.get('explains') for e in new):
  why='The new scoped benign explanation covers its referenced observations. It cannot negate a separate current reviewed compromise assertion.' if state['assessment']['criticality']=='critical' else 'The new scoped benign explanation covers the scan/authentication observations; their joint suspicious interpretation is weakened.'
 elif any(e['originEventId'] in {p['originEventId'] for p in visible if p['availableAtMs']<latest} for e in new):why='The new report repeats an originating observation already present. Report count increases without another underlying observation or provenance root; repetition alone does not escalate criticality.'
 elif s['timeBasis']=='unresolved':why='Occurrence clocks are not established as comparable. No precedence edge is justified; an otherwise relevant scan/authentication pair requires review.'
 elif len(visible)>1 and any(e['timeMs']<max(p['timeMs'] for p in visible if p['id']!=e['id']) for e in new):why='This newly available observation occurred earlier. Update current knowledge at arrival time without inventing a later occurrence or leaking it into previous prefixes.'
 else:why=state['assessment']['rationale']
 state['change']['summary']=why;return state

def main():
 folder=Path(__file__).resolve().parent;out=ROOT/'runtime/scenario-model-v1'
 if (out/'prepared.json').exists():raise ValueError('Preserve prepared experiment')
 o=json.loads((ROOT/'profiles/network_scenarios/ontology.json').read_text(encoding='utf-8'));training=json.loads((ROOT/'profiles/network_scenarios/scenarios.json').read_text(encoding='utf-8'))
 def event(i,c,t,arrival=None,asset='server-Q',**extra):return dict(id=i,concept=c,assetRef=asset,timeMs=t,uncertaintyMs=80,availableAtMs=t+100 if arrival is None else arrival,sourceRoot='reviewed-origin:'+c,originEventId='origin:'+i,statement='Synthetic supplied '+c+' for '+asset,**extra)
 def scenario(i,family,events):
  s=dict(formatVersion='notella.scenario.v1',id=i,family=family,split='validation',ontologyId=fingerprint(o),policyId=POLICY_ID,primaryAsset='server-Q',assets=['server-Q','server-R'],timeBasis='shared-clock-asserted',source=dict(id='scenario-model-v1-development',kind='synthetic',reference='scenario-model-v1/prepare.py',permission='Project-authored synthetic development',labelAuthor='Codex agent and explicit rule reference, not independent review',trainingAllowed=False),evidence=events,steps=[])
  s['steps']=[dict(asOfMs=t,target=narrative(s,t)) for t in sorted({e['availableAtMs'] for e in events})];return s
 events=[event('r17','compromise_evidence',10000,12000),event('r21','reconnaissance',9000,15000),event('r26','credential_activity',11000,16000),event('r32','benign_operation',20000,explains=['r21','r26']),event('r39','source_correction',25000,retracts=['r17'])]
 first=scenario('S-Q71','compromise-first-scoped-benign-original',events)
 auth=event('r44','credential_activity',40000);other=event('r51','reconnaissance',30000,42000,asset='server-R');access=event('r57','compromise_evidence',50000);repost=copy.deepcopy(access);repost['id']='r63';repost['availableAtMs']=52000
 second=scenario('S-Q92','reposted-compromise-unrelated-asset-original',[auth,other,access,repost,event('r68','source_correction',55000,retracts=['r57'])])
 evaluation=[first,second]
 # Explicit review/admission applies to this copy, not the original unadmitted fixtures.
 originals=copy.deepcopy(training)
 for s in training:
  for step in s['steps']:step['target']=narrative(s,step['asOfMs'])
  s['source'].update(trainingAllowed=True,permission='Explicit development admission under owner-authorized scenario training',labelAuthor='Codex agent review against proposed policy; not independent domain validation',reference='scenario-model-v1/review.json')
 receipt=validate_scenario_set(o,training+evaluation)
 trainrows=compile_scenario_examples(o,training);valrows=compile_scenario_examples(o,evaluation)
 def opaque(row):
  frame=json.loads(row['input']);frame['scenarioId']='S-'+fingerprint(frame['scenarioId'])[:12];row['input']=canonical(frame);return row
 rows=[opaque(r) for r in trainrows+valrows]
 assert not ({r['input'] for r in rows if r['split']=='train'}&{r['input'] for r in rows if r['split']=='validation'})
 out.mkdir(parents=True,exist_ok=True)
 review=dict(reviewer=dict(name='Codex',kind='agent',independent=False),policyId=POLICY_ID,ontologyId=fingerprint(o),reviewPassed=True,trainingAdmission=True,
  scope='Agent review of supplied classifications and proposed policy, not source authenticity or field truth.',checks=['All prefixes obey arrival-time visibility and preserve source corrections.','Report deduplication does not add underlying observations.','No cross-asset bridge is asserted.','Reference rule criticality is internally consistent with the proposed policy.','Changed summaries explain new evidence rather than merely repeat labels.','All source branches remain in one family/split; evaluation has different authored trajectories.'],originalTrainingSha256=fingerprint(originals),reviewedTrainingSha256=fingerprint(training),explanationChangesOnly=True)
 (folder/'review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
 for name,data in [('ontology.json',o),('training-scenarios.json',training),('development-scenarios.json',evaluation),('validation-receipt.json',receipt)]:
  (folder/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 api=Notella(out/'store');oid=api.register_ontology(o)['id'];cid=api.compile(oid,rows)['id'];pid=api.plan(cid,'qwen3-4b',steps=80,rank=16,learning_rate=0.0001)['id']
 prepared=dict(ontologyId=oid,curriculumId=cid,planId=pid,trainingRows=len(trainrows),validationRows=len(valrows),trainingFamilies=len({s['family'] for s in training}),validationFamilies=len(evaluation),evaluationSha256=hashlib.sha256((folder/'development-scenarios.json').read_bytes()).hexdigest(),model='C:/workspace/TUltra-Project/LayerTime/tools/ai-training/models/qwen3-4b-instruct-2507')
 (out/'prepared.json').write_text(json.dumps(prepared,indent=2)+'\n');print(json.dumps(prepared),flush=True)
if __name__=='__main__':main()
