import argparse,json,os
from pathlib import Path
from .core import Notella
from .http import server
from .jobs import Jobs

def main():
    p=argparse.ArgumentParser(description='Notella local API');p.add_argument('command',choices=['serve','demo'])
    p.add_argument('--store',default='data');p.add_argument('--port',type=int,default=8765)
    p.add_argument('--engine',type=Path);p.add_argument('--python',type=Path)
    p.add_argument('--model',action='append',default=[],help='Server-owned alias=local-model-directory')
    a=p.parse_args();service=Notella(a.store)
    if a.command=='demo':
        root=Path(__file__).resolve().parent.parent/'examples'
        o=service.register_ontology(json.loads((root/'layertime.ontology.json').read_text(encoding='utf-8')))
        c=service.compile(o['id'],json.loads((root/'layertime.examples.json').read_text(encoding='utf-8')))
        plan=service.plan(c['id'],'qwen3-4b',steps=70)
        print(json.dumps(dict(ontologyId=o['id'],curriculumId=c['id'],planId=plan['id'],splits=c['artifact']['splits']),indent=2));return
    models=dict(item.split('=',1) for item in a.model)
    instance=server(service,os.environ.get('NOTELLA_API_TOKEN',''),port=a.port,jobs=Jobs(service,a.engine,a.python,models))
    print(f'Notella API listening on http://127.0.0.1:{a.port}',flush=True)
    try:instance.serve_forever()
    except KeyboardInterrupt:pass
    finally:instance.server_close()

if __name__=='__main__':main()
