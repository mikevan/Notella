"""Runnable review-ledger demonstration. Authored fixture only; no model inference."""
import argparse,json
from notella import Notella
from notella.semantic_reviews import record_review
from .tutorial import teaching_material

def main():
 p=argparse.ArgumentParser();p.add_argument('--store',default='runtime/review-tutorial');a=p.parse_args()
 api=Notella(a.store);ontology,examples=teaching_material();o=api.register_ontology(ontology);c=api.compile(o['id'],examples)
 output=json.dumps(examples[-1]['target'])
 criteria=[dict(id='threshold-meaning',description='The stated reading is compared correctly against the supplied strictly-greater-than rule.'),dict(id='no-invented-cause',description='The interpretation does not claim a fire or invent a cause.')]
 judgments=[dict(criterionId='threshold-meaning',status='pass',rationale='The authored fixture states that 35 exceeds 30.'),dict(criterionId='no-invented-cause',status='pass',rationale='The authored limitation explicitly declines to infer a fire or its cause.')]
 review=record_review(api,c['id'],'test-warm',output,dict(name='Tutorial fixture author',kind='agent',independent=False),criteria,judgments,split='test')
 print(json.dumps(dict(reviewId=review['id'],outputSha256=review['artifact']['outputSha256'],allCriteriaPassed=review['artifact']['allCriteriaPassed'],fixtureOnly=True,modelLoaded=False,automaticallyMeasuredSemanticAccuracy=False),indent=2))

if __name__=='__main__':main()
