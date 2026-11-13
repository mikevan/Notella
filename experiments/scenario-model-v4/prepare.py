"""Freeze a 20-row curriculum repair; retain known diagnostics, add fresh cases."""
import copy,hashlib,json,sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from notella import Notella
from notella.core import canonical,fingerprint
from notella.scenarios import validate_scenario_set,compile_scenario_examples
from profiles.network_scenarios.reference import rule_state,POLICY_ID
HERE=Path(__file__).resolve().parent; RUN=ROOT/'runtime/scenario-model-v4'
O=json.loads((ROOT/'experiments/scenario-model-v1/ontology.json').read_text(encoding='utf-8'))

def event(identity,concept,t,asset,**extra):
 return dict(id=identity,concept=concept,assetRef=asset,timeMs=t,uncertaintyMs=80,availableAtMs=t+200,sourceRoot='source:'+identity,originEventId='origin:'+identity,statement='Synthetic supplied '+concept+' for '+asset,**extra)

def scenario(identity,events,primary,split='train',clock='shared-clock-asserted'):
 s=dict(formatVersion='notella.scenario.v1',id=identity,family='repair-authoring-suite-001' if split=='train' else identity+'-fresh-family',split=split,ontologyId=fingerprint(O),policyId=POLICY_ID,primaryAsset=primary,assets=sorted({primary}|{e['assetRef'] for e in events}),timeBasis=clock,evidence=events,source=dict(id=identity,kind='synthetic',reference='scenario-model-v4/prepare.py',permission='Owner-authorized curriculum repair; synthetic assertions',labelAuthor='Codex author/reviewer against unchanged rule reference; not independent',trainingAllowed=split=='train'),steps=[])
 for cutoff in sorted({e['availableAtMs'] for e in events}):
  state=rule_state(s,cutoff)
  visible=[e for e in events if e['availableAtMs']<=cutoff];new=[e for e in visible if e['availableAtMs']==cutoff]
  if any(e.get('retracts') for e in new):
   state['change']['summary']='Apply the new retraction to its originating event and all reposts, then reassess remaining primary-asset support. '+state['assessment']['rationale']
  elif any(e.get('explains') for e in new):
   state['change']['summary']='The new explanation covers only its explicit references; it cannot clear a separate current compromise. '+state['assessment']['rationale']
  elif any(e['concept']=='compromise_evidence' and e['assetRef']==primary for e in new):
   state['change']['summary']='Current reviewed primary-asset compromise is sufficient without a scan/authentication prerequisite. Reposts do not add independent support. '+state['assessment']['rationale']
  else: state['change']['summary']='Interpret the newly available observations under asset scope and rule precedence. '+state['assessment']['rationale']
  s['steps'].append(dict(asOfMs=cutoff,target=state))
 return s

def build():
 out=[]
 a='router-K'; c=event('k8','compromise_evidence',8000,a);out.append(scenario('R-101',[c,event('k9','source_correction',14000,a,retracts=['k8'])],a))
 a='gateway-M';c=event('m4','compromise_evidence',40000,a);r=copy.deepcopy(c);r.update(id='m6',availableAtMs=46000)
 out.append(scenario('R-206',[c,r,event('m8','source_correction',51000,a,retracts=['m6'])],a))
 a='service-P'; sc=event('p2','reconnaissance',70000,a);au=event('p4','credential_activity',74000,a)
 out.append(scenario('R-309',[sc,au,event('p7','benign_operation',79000,a,explains=['p2','p4']),event('p9','compromise_evidence',83000,a),event('p11','benign_operation',89000,a,explains=['p2','p4'])],a))
 a='relay-V';out.append(scenario('R-412',[event('v5','compromise_evidence',110000,a),event('v8','reconnaissance',117000,'relay-W')],a))
 a='device-F';out.append(scenario('R-515',[event('f2','credential_activity',150000,a)],a))
 a='host-J';out.append(scenario('R-618',[event('j3','reconnaissance',180000,a),event('j5','credential_activity',185000,a),event('j7','compromise_evidence',190000,a),event('j9','source_correction',196000,a,retracts=['j7'])],a))
 a='endpoint-Z';out.append(scenario('R-721',[event('z1','credential_activity',220000,a),event('z4','benign_operation',226000,a,explains=['z1']),event('z8','compromise_evidence',233000,a)],a))
 # Fresh evaluation structures: do not reuse the inspected diagnostic trajectories.
 a='node-U';fresh1=scenario('V-834',[event('u2','compromise_evidence',300000,a),event('u5','compromise_evidence',307000,'node-T'),event('u7','source_correction',313000,a,retracts=['u2']),event('u9','source_correction',320000,'node-T',retracts=['u5'])],a,'validation')
 a='sensor-B';fresh2=scenario('V-947',[event('b3','reconnaissance',360000,a),event('b6','compromise_evidence',367000,a),event('b8','benign_operation',373000,a,explains=['b3']),event('b9','source_correction',379000,a,retracts=['b6'])],a,'validation')
 return out,[fresh1,fresh2]

