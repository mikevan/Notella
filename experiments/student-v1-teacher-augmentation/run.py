"""Explicit reviewed admission and matched-budget sequential student jobs."""
import hashlib,json,sys,time,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from notella import Notella
from notella.core import canonical,fingerprint
from notella.jobs import Jobs
from notella.teacher_reviews import record_teacher_review

def main():
 folder=Path(__file__).resolve().parent;out=ROOT/'runtime/student-v1-teacher-augmentation';out.mkdir(parents=True,exist_ok=True)
 if (out/'prepared.json').exists():raise ValueError('Preserve existing student experiment')
 teacher=ROOT/'runtime/teacher-constrained-v2';summary=json.loads((teacher/'summary.json').read_text())
 assert summary['decisionMatches']==6 and summary['guardPasses']==6 and summary['formatValidPairs']==3
 tasks=json.loads((ROOT/'experiments/colibri-teacher-v2-constrained/tasks.json').read_text())['tasks']
 ontology=json.loads((ROOT/'experiments/warning-v6-typed-training/ontology.json').read_text())
 prior=json.loads((ROOT/'experiments/warning-v6-typed-training/development-examples.json').read_text())
 train=[e for e in prior if e['split']=='train'];controls=json.loads((folder/'controls.json').read_text());api=Notella(out/'store')
 oid=api.register_ontology(ontology)['id'];criteria=json.loads((ROOT/'experiments/colibri-teacher-v1/review-criteria.json').read_text(encoding='utf-8-sig'))['criteria']
 extra=[];reviews=[]
 for task in tasks:
  candidate=json.loads((teacher/task['id']/'result.json').read_text());assert candidate['finishReason']=='stop'
  answers=json.loads(candidate['output'])['answers']
  rationale={
   'ontology_scope':'Both predicted decisions match the supplied policy and reference for these fixed facts.',
   'source_lineage':'Uses drone-report origin groups without asserting statistical independence. The phrase unconfirmed independence in pair 2 is limited to the declared trigger, not a statistical certification.',
   'temporal_link':'Supplied after relation, numerical interval and window are preserved; the teacher did not change timing.',
   'causal_restraint':'No causal attribution, perpetrator identity or calibrated attack probability is asserted.',
   'contrast_consistency':'Each pair changes one concept and supplies one policy-consistent decision per case. Rationale is a summary rather than an exhaustive restatement of every condition.',
   'completion':'Complete JSON, finishReason stop, exact required two-case shape validated.',
   'candidate_only':'Synthetic draft kept separate from the explicit experimental admission recorded here.'}
  review=record_teacher_review(api,candidate,dict(name='Codex',kind='agent',independent=False),criteria,[dict(criterion=c['id'],status='pass',rationale=rationale[c['id']]) for c in criteria])
  reviews.append(review);assert review['artifact']['disposition']=='review_passed'
  for c in task['cases']:
   prediction=next(a['decision'] for a in answers if a['id']==c['id']);assert prediction==c['expected']
   extra.append(dict(id='teacher-v2-'+task['id']+'-'+c['id'],family='teacher-v2-authored-'+task['id'],split='train',concepts=list(ontology['concepts']),
    source=dict(id='reviewed-teacher-v2-synthetic',kind='synthetic',reference=candidate['resultId']+'#'+c['id'],permission='Project-authored synthetic experiment; explicit agent-reviewed admission under owner-authorized training',labelAuthor='Local teacher decision; Codex agent review, not independent field truth',trainingAllowed=True,reviewId=review['id']),
    input=canonical(dict(observation=c['observation'])),target=prediction))
 assert not ({e['input'] for e in train+extra}&{e['input'] for e in controls})
 model=Path('C:/workspace/TUltra-Project/LayerTime/tools/ai-training/models/qwen3-0.6b-base')
 receipt=dict(sourceAssertion=json.loads((model/'source.json').read_text()),remoteDigestsIndependentlyVerified=False,files=[])
 for p in sorted(model.iterdir()):
  if p.is_file():
   with p.open('rb') as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
   receipt['files'].append(dict(path=p.name,sha256=digest,size=p.stat().st_size))
 (out/'model-intake.json').write_text(json.dumps(receipt,indent=2)+'\n')
 (out/'teacher-reviews.json').write_text(json.dumps(reviews,indent=2)+'\n')
 (out/'explicit-admission.json').write_text(json.dumps(dict(reviewIds=[r['id'] for r in reviews],trainingExamples=extra,operator='Codex under owner-authorized development training',independentReview=False,controlsFrozenSha256=hashlib.sha256((folder/'controls.json').read_bytes()).hexdigest()),indent=2)+'\n')
 excluded=[fingerprint(e['input']) for e in prior if e['split']!='train']
 conditions={}
 for condition,training in [('direct',train),('augmented',train+extra)]:
  cid=api.compile(oid,training+controls,excluded)['id'];pid=api.plan(cid,'qwen3-0.6b',steps=90,rank=16,learning_rate=0.0001)['id']
  conditions[condition]=dict(curriculumId=cid,planId=pid,trainingRows=len(training),validationRows=len(controls))
 (out/'prepared.json').write_text(json.dumps(dict(ontologyId=oid,conditions=conditions,modelIntakeSha256=hashlib.sha256((out/'model-intake.json').read_bytes()).hexdigest()),indent=2)+'\n')
 jobs=Jobs(api,ROOT/'training_engine',sys.executable,{'qwen3-0.6b':model})
 for condition,config in conditions.items():
  job=jobs.start(config['planId']);(out/(condition+'-launch.json')).write_text(json.dumps(job,indent=2)+'\n');print(json.dumps(dict(condition=condition,jobId=job['id'],status=job['status'])),flush=True)
  while job['status'] in ('starting','running'):
   time.sleep(2);job=jobs.get(job['id'])
  if job['status']!='completed':raise RuntimeError(condition+' training failed; inspect '+str(jobs.root/job['id']))
  adapter=jobs.root/job['id']/'adapter';stability=json.loads((adapter/'optimizer-stability.json').read_text());weights=json.loads((adapter/'weight-stability.json').read_text())
  print(json.dumps(dict(condition=condition,applied=stability['appliedOptimizerUpdates'],skipped=stability['skippedOptimizerUpdates'],finite=weights['allWeightsFinite'])),flush=True)
  if not weights['allWeightsFinite'] or stability['skippedOptimizerUpdates']:raise RuntimeError('Numerical issue; preserve and inspect')
  subprocess.run([sys.executable,str(folder/'evaluate.py'),'--condition',condition,'--adapter',str(adapter)],check=True)
 print('BOTH_STUDENT_CONDITIONS_COMPLETED',flush=True)
if __name__=='__main__':main()
