"""Train-only input projection with new development controls and exact-overlap checks."""
import copy,hashlib,json,sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from notella import Notella
from notella.core import canonical
from notella.profile import prepare_profile
from profiles.layertime.decision_contract import project_observation

def main():
 folder=Path(__file__).resolve().parent;out=ROOT/'runtime/warning-v6-typed-training'
 if (out/'launch.json').exists():raise ValueError('Preserve the launched run')
 config=json.loads((ROOT/'experiments/warning-v5-contracts/contract.json').read_text())
 registry=copy.deepcopy(config['registry']);registry.update({
  'third-independent-observer':dict(originRef='third-observer-origin',reviewed=True),
  'third-relay-of-report-X':dict(originRef='report-x-origin',reviewed=True)})
 prior=json.loads((ROOT/'experiments/warning-v4-expanded/ontology.json').read_text())
 instruction=config['systemInstruction'].rsplit('Return only JSON matching: ',1)[0].strip()
 ontology=dict(name='LayerTime typed-observation decision training',version='0.6.0-development',
  concepts=prior['concepts'],relations=prior['relations'],instruction=instruction,outputSchema=config['outputSchema'])
 originals=[e for e in json.loads((ROOT/'experiments/warning-v4-expanded/development-examples.json').read_text()) if e['split']=='train']
 rows=[];templates={};projections=[]
 def convert(parent,obs,identity,family,split,target):
  projection=project_observation(obs,registry,config['ongoingThreat'])
  if not projection['eligibleForModel']:raise ValueError('Unsupported training/control input: '+identity)
  projections.append(dict(id=identity,receipt=projection['receipt']))
  return dict(id=identity,family=family,split=split,concepts=list(ontology['concepts']),
   source=dict(id='notella-typed-warning-development-v6',kind='synthetic',reference=parent['id'],
    permission='Project-authored development use',labelAuthor='Agent-authored proposed policy; not independent field validation',
    trainingAllowed=split=='train',samplingRole=parent['source']['samplingRole'] if split=='train' else 'new development control from an existing authored pattern',
    originalExampleId=parent['id'],observationSha256=projection['receipt']['observationSha256']),
   input=canonical(dict(observation=projection['modelInput'])),target=target)
 for e in originals:
  raw=json.loads(e['input']);obs=next(f['value'] for f in raw['facts'] if f['factId']=='capture_summary')
  rows.append(convert(e,obs,'v6-'+e['id'],e['family'],'train',e['target']))
  templates.setdefault(e['family'],(e,obs))
 for family,(parent,template) in templates.items():
  obs=copy.deepcopy(template);d=obs['disruption'];b=obs['drone']
  d.update(timeMs=1000000,uncertaintyMs=250);b.update(timeMs=1025000,uncertaintyMs=250);obs['linkingWindowMs']=90000
  if family=='credible-sequence':
   b['timeMs']=1055000;b['sources'].append('third-independent-observer')
  elif family=='generic-rf':obs['linkingWindowMs']=60000
  elif family=='outage-only':b['timeMs']=1035000;obs['linkingWindowMs']=45000
  elif family=='reversed-order':b['timeMs']=985000
  elif family=='missing-clock':
   # Numeric timestamps on unaligned clocks must still be unresolved.
   obs['timeBasis']='clock alignment unknown';b['timeMs']=1038000
  elif family=='distant-location':b['timeMs']=1012500;obs['linkingWindowMs']=60000
  elif family=='benign-operations':b['timeMs']=1009000;obs['linkingWindowMs']=60000
  elif family=='duplicate-reports':
   b['sources'].append('third-relay-of-report-X');b['timeMs']=1033000;obs['linkingWindowMs']=45000
  elif family=='outside-window':b['timeMs']=1400000;obs['linkingWindowMs']=60000
  elif family=='overlapping-clock':
   b['timeMs']=1005000;d['uncertaintyMs']=10000;b['uncertaintyMs']=10000
  else:raise ValueError('Unknown pattern')
  rows.append(convert(parent,obs,'v6-control-'+family,'v6-development-'+family,'validation',parent['target']))
 (folder/'ontology.json').write_text(json.dumps(ontology,indent=2)+'\n')
 (folder/'development-examples.json').write_text(json.dumps(rows,indent=2)+'\n')
 (folder/'source-registry.json').write_text(json.dumps(registry,indent=2)+'\n')
 (folder/'projection-receipts.json').write_text(json.dumps(projections,indent=2)+'\n')
 profile=dict(formatVersion='notella.profile.v1',training=dict(baseModel='qwen3-4b',steps=90,rank=16,learningRate=0.0001),
  inputProjection=dict(formatVersion='layertime.decision-observation.v1',implementationSha256=hashlib.sha256((ROOT/'profiles/layertime/decision_contract.py').read_bytes()).hexdigest(),registrySha256=hashlib.sha256(canonical(registry).encode()).hexdigest()))
 for key,file in [('ontology','ontology.json'),('examples','development-examples.json')]:profile[key]=dict(file=file,sha256=hashlib.sha256((folder/file).read_bytes()).hexdigest())
 (folder/'profile.json').write_text(json.dumps(profile,indent=2)+'\n')
 out.mkdir(parents=True,exist_ok=True);receipt=prepare_profile(Notella(out/'store'),folder/'profile.json')
 (out/'prepared.json').write_text(json.dumps(receipt,indent=2)+'\n')
 train=[e for e in rows if e['split']=='train'];validation=[e for e in rows if e['split']=='validation']
 audit=dict(trainingRows=len(train),uniqueProjectedTrainingInputs=len({e['input'] for e in train}),
  sourceAuthoredTrainingVariants=30,explicitReplayRows=15,postureCounts=dict(Counter(e['target']['posture'] for e in train)),
  newDevelopmentControls=len(validation),exactCrossSplitInputOverlap=len({e['input'] for e in train}&{e['input'] for e in validation}),
  oldAnchorRole='known-template regression only; some old anchors equal projected training inputs',independentFieldIncidents=0,frozenTestLoaded=False)
 assert audit['exactCrossSplitInputOverlap']==0
 (folder/'sampling-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
 print(json.dumps(dict(receipt=receipt,audit=audit),indent=2))

if __name__=='__main__':main()
