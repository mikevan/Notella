"""Read-only training and generation progress for v5."""
import json
from pathlib import Path
from report import summarize
ROOT=Path(__file__).resolve().parents[2];RUN=ROOT/'runtime/scenario-model-v5'

def main():
    prepared=json.loads((RUN/'prepared.json').read_text(encoding='utf-8'))
    scenarios=json.loads((ROOT/'experiments/scenario-model-v5/development-scenarios.json').read_text(encoding='utf-8'))
    targets={(s['id'],t['asOfMs']):t['target']['assessment']['criticality'] for s in scenarios for t in s['steps']}
    result={};launch=RUN/'launch.json'
    if launch.exists():
        j=json.loads(launch.read_text(encoding='utf-8'));ledger=RUN/'store/jobs'/j['id']/'adapter/optimizer-stability.json'
        if ledger.exists():
            x=json.loads(ledger.read_text(encoding='utf-8'));result['training']={k:x[k] for k in ('appliedOptimizerUpdates','skippedOptimizerUpdates')}
    for condition in ('base','adapted'):
        rows=[];path=RUN/(condition+'-generation.jsonl')
        if path.exists():
            lines=path.read_text(encoding='utf-8').splitlines()
            for index,line in enumerate(lines):
                try:rows.append(json.loads(line))
                except json.JSONDecodeError:
                    if index!=len(lines)-1:raise
        result[condition]={}
        for group in ('known','fresh'):
            selected=[r for r in rows if r['scenarioId'].startswith('F-')==(group=='fresh')]
            summary=summarize(selected,targets);summary.pop('decisions');result[condition][group]=summary
        result[condition]['finalized']=(RUN/(condition+'-generation.json')).exists()
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
