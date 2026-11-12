"""Versioned local HTTP transport for the public Python API."""
import hmac,json
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from .core import ValidationError,canonical

def server(service,token,host='127.0.0.1',port=8765,jobs=None):
    if host not in ('127.0.0.1','::1','localhost'):raise ValidationError('This release supports loopback binding only')
    if not isinstance(token,str) or len(token)<24:raise ValidationError('Use an API token of at least 24 characters')
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def send(self,status,value):
            raw=canonical(value).encode();self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8')
            self.send_header('Content-Length',str(len(raw)));self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(raw)
        def do_GET(self):self.dispatch()
        def do_POST(self):self.dispatch()
        def dispatch(self):
            try:
                if self.path=='/health' and self.command=='GET':return self.send(200,dict(status='ok',apiVersion='v1',product='Notella'))
                if not hmac.compare_digest(self.headers.get('Authorization',''),'Bearer '+token):return self.send(401,dict(error='Unauthorized'))
                if self.path=='/v1/openapi.json' and self.command=='GET':
                    from .openapi import specification
                    return self.send(200,specification())
                parts=self.path.strip('/').split('/')
                if self.command=='GET' and len(parts)==3 and parts[0]=='v1':
                    value=jobs.get(parts[2]) if parts[1]=='jobs' and jobs else service.get(parts[1],parts[2])
                    return self.send(200,value)
                if self.command!='POST':return self.send(404,dict(error='Unknown route'))
                length=int(self.headers.get('Content-Length','0'))
                if not 0<length<=4*1024*1024:return self.send(413,dict(error='Body must be 1 byte to 4 MiB'))
                body=json.loads(self.rfile.read(length));
                if not isinstance(body,dict):raise ValidationError('JSON body must be an object')
                if self.path=='/v1/ontologies':result=service.register_ontology(body)
                elif self.path=='/v1/curricula':result=service.compile(body['ontologyId'],body['examples'],body.get('excludedPromptHashes'))
                elif self.path=='/v1/plans':result=service.plan(body['curriculumId'],body['baseModel'],body.get('steps',100),body.get('rank',16),body.get('learningRate',0.00005))
                elif self.path=='/v1/evaluations':result=service.evaluate(body['curriculumId'],body['predictions'],body.get('split','test'))
                elif self.path=='/v1/jobs' and jobs:result=jobs.start(body['planId'])
                else:return self.send(404,dict(error='Unknown route'))
                self.send(201,result)
            except FileNotFoundError:self.send(404,dict(error='Artifact not found'))
            except (ValidationError,KeyError,TypeError,ValueError) as error:self.send(400,dict(error=str(error)))
            except Exception:self.send(500,dict(error='Internal error; inspect local server state'))
    instance=ThreadingHTTPServer((host,port),Handler);instance.daemon_threads=True
    return instance
