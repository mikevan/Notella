"""Small HTTP client for other PRS applications; no third-party dependencies."""
import json
from urllib.request import Request,urlopen

class Client:
    def __init__(self,token,base_url='http://127.0.0.1:8765',timeout=30):
        self.base_url=base_url.rstrip('/');self.token=token;self.timeout=timeout
    def request(self,path,body=None):
        req=Request(self.base_url+path,data=json.dumps(body,allow_nan=False).encode() if body is not None else None,
            headers={'Authorization':'Bearer '+self.token,'Content-Type':'application/json'})
        with urlopen(req,timeout=self.timeout) as response:return json.load(response)
    def register_ontology(self,ontology):return self.request('/v1/ontologies',ontology)
    def compile(self,ontology_id,examples,exclusions=None):
        return self.request('/v1/curricula',dict(ontologyId=ontology_id,examples=examples,excludedPromptHashes=exclusions or []))
    def plan(self,curriculum_id,base_model,steps=100,rank=16,learning_rate=0.00005):
        return self.request('/v1/plans',dict(curriculumId=curriculum_id,baseModel=base_model,steps=steps,rank=rank,learningRate=learning_rate))
    def start_job(self,plan_id):return self.request('/v1/jobs',dict(planId=plan_id))
    def get(self,kind,identity):return self.request('/v1/'+kind+'/'+identity)
    def evaluate(self,curriculum_id,predictions,split='test'):
        return self.request('/v1/evaluations',dict(curriculumId=curriculum_id,predictions=predictions,split=split))
    def record_review(self,curriculum_id,example_id,output,reviewer,criteria,judgments,split='validation'):
        return self.request('/v1/interpretation-reviews',dict(curriculumId=curriculum_id,exampleId=example_id,output=output,reviewer=reviewer,criteria=criteria,judgments=judgments,split=split))
