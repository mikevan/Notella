"""Run with python -m examples.tutorial --store runtime/tutorial. No GPU or downloads."""
import argparse,json
from pathlib import Path
from notella import Notella

def teaching_material():
    ontology=dict(name='Workshop temperature interpretation',version='1.0.0',
        concepts={'observation':'A measured temperature with units and sensor identity.',
          'threshold':'A supplied comparison rule, not a measured value.',
          'interpretation':'A finding justified by the observation and supplied rule.'},
        relations=[dict(subject='interpretation',predicate='supportedBy',object='observation'),dict(subject='interpretation',predicate='comparedAgainst',object='threshold')],
        instruction='Explain whether the supplied temperature exceeds the configured threshold. A threshold is a policy parameter, not a reading. Do not infer a fire, cause, or physical sensor identity beyond the supplied evidence.',
        outputSchema=dict(type='object',properties={'finding':dict(type='string',minLength=1),'exceedsThreshold':dict(type='boolean'),'limitation':dict(type='string',minLength=1)},required=['finding','exceedsThreshold','limitation'],additionalProperties=False))
    rows=[]
    for identity,split,value in [('above-rule','train',32),('below-rule','train',24),('at-rule','train',30),('validation-cool','validation',19),('test-warm','test',35)]:
        rows.append(dict(id=identity,family=identity,split=split,concepts=list(ontology['concepts']),
          source=dict(id='notella-tutorial-authored',kind='synthetic',reference='Tutorial case '+identity,permission='Project-authored demonstration; development training permitted',labelAuthor='Notella tutorial author; not field validated',trainingAllowed=True),
          input=f'Sensor {identity} reports {value} degrees Celsius. Configured threshold: 30 degrees Celsius. The rule uses strictly greater than.',
          target=dict(finding=f'The {value} degree Celsius reading '+('exceeds' if value>30 else 'does not exceed')+' the configured 30 degree Celsius threshold.',exceedsThreshold=value>30,limitation='This reading alone does not establish a fire or explain its cause.')))
    return ontology,rows

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--store',default='runtime/tutorial');args=parser.parse_args()
    api=Notella(args.store);ontology,rows=teaching_material()
    o=api.register_ontology(ontology);c=api.compile(o['id'],rows);plan=api.plan(c['id'],'configured-model-alias',steps=30)
    # This is deliberately the authored reference answer, NOT output from a model.
    fixture={'test-warm':rows[-1]['target']}
    review=api.evaluate(c['id'],fixture)
    result=dict(ontologyId=o['id'],curriculumId=c['id'],planId=plan['id'],evaluationId=review['id'],splits=c['artifact']['splits'],
      fixtureOnly=True,modelLoaded=False,trainingStarted=False,semanticAccuracyMeasured=review['artifact']['semanticAccuracyMeasured'])
    print(json.dumps(result,indent=2))
    Path(args.store,'tutorial-result.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
