"""Read-only comparison summary; safe to run while generation journals grow.

Run: python experiments/scenario-model-v3/summarize.py
Partial results are progress, not a completed comparison.
"""
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / 'runtime' / 'scenario-model-v3'
SCENARIOS = ROOT / 'experiments' / 'scenario-model-v1' / 'development-scenarios.json'


def summarize():
    scenarios = json.loads(SCENARIOS.read_text(encoding='utf-8'))
    targets = {(s['id'], t['asOfMs']):t['target']['assessment']['criticality'] for s in scenarios for t in s['steps']}
    expected = len(targets)
    conditions = {}
    records = {}
    metrics = ('jsonValid', 'schemaValid', 'contractValid', 'criticalityMatch', 'assessmentEvidenceMatch', 'nodesMatch', 'edgesMatch', 'fullStateMatch', 'tokenLimitReached')
    for condition in ('base', 'adapted'):
        journal = RUN / (condition + '-generation.jsonl')
        rows = []
        if journal.exists():
            lines = journal.read_text(encoding='utf-8').splitlines()
            for index, line in enumerate(lines):
                try: rows.append(json.loads(line))
                except json.JSONDecodeError:
                    if index != len(lines)-1: raise
                    # An unfinished final line may still be being flushed.
        ids = [r['id'] for r in rows]
        if len(ids) != len(set(ids)): raise ValueError('Duplicate evaluation row')
        confusion = Counter()
        for row in rows:
            try: label = json.loads(row['output'])['assessment']['criticality']
            except (ValueError, KeyError, TypeError): label = '<unreadable>'
            confusion[(targets[(row['scenarioId'], row['asOfMs'])], str(label))] += 1
        records[condition] = {r['id']:r for r in rows}
        final_path = RUN / (condition + '-generation.json')
        final = json.loads(final_path.read_text(encoding='utf-8')) if final_path.exists() else None
        if final is not None and final['total'] != len(rows): raise ValueError('Journal/final count mismatch')
        conditions[condition] = dict(completed=len(rows), expected=expected, finalized=final is not None,
            counts={key:sum(bool(r['score'][key]) for r in rows) for key in metrics},
            errors=dict(Counter(r['score'].get('error', '<none>') for r in rows)),
            criticalityConfusion=[dict(expected=a, generated=b, count=n) for (a,b),n in sorted(confusion.items())],
            generationSeconds=sum(r['seconds'] for r in rows))
    shared = sorted(set(records['base']) & set(records['adapted']))
    mismatched = [key for key in shared if records['base'][key]['promptSha256'] != records['adapted'][key]['promptSha256']]
    if mismatched: raise ValueError('Unmatched prompts: ' + str(mismatched))
    complete = all(c['finalized'] and c['completed'] == expected for c in conditions.values())
    if complete:
        finals = [json.loads((RUN / (c+'-generation.json')).read_text(encoding='utf-8')) for c in ('base', 'adapted')]
        for field in ('evaluationSha256', 'evaluatorSha256', 'scorerSha256', 'curriculumId'):
            if finals[0][field] != finals[1][field]: raise ValueError('Comparison provenance mismatch: '+field)
        if finals[0]['evaluationSha256'] != hashlib.sha256(SCENARIOS.read_bytes()).hexdigest(): raise ValueError('Evaluation fixture changed')
    return dict(complete=complete, matchedPromptPairs=len(shared), conditions=conditions,
        releaseEligible=False, limits=['Same-author synthetic development, not independent field evidence.',
        'Full-prefix reconstruction, not delta inference or phone performance.',
        'Partial conditions cannot establish training benefit.'])

if __name__ == '__main__': print(json.dumps(summarize(), indent=2))
