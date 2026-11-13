"""Freeze small-student controls before teacher admission; uses TRAIN records only."""
import copy,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from notella.core import canonical
from profiles.layertime.decision_contract import inspect_warning_output
folder=Path(__file__).resolve().parent
if (folder/'controls.json').exists():raise ValueError('Preserve frozen controls')
rows=json.loads((ROOT/'experiments/warning-v6-typed-training/development-examples.json').read_text())
train=[e for e in rows if e['split']=='train'];patterns={}
for e in train:patterns.setdefault(e['family'],e)
chosen=['credible-sequence','generic-rf','outage-only','duplicate-reports','outside-window','reversed-order','benign-operations','distant-location']
contract=json.loads((ROOT/'experiments/warning-v5-contracts/contract.json').read_text())
prior={canonical(json.loads(e['input'])) for e in rows}
extra=json.loads((ROOT/'experiments/colibri-teacher-v2-constrained/tasks.json').read_text())['tasks']
prior.update(canonical(dict(observation=c['observation'])) for t in extra for c in t['cases'])
controls=[]
for i,name in enumerate(chosen):
 parent=patterns[name];frame=json.loads(parent['input'])['observation'];window=171000+i*7000
 frame['time']['configuredWindowMs']=window
 if name=='outside-window':frame['time']['delayIntervalMs']=[window+17000,window+17400]
 elif name=='reversed-order':frame['time']['delayIntervalMs']=[-37000-i*1000,-36500-i*1000]
 else:frame['time']['delayIntervalMs']=[27000+i*1100,27360+i*1100]
 text=canonical(dict(observation=frame));assert text not in prior;prior.add(text)
 guard=inspect_warning_output(canonical(parent['target']),dict(eligibleForModel=True,modelInput=frame),contract['outputSchema'],contract['allowedStates']);assert guard['checksPassed']
 controls.append(dict(id='student-v1-control-'+name,family='student-v1-authored-scenario-'+name,split='validation',concepts=parent['concepts'],source=dict(id='student-v1-prospective-development',kind='synthetic',reference=parent['id'],permission='Project-authored synthetic development',labelAuthor='Agent-authored known-pattern reference, not independent field validation',trainingAllowed=False),input=text,target=copy.deepcopy(parent['target'])))
(folder/'controls.json').write_text(json.dumps(controls,indent=2)+'\n')
print(json.dumps(dict(controls=len(controls),exactOverlap=0,controlsSha256=hashlib.sha256((folder/'controls.json').read_bytes()).hexdigest())))