def main():
 if (RUN/'prepared.json').exists():raise ValueError('Preserve prepared run')
 train,fresh=build();known=json.loads((ROOT/'experiments/scenario-model-v1/development-scenarios.json').read_text(encoding='utf-8'))
 evaluation=known+fresh; receipt=validate_scenario_set(O,train+evaluation)
 trainrows=compile_scenario_examples(O,train);valrows=compile_scenario_examples(O,evaluation)
 normalized=[]
 for r in trainrows+valrows:
  f=json.loads(r['input']);f['scenarioId']='S-'+fingerprint(f['scenarioId'])[:12];r['input']=canonical(f)
  if r['split']=='train':
   n=copy.deepcopy(f);n.pop('scenarioId');normalized.append(fingerprint(n))
 assert len(trainrows)==20 and len(set(normalized))==20
 assert not ({r['input'] for r in trainrows}&{r['input'] for r in valrows})
 # Explicit semantic assertions supplement schema/contract review.
 expected=[['critical','contextual'],['critical','critical','contextual'],['contextual','high','contextual','critical','critical'],['critical','critical'],['contextual'],['contextual','high','critical','high'],['contextual','contextual','critical']]
 assert [[t['target']['assessment']['criticality'] for t in s['steps']] for s in train]==expected
 assert [[t['target']['assessment']['criticality'] for t in s['steps']] for s in fresh]==[['critical','critical','contextual','contextual'],['contextual','critical','critical','contextual']]
 RUN.mkdir(parents=True,exist_ok=True)
 for name,value in [('ontology.json',O),('training-scenarios.json',train),('development-scenarios.json',evaluation),('fresh-evaluation.json',fresh),('validation-receipt.json',receipt)]:
  (HERE/name).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
 review=dict(reviewer=dict(name='Codex',independent=False),trainingAdmission=True,ruleReferenceUnchanged=True,ontologyUnchanged=True,trainingRows=20,uniqueTrainingPrefixes=20,trainingTemplates=7,trainingAuthoredFamilies=1,labels=dict(Counter(r['target']['assessment']['criticality'] for r in trainrows)),knownDiagnosticPrefixes=10,freshEvaluationPrefixes=8,checks=['Explicit criticality trajectories asserted against unchanged rule reference','Retractions invalidate originating events and reposts','Scoped benign explanations do not clear separate compromise','New training events/identities/contexts; no copied development outputs','Same-author synthetic motifs, not independent field evidence; known diagnostic semantic motifs are now intentionally taught through new contrasts'])
 (HERE/'review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
 api=Notella(RUN/'store');oid=api.register_ontology(O)['id'];cid=api.compile(oid,trainrows+valrows)['id'];pid=api.plan(cid,'qwen3-4b',steps=80,rank=16,learning_rate=0.0001)['id']
 prepared=dict(ontologyId=oid,curriculumId=cid,planId=pid,trainingRows=20,validationRows=18,trainingFamilies=1,validationFamilies=4,evaluationSha256=hashlib.sha256((HERE/'development-scenarios.json').read_bytes()).hexdigest(),model='C:/workspace/TUltra-Project/LayerTime/tools/ai-training/models/qwen3-4b-instruct-2507')
 (RUN/'prepared.json').write_text(json.dumps(prepared,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(prepared=prepared,review=review),indent=2))
if __name__=='__main__':main()
