"""Prospective single-factor contrasts; reference decisions are not sent to teacher."""
import argparse,copy,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from notella.core import canonical
from profiles.layertime.decision_contract import project_observation
from profiles.layertime.temporal_features import SHARED_CLOCK

def main():
 folder=Path(__file__).resolve().parent
 if (folder/'tasks.json').exists():raise ValueError('Preserve frozen tasks')
 registry={'visual':dict(originRef='visual-root',reviewed=True),'acoustic':dict(originRef='acoustic-root',reviewed=True),'relay-one':dict(originRef='common-root',reviewed=True),'relay-two':dict(originRef='common-root',reviewed=True)}
 base=dict(timeBasis=SHARED_CLOCK,linkingWindowMs=88000,disruption=dict(kind='credible independently reviewed deliberate Wi-Fi denial of service',location='camp-area',timeMs=2300000,uncertaintyMs=120),drone=dict(kind='corroborated drone presence',location='camp-area',timeMs=2323500,uncertaintyMs=160,sources=['visual','acoustic']))
 critical=dict(posture='critical',combinedTrigger='met',evidenceClass='corroborated_drone')
 specs=[('disruption_identity',23500,88000,dict(posture='high',combinedTrigger='unconfirmed',evidenceClass='cause_unresolved')),('source_independence',37500,110000,dict(posture='high',combinedTrigger='unconfirmed',evidenceClass='dependent_reports')),('signal_identity',42500,135000,dict(posture='high',combinedTrigger='unconfirmed',evidenceClass='unidentified_signal'))]
 tasks=[];seen=set()
 prior=json.loads((ROOT/'experiments/warning-v6-typed-training/development-examples.json').read_text())
 prior_inputs={canonical(json.loads(e['input'])) for e in prior}
 for index,(concept,delay,window,target) in enumerate(specs):
  before=copy.deepcopy(base);before['linkingWindowMs']=window;before['drone']['timeMs']=before['disruption']['timeMs']+delay
  after=copy.deepcopy(before)
  if concept=='disruption_identity':after['disruption']['kind']='Wi-Fi outage; cause unknown'
  elif concept=='source_independence':after['drone']['sources']=['relay-one','relay-two']
  else:after['drone']['kind']='unidentified RF signature; drone classifier uncertain'
  cases=[]
  for label,obs,expected in [('A',before,critical),('B',after,target)]:
   projection=project_observation(obs,registry,True)
   assert projection['eligibleForModel']
   text=canonical(dict(observation=projection['modelInput']))
   assert text not in prior_inputs and text not in seen
   seen.add(text)
   cases.append(dict(id=label,observation=projection['modelInput'],projection=projection,expected=expected,inputSha256=hashlib.sha256(text.encode()).hexdigest()))
  tasks.append(dict(id=f'contrast-{index+1}',concept=concept,cases=cases))
 artifact=dict(tasks=tasks,registry=registry,overlapAudit=dict(priorV6Inputs=len(prior_inputs),newInputs=len(seen),exactOverlap=0),scope='Agent-authored synthetic development contrasts using known policy patterns; not independent evaluation or automatic training admission.')
 (folder/'tasks.json').write_text(json.dumps(artifact,indent=2)+'\n')
 print(json.dumps(artifact['overlapAudit']))
if __name__=='__main__':main()
