"""Freeze a 20-row curriculum repair; retain known diagnostics, add fresh cases."""
import copy,hashlib,json,sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from notella import Notella
from notella.core import canonical,fingerprint
from notella.scenarios import validate_scenario_set,compile_scenario_examples
from profiles.network_scenarios.reference import rule_state,POLICY_ID
HERE=Path(__file__).resolve().parent; RUN=ROOT/'runtime/scenario-model-v5'
O=json.loads((ROOT/'experiments/scenario-model-v1/ontology.json').read_text(encoding='utf-8'))

def event(identity,concept,t,asset,**extra):
 return dict(id=identity,concept=concept,assetRef=asset,timeMs=t,uncertaintyMs=80,availableAtMs=t+200,sourceRoot='source:'+identity,originEventId='origin:'+identity,statement='Synthetic supplied '+concept+' for '+asset,**extra)

def scenario(identity,events,primary,split='train',clock='shared-clock-asserted'):
 s=dict(formatVersion='notella.scenario.v1',id=identity,family='retraction-authoring-suite-001' if split=='train' else identity+'-fresh-family',split=split,ontologyId=fingerprint(O),policyId=POLICY_ID,primaryAsset=primary,assets=sorted({primary}|{e['assetRef'] for e in events}),timeBasis=clock,evidence=events,source=dict(id=identity,kind='synthetic',reference='scenario-model-v5/prepare.py',permission='Owner-authorized curriculum repair; synthetic assertions',labelAuthor='Codex author/reviewer against unchanged rule reference; not independent',trainingAllowed=split=='train'),steps=[])
 for cutoff in sorted({e['availableAtMs'] for e in events}):
  if not any(e['assetRef']==primary and e['availableAtMs']<=cutoff for e in events):continue
  state=rule_state(s,cutoff)
  visible=[e for e in events if e['availableAtMs']<=cutoff];new=[e for e in visible if e['availableAtMs']==cutoff]
  withdrawn={next(p['originEventId'] for p in visible if p['id']==identity) for e in visible for identity in e.get('retracts',[])}
  current=[e['id'] for e in visible if e['concept']=='compromise_evidence' and e['assetRef']==primary and e['originEventId'] not in withdrawn]
  retired=[e['id'] for e in visible if e['concept']=='compromise_evidence' and e['assetRef']==primary and e['originEventId'] in withdrawn]
  c=', '.join(current) or 'none'; r=', '.join(retired) or 'none'; level=state['assessment']['criticality']
  style=sum(map(ord,s['id']))%3
  if level=='critical':
   choices=[f'Primary-asset access support remains in {c}; withdrawn reports ({r}) are excluded.',f'Current reviewed primary compromise: {c}. Retired access assertions: {r}. The current support warrants critical.',f'{c} supplies active primary access evidence independently of the retired assertions {r}.']
  elif level=='high':
   choices=[f'Access reports {r} are withdrawn; the remaining primary scan/authentication sequence supports high concern.',f'No active compromise remains. The primary scan-to-credential link still holds after retiring {r}.',f'Retire {r} from compromise support; keep the surviving primary scan/auth association, assessed high.']
  else:
   choices=[f'No active primary compromise or qualifying scan/auth association remains; {r} is historical, not current support.',f'Primary access support is absent after excluding {r}; remaining evidence is contextual.',f'With {r} retired and no supported primary scan/auth pair, contextual assessment follows.']
  state['assessment']['rationale']=choices[style]
  if any(e.get('retracts') for e in new):
   targets=[identity for e in new for identity in e.get('retracts',[])];origins={next(p['originEventId'] for p in visible if p['id']==identity) for identity in targets}
   affected=[e['id'] for e in visible if e['originEventId'] in origins]
   state['change']['summary']='Correction '+','.join(e['id'] for e in new)+' withdraws reports '+','.join(affected)+' by originating event; preserve their retired history.'
  elif any(e.get('explains') for e in new):state['change']['summary']='Explanation '+','.join(e['id'] for e in new)+' covers only its named reports; reassess separate active support.'
  else:state['change']['summary']='Newly available reports '+','.join(e['id'] for e in new)+' update the evidence state; report multiplicity does not imply independence.'
  s['steps'].append(dict(asOfMs=cutoff,target=state))
 return s

