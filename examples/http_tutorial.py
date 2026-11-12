"""Run against a local Notella server. Creates artifacts, but does not start training."""
import argparse,json,os
from notella import Client
from .tutorial import teaching_material

def main():
    p=argparse.ArgumentParser();p.add_argument('--url',default='http://127.0.0.1:8765');a=p.parse_args()
    client=Client(os.environ['NOTELLA_API_TOKEN'],a.url);ontology,rows=teaching_material()
    o=client.register_ontology(ontology);c=client.compile(o['id'],rows);plan=client.plan(c['id'],'configured-model-alias',steps=30)
    result=client.evaluate(c['id'],{'test-warm':rows[-1]['target']})
    print(json.dumps(dict(ontologyId=o['id'],curriculumId=c['id'],planId=plan['id'],fixtureEvaluation=result['artifact'],trainingStarted=False),indent=2))

if __name__=='__main__':main()
