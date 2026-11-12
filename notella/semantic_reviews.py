"""Hash-bound interpretation reviews; records judgments without pretending to automate them."""
import hashlib,json
from .core import check,canonical,validate_schema

def record_review(api,curriculum_id,example_id,output,reviewer,criteria,judgments,split='validation'):
    """Store exact output and criterion judgments as a separately typed evaluation artifact.

    reviewer: {name, kind: human|agent, independent: bool}; independence is an assertion.
    criteria: [{id, description}]; judgments: [{criterionId, status, rationale}].
    This does not infer semantic truth from JSON validity or score a model automatically.
    """
    check(split in ('validation','test'),'Review only held-out validation or test examples')
    corpus=api.get('curricula',curriculum_id)
    examples=[e for e in corpus['examples'] if e['id']==example_id and e['split']==split]
    check(len(examples)==1,'Unknown or wrong-split review example')
    check(type(output) is str and output.strip(),'Review output must be the exact nonempty generated text')
    check(isinstance(reviewer,dict) and set(reviewer)=={'name','kind','independent'},'Reviewer requires name, kind and independent')
    check(type(reviewer['name']) is str and reviewer['name'].strip(),'Reviewer name is required')
    check(reviewer['kind'] in ('human','agent') and type(reviewer['independent']) is bool,'Invalid reviewer metadata')
    check(isinstance(criteria,list) and criteria,'Review criteria are required')
    criterion_ids=set()
    for c in criteria:
        check(isinstance(c,dict) and set(c)=={'id','description'},'Criterion requires id and description')
        check(all(type(c[k]) is str and c[k].strip() for k in ('id','description')),'Criterion fields must be nonempty strings')
        check(c['id'] not in criterion_ids,'Duplicate criterion');criterion_ids.add(c['id'])
    check(isinstance(judgments,list),'Judgments must be an array')
    seen=set()
    for j in judgments:
        check(isinstance(j,dict) and set(j)=={'criterionId','status','rationale'},'Judgment requires criterionId, status and rationale')
        check(j['criterionId'] in criterion_ids and j['criterionId'] not in seen,'Unknown or duplicate criterion judgment');seen.add(j['criterionId'])
        check(j['status'] in ('pass','fail','not_assessed'),'Invalid judgment status')
        check(type(j['rationale']) is str and j['rationale'].strip(),'Judgment rationale required')
    check(seen==criterion_ids,'Every criterion needs an explicit judgment')
    schema_valid=False;schema_error=None
    try:
        value=json.loads(output);ontology=api.get('ontologies',corpus['ontologyId']);validate_schema(value,ontology['outputSchema']);schema_valid=True
    except (ValueError,TypeError) as error:schema_error=str(error)
    return api.put('evaluations',dict(formatVersion='notella.interpretation-review.v1',curriculumId=curriculum_id,
        exampleId=example_id,split=split,promptSha256=examples[0]['promptSha256'],
        output=output,outputSha256=hashlib.sha256(output.encode('utf-8')).hexdigest(),
        reviewer=reviewer,criteria=criteria,criteriaSha256=hashlib.sha256(canonical(criteria).encode()).hexdigest(),judgments=judgments,
        schemaValid=schema_valid,schemaError=schema_error,
        allCriteriaPassed=all(j['status']=='pass' for j in judgments),
        automaticallyMeasuredSemanticAccuracy=False,releaseEligible=False,
        limitations=['Judgments and reviewer independence are recorded assertions, not independently verified facts.','A review of selected outputs is not a field accuracy estimate.']))