def build():
 out=[]
 def add(identity,events,asset,indices,expected):
  s=scenario(identity,events,asset);s['steps']=[s['steps'][i] for i in indices]
  assert [t['target']['assessment']['criticality'] for t in s['steps']]==expected
  out.append(s)
 a='appliance-L';add('N-110',[event('l1','compromise_evidence',5000,a),event('l8','source_correction',13000,a,retracts=['l1'])],a,[0,1],['critical','contextual'])
 a='bridge-D';c=event('d2','compromise_evidence',27000,a);rep=copy.deepcopy(c);rep.update(id='d6',availableAtMs=33000)
 add('N-220',[c,rep,event('d9','source_correction',39000,a,retracts=['d2'])],a,[1,2],['critical','contextual'])
 a='service-H';add('N-330',[event('h1','reconnaissance',50000,a),event('h2','credential_activity',55000,a),event('h3','compromise_evidence',61000,a),event('h8','source_correction',69000,a,retracts=['h3'])],a,[2,3],['critical','high'])
 a='terminal-G';add('N-440',[event('g1','reconnaissance',80000,a),event('g2','credential_activity',85000,a),event('g3','benign_operation',90000,a,explains=['g1','g2']),event('g5','compromise_evidence',97000,a),event('g9','source_correction',104000,a,retracts=['g5'])],a,[3,4],['critical','contextual'])
 a='station-E';add('N-550',[event('e1','compromise_evidence',120000,'station-R'),event('e2','reconnaissance',125000,'station-R'),event('e3','compromise_evidence',131000,a),event('e8','source_correction',138000,a,retracts=['e3'])],a,[0,1],['critical','contextual'])
 a='host-C';add('N-660',[event('c1','compromise_evidence',150000,a),event('c4','compromise_evidence',157000,a),event('c8','source_correction',164000,a,retracts=['c1'])],a,[1,2],['critical','critical'])
 a='endpoint-Q';add('N-770',[event('q1','compromise_evidence',180000,a),event('q3','compromise_evidence',187000,a),event('q6','source_correction',194000,a,retracts=['q3']),event('q9','source_correction',201000,a,retracts=['q1'])],a,[2,3],['critical','contextual'])
 a='gateway-S';add('N-880',[event('s1','credential_activity',220000,a),event('s2','compromise_evidence',225000,a),event('s3','compromise_evidence',231000,'gateway-T'),event('s8','source_correction',239000,'gateway-T',retracts=['s3'])],a,[2,3],['critical','critical'])
 a='router-W';add('N-990',[event('w1','reconnaissance',260000,a),event('w2','credential_activity',265000,a),event('w3','compromise_evidence',271000,a),event('w6','source_correction',278000,a,retracts=['w3']),event('w9','benign_operation',285000,a,explains=['w1','w2'])],a,[3,4],['high','contextual'])
 a='relay-A';add('N-1010',[event('a1','compromise_evidence',300000,a),event('a4','source_correction',308000,a,retracts=['a1']),event('a9','compromise_evidence',316000,a)],a,[1,2],['contextual','critical'])
 a='sensor-X';f1=scenario('F-1120',[event('x1','compromise_evidence',410000,a),event('x4','compromise_evidence',418000,'sensor-Z'),event('x9','source_correction',427000,'sensor-Z',retracts=['x4'])],a,'validation')
 a='node-Y';f2=scenario('F-1230',[event('y2','compromise_evidence',460000,a),event('y5','source_correction',469000,a,retracts=['y2']),event('y8','credential_activity',477000,a)],a,'validation')
 assert [[t['target']['assessment']['criticality'] for t in s['steps']] for s in [f1,f2]]==[['critical','critical','critical'],['critical','contextual','contextual']]
 return out,[f1,f2]

def main():
 if (RUN/'prepared.json').exists():raise ValueError('Preserve prepared run')
 train,fresh=build();known=json.loads((ROOT/'experiments/scenario-model-v4/development-scenarios.json').read_text(encoding='utf-8'))
 evaluation=known+fresh;receipt=validate_scenario_set(O,train+evaluation)
 tr=compile_scenario_examples(O,train);va=compile_scenario_examples(O,evaluation);normalized=[]
 for row in tr+va:
  frame=json.loads(row['input']);frame['scenarioId']='S-'+fingerprint(frame['scenarioId'])[:12];row['input']=canonical(frame)
  if row['split']=='train':
   frame.pop('scenarioId');normalized.append(fingerprint(frame))
 assert len(tr)==20 and len(set(normalized))==20
 assert not ({r['input'] for r in tr}&{r['input'] for r in va})
 # Explicit review: generic contract cannot alone establish correct domain labels.
 for s in train:
  for step in s['steps']:
   reference=rule_state(s,step['asOfMs']);assert step['target']['assessment']['criticality']==reference['assessment']['criticality']
   assert step['target']['assessment']['rationale']!=step['target']['change']['summary']
 RUN.mkdir(parents=True,exist_ok=True)
 for name,value in [('ontology.json',O),('training-scenarios.json',train),('development-scenarios.json',evaluation),('fresh-evaluation.json',fresh),('validation-receipt.json',receipt)]:
  (HERE/name).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
 review=dict(reviewer=dict(name='Codex',independent=False),trainingAdmission=True,trainingRows=20,uniqueTrainingPrefixes=20,trainingTemplates=10,trainingAuthoredFamilies=1,labels=dict(Counter(r['target']['assessment']['criticality'] for r in tr)),knownDiagnosticPrefixes=18,freshPrefixes=6,ontologyAndRuleUnchanged=True,intervention=['More before/after correction contrasts, including surviving independent compromise and remaining high/contextual support','Scope is explicit in short fact-specific rationales with current and retired IDs','Change summaries describe the update without repeating assessment rationale','Selected before/after prefixes; no copied evaluation outputs or targets'],limits=['Same-author synthetic motifs informed by inspected failures, not independent validation','No change to decoder, output format, input representation, loss or training settings'])
 (HERE/'review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
 api=Notella(RUN/'store');oid=api.register_ontology(O)['id'];cid=api.compile(oid,tr+va)['id'];pid=api.plan(cid,'qwen3-4b',steps=80,rank=16,learning_rate=0.0001)['id']
 prepared=dict(ontologyId=oid,curriculumId=cid,planId=pid,trainingRows=20,validationRows=24,trainingFamilies=1,validationFamilies=6,evaluationSha256=hashlib.sha256((HERE/'development-scenarios.json').read_bytes()).hexdigest(),model='C:/workspace/TUltra-Project/LayerTime/tools/ai-training/models/qwen3-4b-instruct-2507')
 (RUN/'prepared.json').write_text(json.dumps(prepared,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(prepared=prepared,review=review),indent=2))
if __name__=='__main__':main()
