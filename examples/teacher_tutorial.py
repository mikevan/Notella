"""Draft one ontology-scoped candidate with a running local teacher; never trains."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from notella.core import canonical
from notella.teachers import LocalTeacher,teaching_candidate
import hashlib

def main():
 p=argparse.ArgumentParser();p.add_argument('--model',required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--base-url',default='http://127.0.0.1:8000/v1');a=p.parse_args()
 ontology=json.loads((ROOT/'experiments/warning-v6-typed-training/ontology.json').read_text(encoding='utf-8'))
 identity=hashlib.sha256(canonical(ontology).encode()).hexdigest()
 concepts=['temporal_precedence','source_independence','warning_posture','causal_claim']
 messages=[dict(role='system',content='Propose synthetic teaching material for human review. Your output is not ground truth. Follow the supplied ontology; do not claim a real attack, perpetrator, or calibrated attack probability.'),dict(role='user',content=json.dumps(dict(task='Draft two short contrasting observations: a temporally linked disruption and corroborated drone observation with distinct asserted origins, and a similar observation with two reports sharing one origin. Explain the distinction, uncertainty, and why neither establishes causation. Do not use real people or locations.',concepts={k:ontology['concepts'][k] for k in concepts},proposedPolicy=ontology['instruction']),sort_keys=True))]
 result=teaching_candidate(LocalTeacher(a.model,a.base_url),identity,concepts,messages,a.output,max_tokens=768)
 print(json.dumps(dict(requestId=result['requestId'],reviewStatus=result['reviewStatus'],admittedForTraining=result['admittedForTraining'],output=str(a.output))))
if __name__=='__main__':main()
