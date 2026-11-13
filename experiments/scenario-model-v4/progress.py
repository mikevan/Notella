"""Read-only progress, separated into known diagnostics and fresh controls."""
import json
from pathlib import Path
from report import counts
ROOT=Path(__file__).resolve().parents[2];RUN=ROOT/'runtime/scenario-model-v4'

def progress():
 result={}
 launch=RUN/'launch.json'
 if launch.exists():
  job=json.loads(launch.read_text(encoding='utf-8'))
  ledger=RUN/'store/jobs'/job['id']/'adapter/optimizer-stability.json'
  if ledger.exists():
   x=json.loads(ledger.read_text(encoding='utf-8'));result['training']={k:x[k] for k in ['recordedIterations','appliedOptimizerUpdates','skippedOptimizerUpdates']}
 for condition in ['base','adapted']:
  path=RUN/(condition+'-generation.jsonl');rows=[]
  if path.exists():
   lines=path.read_text(encoding='utf-8').splitlines()
   for index,line in enumerate(lines):
    try: rows.append(json.loads(line))
    except json.JSONDecodeError:
     if index !=len(lines)-1:raise
  result[condition]={group:counts([r for r in rows if (r['scenarioId'] in ['S-Q71','S-Q92'])==(group=='known')]) for group in ['known','fresh']}
  result[condition]['finalized']=(RUN/(condition+'-generation.json')).exists()
 return result
if __name__=='__main__':print(json.dumps(progress(),indent=2))
