import json,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];folder=Path(__file__).resolve().parent
out=ROOT/'runtime/warning-v5-contracts';out.mkdir(exist_ok=True)
comparison=json.loads((ROOT/'runtime/warning-v4-expanded/comparison.json').read_text())
adapter=ROOT/'runtime/warning-v4-expanded/store/jobs'/comparison['jobId']/'adapter'
for name in ('base','adapted'):
 command=[sys.executable,str(folder/'evaluate.py'),'--model',os.environ['NOTELLA_EXPERIMENT_MODEL'],'--output',str(out/(name+'.json'))]
 if name=='adapted':command+=['--adapter',str(adapter)]
 with (out/(name+'.stdout.log')).open('xb') as stdout,(out/(name+'.stderr.log')).open('xb') as stderr:subprocess.run(command,check=True,stdout=stdout,stderr=stderr)
 report=json.loads((out/(name+'.json')).read_text());print(json.dumps(dict(condition=name,groups=report['groups'],inputDeferred=report['inputDeferred'])),flush=True)
base=json.loads((out/'base.json').read_text());adapted=json.loads((out/'adapted.json').read_text())
assert [r.get('promptSha256') for r in base['results']]==[r.get('promptSha256') for r in adapted['results']]
assert base['evaluatorSha256']==adapted['evaluatorSha256']
(out/'comparison.json').write_text(json.dumps(dict(noWeightUpdates=True,matchedPrompts=True,conditions={name:dict(groups=r['groups'],inputDeferred=r['inputDeferred']) for name,r in [('base',base),('adapted',adapted)]}),indent=2)+'\n')
