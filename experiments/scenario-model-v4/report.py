"""Finalize the curriculum-only rerun, with known and fresh cases separated."""
import hashlib,json,shutil
from pathlib import Path
from audit_revisions import audit
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;RUN=ROOT/'runtime/scenario-model-v4'
METRICS=['jsonValid','schemaValid','contractValid','criticalityMatch','assessmentEvidenceMatch','nodesMatch','edgesMatch','fullStateMatch','tokenLimitReached']

def counts(rows):return dict(total=len(rows),counts={k:sum(bool(r['score'][k]) for r in rows) for k in METRICS})

def main():
 reports={c:json.loads((RUN/(c+'-generation.json')).read_text(encoding='utf-8')) for c in ['base','adapted']}
 prior=json.loads((ROOT/'experiments/scenario-model-v3/evidence/adapted-generation.json').read_text(encoding='utf-8'))
 for field in ['evaluatorSha256','scorerSha256','curriculumId','evaluationSha256']:
  assert reports['base'][field]==reports['adapted'][field],field
 assert reports['base']['evaluationSha256']==hashlib.sha256((HERE/'development-scenarios.json').read_bytes()).hexdigest()
 old={r['id']:r for r in prior['results']};base={r['id']:r for r in reports['base']['results']};new={r['id']:r for r in reports['adapted']['results']}
 assert len(base)==len(new)==18 and base.keys()==new.keys()
 for identity in base:
  assert base[identity]['promptSha256']==new[identity]['promptSha256']
  if identity in old: assert old[identity]['promptSha256']==new[identity]['promptSha256']
 result=dict(known=dict(base=counts([base[i] for i in old]),previousAdapter=counts(list(old.values())),repairedAdapter=counts([new[i] for i in old])),fresh=dict(base=counts([r for i,r in base.items() if i not in old]),repairedAdapter=counts([r for i,r in new.items() if i not in old])),releaseEligible=False)
 # Compare actual model/training configuration, excluding output/data paths.
 launch=json.loads((RUN/'launch.json').read_text(encoding='utf-8'));adapter=Path(json.loads((RUN/'training-result.json').read_text(encoding='utf-8'))['adapter'])
 runtime=json.loads((adapter/'runtime-manifest.json').read_text(encoding='utf-8'))
 before=json.loads((ROOT/'experiments/scenario-model-v3/evidence/runtime-manifest.json').read_text(encoding='utf-8'))
 ignored={'dataset','output'}
 assert {k:v for k,v in runtime['requestedArguments'].items() if k not in ignored}=={k:v for k,v in before['requestedArguments'].items() if k not in ignored},'Training settings changed'
 assert runtime['packages']==before['packages'],'Training packages changed'
 assert runtime['sourceSha256']==before['sourceSha256'],'Training engine changed'
 assert runtime['baseIntakeManifestSha256']==before['baseIntakeManifestSha256'],'Base model intake changed'
 targets={(scenario['id'],step['asOfMs']):step['target']['assessment']['criticality'] for scenario in json.loads((HERE/'development-scenarios.json').read_text(encoding='utf-8')) for step in scenario['steps']}
 details={}
 conditions={'base':base,'previousAdapter':old,'repairedAdapter':new}
 for condition,records in conditions.items():
  details[condition]=[]
  for identity,row in records.items():
   try:label=json.loads(row['output'])['assessment']['criticality']
   except (ValueError,KeyError,TypeError):label=None
   if not row['score']['jsonValid'] or not isinstance(label,str) or label not in ('contextual','high','critical'): label=None
   expected=targets[(row['scenarioId'],row['asOfMs'])]
   details[condition].append(dict(id=identity,scenarioId=row['scenarioId'],expected=expected,generated=label,match=row['score']['criticalityMatch'],contractValid=row['score']['contractValid'],error=row['score'].get('error')))
 result['decisionDetails']=details
 result['revisions']=audit()
 result['sameTrainingSettingsVerified']=True;result['sameTrainingEngineVerified']=True;result['sameBaseIntakeVerified']=True
 evidence=HERE/'evidence';evidence.mkdir(exist_ok=True);sources={name:RUN/name for name in ['prepared.json','preflight.json','reference-answer-lengths.json','training-control-check.json','training-result.json','launch.json','base-generation.json','base-generation.jsonl','adapted-generation.json','adapted-generation.jsonl']}
 sources.update({name:adapter/name for name in ['training-metrics.json','runtime-manifest.json','optimizer-stability.json','weight-stability.json','base-intake-manifest.json','adapter_config.json']})
 manifest={}
 for name,source in sources.items():
  dest=evidence/name
  if dest.exists():assert dest.read_bytes()==source.read_bytes(),'Evidence changed'
  else:shutil.copyfile(source,dest)
  manifest[name]=hashlib.sha256(dest.read_bytes()).hexdigest()
 (evidence/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
 (evidence/'comparison.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 lines=['# Curriculum repair: completed comparison','','Same base model, ontology, engine, LoRA/optimizer settings, 80-update budget and 20 training rows. The curriculum and its repeated-prefix exposure changed; it now has 20 unique prefixes rather than 11. All exact known prompts match, and fresh-case prompts match between base and repaired adapter.','', '## Known diagnostics: inspected before curriculum repair','','| Metric | Base | Previous adapter | Repaired adapter |','| --- | ---: | ---: | ---: |']
 for k in METRICS:lines.append('| '+k+' | '+' | '.join(str(result['known'][c]['counts'][k])+'/10' for c in ['base','previousAdapter','repairedAdapter'])+' |')
 lines+=['','## Fresh synthetic evaluation: frozen before training','','| Metric | Base | Repaired adapter |','| --- | ---: | ---: |']
 for k in METRICS:lines.append('| '+k+' | '+' | '.join(str(result['fresh'][c]['counts'][k])+'/8' for c in ['base','repairedAdapter'])+' |')
 lines+=['','Known cases are reused diagnostics, not independent evidence. Fresh cases share author, semantic motifs and rule reference with training, so are synthetic development controls, not field validation. No previous adapter generation was run on fresh cases. Schema/contract agreement and loss do not establish complete semantic correctness. Exact explanations still require inspection.','', 'The untrained base outputs for the ten unchanged known cases were reused after exact prompt and score verification; eight fresh baseline cases were generated. The repaired adapter generated all eighteen responses. No generated evaluation output was repaired, admitted to training, or excluded. Token-capped incomplete responses remain failures.','', 'See PROTOCOL.md, review.json and evidence/ for provenance. No Colibri, phone, delta-trained inference, independent expert validation or calibrated attack probability is demonstrated. No automatic field deployment follows from this experiment.']
 lines+=['','## Criticality failure detail','','| Group / condition | Critical correct | Critical to contextual | Critical to high | Critical unreadable | Contextual to critical |','| --- | ---: | ---: | ---: | ---: | ---: |']
 for group in ['known','fresh']:
  for condition in ['base','previousAdapter','repairedAdapter']:
   if group=='fresh' and condition=='previousAdapter':continue
   rows=[r for r in details[condition] if (r['scenarioId'] in ['S-Q71','S-Q92'])==(group=='known')]
   critical=[r for r in rows if r['expected']=='critical'];contextual=[r for r in rows if r['expected']=='contextual']
   values=[sum(r['generated']=='critical' for r in critical),sum(r['generated']=='contextual' for r in critical),sum(r['generated']=='high' for r in critical),sum(r['generated'] is None for r in critical),sum(r['generated']=='critical' for r in contextual)]
   lines.append('| '+group+' / '+condition+' | '+' | '.join(map(str,values))+' |')
 lines+=['','## Assessment revisions','','| Group / condition | Correct direction | Correct endpoints |','| --- | ---: | ---: |']
 for group in ['known','fresh']:
  for condition in ['base','adapted']:
   transitions=[t for t in result['revisions']['conditions'][condition]['transitions'] if (t['scenarioId'] in ['S-Q71','S-Q92']) == (group=='known')]
   n=len(transitions);direction=sum(t['directionMatch'] for t in transitions);endpoints=sum(t['endpointsMatch'] for t in transitions)
   lines.append(f'| {group} / {condition} | {direction}/{n} | {endpoints}/{n} |')
 lines+=['','The previous adapter scored 3/8 direction and 1/8 endpoint matches on known diagnostics. These revisions are reconstructed from independently prompted prefixes, not rollout from prior generated state. Direction agreement alone can conceal wrong severity.']
 lines+=['','## Output limits and warning continuity','','The 1536-token output limit remained unchanged throughout both conditions. A separate tokenizer check found all eighteen valid reference answers fit within 857 tokens; the two early capped repaired responses correspond to reference lengths 856 and 512. Observed repetitive/incomplete responses are not merely reference graphs exceeding the allowance. Capped output remains unreadable for scoring; a partial initial label is not accepted or silently repaired.','', 'The owner requires that output budgets must not silently suppress operational warnings. Separate runtime tooling now provides configurable bounded retries, retained validated assessments and focused incidents, and a warning-state callback before generation. See [Tutorial 16](../../docs/warning-continuity.md). The frozen comparison does not use those new policies. Their simulated-backend tests are not phone deployment, notification delivery validation, or evidence that a model can reliably detect an assault.']
 (HERE/'RESULTS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
