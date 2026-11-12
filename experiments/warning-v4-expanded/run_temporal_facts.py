import json,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
main=ROOT/'runtime/warning-v4-expanded';out=ROOT/'runtime/warning-v4-temporal-facts';out.mkdir(exist_ok=True)
comparison=json.loads((main/'comparison.json').read_text());adapter=main/'store/jobs'/comparison['jobId']/'adapter'
for name in ('base','adapted'):
 command=[sys.executable,str(Path(__file__).with_name('evaluate_temporal_facts.py')),'--model',os.environ['NOTELLA_EXPERIMENT_MODEL'],'--output',str(out/(name+'-validation.json'))]
 if name=='adapted':command+=['--adapter',str(adapter)]
 with (out/(name+'.stdout.log')).open('xb') as stdout,(out/(name+'.stderr.log')).open('xb') as stderr:subprocess.run(command,check=True,stdout=stdout,stderr=stderr)
 report=json.loads((out/(name+'-validation.json')).read_text())
 print(json.dumps(dict(condition=name,groups={group:dict(total=sum(r['caseGroup']==group for r in report['results']),decisionMatches=sum(r['caseGroup']==group and r['decisionFieldsMatch'] for r in report['results']),schemaPasses=sum(r['caseGroup']==group and r['schemaValid'] for r in report['results'])) for group in ('primary','robustness')})),flush=True)
