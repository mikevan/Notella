"""Validate declared output states. Rejected answers are never repaired or rescored as correct."""
import hashlib,json
from .core import canonical,check,validate_schema

def inspect_output(output,schema,allowed_states,fields):
    check(type(output) is str,'Exact output text required')
    check(isinstance(fields,list) and fields and all(type(k) is str for k in fields) and len(set(fields))==len(fields),'Invalid contract fields')
    check(isinstance(allowed_states,list) and allowed_states,'Allowed states required')
    for state in allowed_states:check(isinstance(state,dict) and set(state)==set(fields),'Allowed state fields differ from contract')
    result=dict(checksPassed=False,jsonValid=False,schemaValid=False,stateConsistent=False,value=None,violations=[],
        outputSha256=hashlib.sha256(output.encode()).hexdigest(),groundTruthVerified=False,rewritten=False)
    def unique(pairs):
        check(len({key for key,_ in pairs})==len(pairs),'Duplicate JSON key');return dict(pairs)
    try:
        value=json.loads(output,object_pairs_hook=unique);canonical(value);result.update(jsonValid=True,value=value)
    except (ValueError,TypeError) as error:
        result['violations'].append(dict(code='invalid_json',message=str(error)));return result
    try:validate_schema(value,schema);result['schemaValid']=True
    except (ValueError,TypeError) as error:result['violations'].append(dict(code='schema_failure',message=str(error)))
    if isinstance(value,dict) and set(fields)<=set(value):
        selected={k:value[k] for k in fields}
        result['stateConsistent']=canonical(selected) in {canonical(s) for s in allowed_states}
    if not result['stateConsistent']:result['violations'].append(dict(code='inconsistent_state',message='Output fields do not form a declared allowed state.'))
    result['checksPassed']=not result['violations'];return result
