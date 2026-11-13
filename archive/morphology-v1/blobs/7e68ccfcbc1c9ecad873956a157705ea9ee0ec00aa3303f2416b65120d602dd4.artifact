"""Separate JSON compliance from declared decision-field agreement. No semantic judge."""
import json
from .core import canonical,check,validate_schema

def score_output(output,target,schema,fields):
    """Score exact generated text against predeclared fields, even when schema fails.

    Field agreement is a bounded contract check, not proof of explanation correctness.
    The original text remains untouched; callers should retain its hash and provenance.
    """
    check(type(output) is str,'Output must be exact generated text')
    check(isinstance(fields,list) and fields and all(type(k) is str and k for k in fields),'Nonempty score fields required')
    check(len(set(fields))==len(fields),'Duplicate score field')
    check(isinstance(target,dict) and set(fields)<=set(target),'Score field absent from target')
    validate_schema(target,schema)
    result=dict(jsonValid=False,schemaValid=False,fieldMatches={k:False for k in fields},
        decisionFieldsMatch=False,schemaAndDecisionMatch=False,semanticAccuracyMeasured=False)
    def unique_object(pairs):
        check(len({key for key,_ in pairs})==len(pairs),'Duplicate JSON key')
        return dict(pairs)
    try:value=json.loads(output,object_pairs_hook=unique_object);canonical(value);result['jsonValid']=True
    except (ValueError,TypeError) as error:result['error']=str(error);return result
    try:validate_schema(value,schema);result['schemaValid']=True
    except (ValueError,TypeError) as error:result['error']=str(error)
    if isinstance(value,dict):
        result['fieldMatches']={k:k in value and canonical(value[k])==canonical(target[k]) for k in fields}
    result['decisionFieldsMatch']=all(result['fieldMatches'].values())
    result['schemaAndDecisionMatch']=result['schemaValid'] and result['decisionFieldsMatch']
    return result
