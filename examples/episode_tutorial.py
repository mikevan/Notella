"""Episode contract tutorial. Explicit rule references, no GPU or model generation."""
import argparse,copy,json,hashlib
from pathlib import Path
from notella import Notella,ValidationError
from notella.core import canonical
from notella.episodes import validate_episode_set,compile_episode_examples
from profiles.network_episodes.reference import rule_state

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('runtime/episode-tutorial'));a=p.parse_args()
 if a.output.exists():raise ValueError('Use a new tutorial output directory; preserve earlier receipts')
 profile=Path(__file__).resolve().parents[1]/'profiles/network_episodes'
 ontology=json.loads((profile/'ontology.json').read_text());episodes=json.loads((profile/'episodes.json').read_text());receipt=validate_episode_set(ontology,episodes);rows=compile_episode_examples(ontology,episodes)
 # Domain reference is an explicit rule implementation, not semantic ground truth.
 assert all(s['target']==rule_state(e,s['asOfMs']) for e in episodes for s in e['steps'])
 a.output.mkdir(parents=True)
 (a.output/'ontology.json').write_text(json.dumps(ontology,indent=2)+'\n');(a.output/'episodes.json').write_text(json.dumps(episodes,indent=2)+'\n');(a.output/'examples.json').write_text(json.dumps(rows,indent=2)+'\n')
 api=Notella(a.output/'store');registered=api.register_ontology(ontology)
 admission_refused=False
 try:api.compile(registered['id'],rows)
 except ValidationError as error:
  assert 'not admitted' in str(error);admission_refused=True
 result=dict(validatorSha256=hashlib.sha256((Path(__file__).resolve().parents[1]/'notella/episodes.py').read_bytes()).hexdigest(),referenceSha256=hashlib.sha256((profile/'reference.py').read_bytes()).hexdigest(),episodes=receipt['episodes'],prefixStates=receipt['steps'],uniqueVisiblePrefixes=receipt['uniquePrefixes'],originalFamilies=len({e['family'] for e in episodes}),sharedPrefixVariants=True,modelLoaded=False,trainingStarted=False,semanticAccuracyMeasured=False,unreviewedTrainingAdmissionRefused=admission_refused,
  trajectories={e['id']:[s['target']['assessment']['criticality']+('/review' if s['target']['assessment']['status']=='review_required' else '') for s in e['steps']] for e in episodes},receipt=receipt)
 (a.output/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='receipt'},indent=2))
if __name__=='__main__':main()
