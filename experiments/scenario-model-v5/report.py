"""Finalize matched results and verify unchanged training controls."""
import hashlib,json,shutil
from pathlib import Path
from repetition import measure
from audit_revisions import audit
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;RUN=ROOT/'runtime/scenario-model-v5'
METRICS=['jsonValid','schemaValid','contractValid','criticalityMatch','assessmentEvidenceMatch','nodesMatch','edgesMatch','fullStateMatch','tokenLimitReached']

def summarize(rows,targets):
    decisions=[]
    for row in rows:
        try:label=json.loads(row['output'])['assessment']['criticality']
        except (ValueError,TypeError,KeyError):label=None
        if not row['score']['jsonValid'] or not isinstance(label,str) or label not in ('contextual','high','critical'):label=None
        decisions.append(dict(id=row['id'],scenarioId=row['scenarioId'],expected=targets[(row['scenarioId'],row['asOfMs'])],generated=label,score=row['score'],repetition=measure(row['output'])))
    return dict(total=len(rows),counts={m:sum(bool(r['score'][m]) for r in rows) for m in METRICS},repetitive=sum(r['repetition']['repetitive'] for r in decisions),decisions=decisions)

def main():
    reports={c:json.loads((RUN/(c+'-generation.json')).read_text(encoding='utf-8')) for c in ('base','adapted')}
    prior=json.loads((ROOT/'experiments/scenario-model-v4/evidence/adapted-generation.json').read_text(encoding='utf-8'))
    for key in ('evaluatorSha256','scorerSha256','curriculumId','evaluationSha256'):
        assert reports['base'][key]==reports['adapted'][key],key
    assert reports['base']['evaluationSha256']==hashlib.sha256((HERE/'development-scenarios.json').read_bytes()).hexdigest()
    old={r['id']:r for r in prior['results']};base={r['id']:r for r in reports['base']['results']};new={r['id']:r for r in reports['adapted']['results']}
    assert len(base)==len(new)==24 and base.keys()==new.keys()
    for identity in new:
        assert base[identity]['promptSha256']==new[identity]['promptSha256']
        if identity in old:assert old[identity]['promptSha256']==new[identity]['promptSha256']
    targets={(s['id'],t['asOfMs']):t['target']['assessment']['criticality'] for s in json.loads((HERE/'development-scenarios.json').read_text(encoding='utf-8')) for t in s['steps']}
    result=dict(known={},fresh={},releaseEligible=False,repetitionDiagnosticSha256=hashlib.sha256((HERE/'repetition.py').read_bytes()).hexdigest())
    for condition,records in [('base',base),('previousAdapter',old),('retractionAdapter',new)]:
        result['known'][condition]=summarize([r for i,r in records.items() if i in old],targets)
        if condition!='previousAdapter':result['fresh'][condition]=summarize([r for i,r in records.items() if i not in old],targets)
    adapter=Path(json.loads((RUN/'training-result.json').read_text(encoding='utf-8'))['adapter'])
    runtime=json.loads((adapter/'runtime-manifest.json').read_text(encoding='utf-8'));before=json.loads((ROOT/'experiments/scenario-model-v4/evidence/runtime-manifest.json').read_text(encoding='utf-8'))
    ignore={'dataset','output'}
    assert {k:v for k,v in runtime['requestedArguments'].items() if k not in ignore}=={k:v for k,v in before['requestedArguments'].items() if k not in ignore}
    for key in ('packages','sourceSha256','baseIntakeManifestSha256'):assert runtime[key]==before[key],key
    result['sameTrainingControlsVerified']=True;result['revisions']=audit()
    evidence=HERE/'evidence';evidence.mkdir(exist_ok=True)
    sources={name:RUN/name for name in ['prepared.json','launch.json','training-result.json','preflight.json','training-control-check.json','base-generation.json','base-generation.jsonl','adapted-generation.json','adapted-generation.jsonl']}
    sources.update({name:adapter/name for name in ['runtime-manifest.json','training-metrics.json','optimizer-stability.json','weight-stability.json','base-intake-manifest.json','adapter_config.json']})
    hashes={}
    for name,source in sources.items():
        target=evidence/name
        if target.exists():assert target.read_bytes()==source.read_bytes()
        else:shutil.copyfile(source,target)
        hashes[name]=hashlib.sha256(target.read_bytes()).hexdigest()
    (evidence/'manifest.json').write_text(json.dumps(hashes,indent=2)+'\n',encoding='utf-8')
    (evidence/'comparison.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    lines=['# Retraction and repetition curriculum: completed comparison','','The local 4B base, immutable ontology, engine/package hashes, actual training arguments, fresh adapter initialization, 80-update budget and twenty training rows are held fixed. The intervention is a retraction-focused curriculum with short fact-specific rationales and separate change summaries. Full-prefix input, full-state output, greedy generation and the 1536-token output cap remain unchanged.','']
    for group in ('known','fresh'):
        conditions=['base','previousAdapter','retractionAdapter'] if group=='known' else ['base','retractionAdapter']
        denominator=18 if group=='known' else 6
        lines+=['## '+group.title()+' cases','', '| Measure | '+' | '.join(conditions)+' |','| --- | '+' | '.join('---:' for c in conditions)+' |']
        for metric in METRICS:
            lines.append('| '+metric+' | '+' | '.join(str(result[group][c]['counts'][metric])+'/'+str(denominator) for c in conditions)+' |')
        lines.append('| repetitive narrative heuristic | '+' | '.join(str(result[group][c]['repetitive'])+'/'+str(denominator) for c in conditions)+' |')
        lines.append('')
    lines+=['## Criticality detail','','| Group / condition | Critical correct | Critical downgraded | Critical unreadable | Contextual falsely critical |','| --- | ---: | ---: | ---: | ---: |']
    for group in ('known','fresh'):
        for condition,summary in result[group].items():
            ds=summary['decisions'];critical=[r for r in ds if r['expected']=='critical'];contextual=[r for r in ds if r['expected']=='contextual']
            values=[sum(r['generated']=='critical' for r in critical),sum(r['generated'] in ('high','contextual') for r in critical),sum(r['generated'] is None for r in critical),sum(r['generated']=='critical' for r in contextual)]
            lines.append('| '+group+' / '+condition+' | '+' | '.join(map(str,values))+' |')
    lines+=['','## Interpretation boundaries','','All eighteen v4 evaluation prefixes are now inspected, known diagnostics. Six fresh prefixes were frozen before training but share the same author and proposed rule reference; neither group is independent field validation. Known base outputs were reused only after exact prompt and score checks; six fresh base outputs and all twenty-four candidate outputs were generated. No previous-adapter generation was run on the new fresh cases.','', 'Repetition is a fixed diagnostic on rationale/summary prose, including incomplete quoted prose: at least 36 words, a repeated 12-word window appearing at least three times, and duplicate-window fraction at least 0.25. It excludes repeated graph fields and is not a semantic correctness measure. Thresholds were fixed before candidate generation. Exact outputs, heuristic details and per-case scores are preserved.','', 'No generated output was repaired, dropped or admitted to training. Incomplete output remains unreadable, never clearance. More output tokens and warning-continuity retries were not introduced into this matched comparison. Runtime safeguards remain separate, and no phone deployment or alert-delivery guarantee is demonstrated.','', 'See PROTOCOL.md and review.json for curriculum, scope and provenance. The generic ontology currently declares correction edges for compromise evidence only; credential-retraction authoring drafts failed validation and were revised before admission, without changing the ontology.']
    (HERE/'RESULTS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({g:{c:{k:v for k,v in s.items() if k!='decisions'} for c,s in result[g].items()} for g in ('known','fresh')},indent=2))
if __name__=='__main__':main()
