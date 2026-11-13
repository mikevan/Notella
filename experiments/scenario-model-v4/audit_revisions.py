"""Describe temporal decision revisions from preserved outputs; never repairs them."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / 'runtime' / 'scenario-model-v4'
RANK = dict(contextual=0, high=1, critical=2)


def direction(before, after):
    if before not in RANK or after not in RANK: return 'unreadable'
    return 'escalate' if RANK[after] > RANK[before] else 'deescalate' if RANK[after] < RANK[before] else 'unchanged'


def audit():
    scenarios = json.loads((ROOT/'experiments/scenario-model-v4/development-scenarios.json').read_text(encoding='utf-8'))
    results = {}
    for condition in ('base', 'adapted'):
        path = RUN/(condition+'-generation.jsonl')
        rows = {}
        if path.exists():
            lines = path.read_text(encoding='utf-8').splitlines()
            for index,line in enumerate(lines):
                try: row = json.loads(line)
                except json.JSONDecodeError:
                    if index != len(lines)-1: raise
                    continue
                key = (row['scenarioId'],row['asOfMs'])
                if key in rows: raise ValueError('Duplicate prefix')
                rows[key] = row
        transitions = []
        for scenario in scenarios:
            for before,after in zip(scenario['steps'],scenario['steps'][1:]):
                keys = [(scenario['id'],s['asOfMs']) for s in (before,after)]
                if not all(k in rows for k in keys): continue
                generated = []
                for k in keys:
                    try: label = json.loads(rows[k]['output'])['assessment']['criticality']
                    except (ValueError,KeyError,TypeError): label = None
                    generated.append(label if isinstance(label,str) else None)
                expected = [s['target']['assessment']['criticality'] for s in (before,after)]
                expected_direction = direction(*expected); actual_direction = direction(*generated)
                transitions.append(dict(scenarioId=scenario['id'],beforeMs=before['asOfMs'],afterMs=after['asOfMs'],expected=expected,generated=generated,expectedDirection=expected_direction,generatedDirection=actual_direction,directionMatch=expected_direction==actual_direction,endpointsMatch=expected==generated))
        results[condition] = dict(observedTransitions=len(transitions), expectedTransitions=sum(len(s['steps'])-1 for s in scenarios),directionMatches=sum(t['directionMatch'] for t in transitions),endpointMatches=sum(t['endpointsMatch'] for t in transitions),transitions=transitions)
    return dict(conditions=results, limits=['Decision revisions reconstructed from independent full-prefix responses, not model-state rollout.', 'Direction agreement alone can conceal consistently wrong severity.', 'No automatic judgment of rationale truth or causal validity.'])

if __name__ == '__main__': print(json.dumps(audit(),indent=2))
