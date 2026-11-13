"""Local teacher inference. Responses are candidates, never admitted training data."""
import hashlib
import json
import math
import os
import time
from pathlib import Path
from urllib.parse import urlsplit
from urllib.error import HTTPError
from urllib.request import Request, build_opener, HTTPRedirectHandler, ProxyHandler
from .core import canonical, check

class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

class LocalTeacher:
    """Colibri/OpenAI-compatible loopback provider; no redirects or proxy routing."""
    def __init__(self, model, base_url='http://127.0.0.1:8000/v1', timeout=300, token=None):
        u=urlsplit(base_url)
        check(u.scheme=='http' and u.hostname in ('127.0.0.1','localhost','::1') and not u.username and not u.password and not u.query and not u.fragment,'Teacher must use a loopback HTTP URL')
        check(isinstance(model,str) and bool(model.strip()),'Explicit served model identity required')
        check(type(timeout) in (int,float) and math.isfinite(timeout) and timeout>0,'Positive finite timeout required')
        self.model=model;self.base_url=base_url.rstrip('/');self.timeout=timeout;self.token=token
    def generate(self,messages,max_tokens=384):
        check(type(max_tokens) is int and 0<max_tokens<=4096,'max_tokens must be 1..4096')
        check(isinstance(messages,list) and bool(messages),'Messages required')
        for m in messages:
            check(isinstance(m,dict) and set(m)=={'role','content'} and m['role'] in ('system','user','assistant') and isinstance(m['content'],str),'Invalid message')
        body=dict(model=self.model,messages=messages,temperature=0,max_tokens=max_tokens,stream=False)
        headers={'Content-Type':'application/json'}
        if self.token:headers['Authorization']='Bearer '+self.token
        started=time.monotonic()
        try:
            with build_opener(ProxyHandler({}),_NoRedirect()).open(Request(self.base_url+'/chat/completions',data=canonical(body).encode(),headers=headers),timeout=self.timeout) as response:
                raw=response.read(8*1024*1024+1)
        except HTTPError as error:
            error.response_body=error.read(8*1024*1024).decode('utf-8',errors='replace')
            error.close()
            raise
        check(len(raw)<=8*1024*1024,'Teacher response exceeds limit')
        try:
            parsed=json.loads(raw)
            output=parsed['choices'][0]['message']['content']
            check(isinstance(output,str),'Teacher returned non-text content')
        except (ValueError,KeyError,IndexError,TypeError) as error:
            error.response_body=raw.decode('utf-8',errors='replace')
            raise
        return dict(request=body,responseBody=raw.decode('utf-8'),output=output,seconds=time.monotonic()-started,
                    responseModel=parsed.get('model'),finishReason=parsed['choices'][0].get('finish_reason'),
                    admittedForTraining=False,reviewStatus='pending')

def teaching_candidate(provider, ontology_id, concept_refs, messages, directory, max_tokens=384):
    """Persist one immutable request and completed response; restart skips completed work.

    A failed/uncertain call is preserved and refused on restart: use a new directory
    for an explicit retry. No claim of exactly-once remote execution is made.
    """
    check(isinstance(ontology_id,str) and bool(ontology_id),'Ontology identity required')
    check(isinstance(concept_refs,list) and bool(concept_refs) and all(isinstance(x,str) and x for x in concept_refs),'Concept references required')
    request=dict(formatVersion='notella.teacher-request.v1',ontologyId=ontology_id,conceptRefs=concept_refs,
                 baseUrl=provider.base_url,model=provider.model,messages=messages,maxTokens=max_tokens,
                 providerSha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    identity=hashlib.sha256(canonical(request).encode()).hexdigest()
    root=Path(directory);root.mkdir(parents=True,exist_ok=True)
    request_path=root/'request.json';result_path=root/'result.json'
    if request_path.exists():
        check(request_path.read_text(encoding='utf-8')==canonical(request),'Existing request differs')
        check(result_path.exists(),'Previous request incomplete or failed; inspect before an explicit retry in a new directory')
        result=json.loads(result_path.read_text(encoding='utf-8'))
        check(result.get('requestId')==identity,'Result identity mismatch')
        stored_id=result.pop('resultId',None)
        check(stored_id==hashlib.sha256(canonical(result).encode()).hexdigest(),'Saved result integrity mismatch')
        result['resultId']=stored_id
        return result
    with request_path.open('x',encoding='utf-8') as f:f.write(canonical(request))
    try:
        result=provider.generate(messages,max_tokens)
        result.update(requestId=identity,ontologyId=ontology_id,conceptRefs=concept_refs,admittedForTraining=False,reviewStatus='pending')
        result['outputSha256']=hashlib.sha256(result['output'].encode('utf-8')).hexdigest()
        result['resultId']=hashlib.sha256(canonical(result).encode()).hexdigest()
        temp=root/'result.tmp'
        with temp.open('x',encoding='utf-8') as f:f.write(canonical(result))
        os.replace(temp,result_path)
        return result
    except Exception as e:
        with (root/'error.json').open('x',encoding='utf-8') as f:
            f.write(canonical(dict(requestId=identity,errorType=type(e).__name__,error=str(e),responseBody=getattr(e,'response_body',None),admittedForTraining=False)))
        raise
