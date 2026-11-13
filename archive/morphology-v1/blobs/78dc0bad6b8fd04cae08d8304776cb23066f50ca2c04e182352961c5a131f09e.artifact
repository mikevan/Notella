"""Domain-neutral ontology and curriculum API. Standard library only."""
import hashlib
import json
import math
import re
import os
import uuid
from pathlib import Path

class ValidationError(ValueError): pass

def canonical(value):
    try: return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)
    except (TypeError, ValueError) as e: raise ValidationError(str(e)) from e

def fingerprint(value): return hashlib.sha256(canonical(value).encode()).hexdigest()

def check(condition, message):
    if not condition: raise ValidationError(message)

def validate_schema(value, schema, path='$'):
    """Deliberately small, fail-closed JSON Schema subset; unsupported keywords rejected."""
    supported={'type','properties','required','additionalProperties','items','enum','const','minLength','maxLength','minItems','maxItems','uniqueItems','minimum','maximum','description'}
    check(isinstance(schema,dict),f'{path}: schema must be an object')
    check(not set(schema)-supported,f'{path}: unsupported schema keywords: {set(schema)-supported}')
    types={'object':dict,'array':list,'string':str,'integer':int,'number':(int,float),'boolean':bool,'null':type(None)}
    if 'type' in schema:
        t=schema['type'];check(isinstance(t,str) and t in types,f'{path}: unsupported type')
        check(isinstance(value,types[t]) and not (t in ('integer','number') and isinstance(value,bool)),f'{path}: expected {t}')
    if 'const' in schema: check(canonical(value)==canonical(schema['const']),f'{path}: const mismatch')
    if 'enum' in schema: check(canonical(value) in [canonical(v) for v in schema['enum']],f'{path}: enum mismatch')
    if isinstance(value,dict):
        props=schema.get('properties',{})
        check(set(schema.get('required',[]))<=set(value),f'{path}: missing required fields')
        if schema.get('additionalProperties') is False:check(set(value)<=set(props),f'{path}: unknown fields')
        for key,item in value.items():
            if key in props:validate_schema(item,props[key],path+'.'+key)
    if isinstance(value,list):
        check(len(value)>=schema.get('minItems',0) and len(value)<=schema.get('maxItems',math.inf),f'{path}: array length')
        if schema.get('uniqueItems'):check(len({canonical(x) for x in value})==len(value),f'{path}: repeated item')
        for i,item in enumerate(value):
            if 'items' in schema:validate_schema(item,schema['items'],f'{path}[{i}]')
    if isinstance(value,str):check(len(value)>=schema.get('minLength',0) and len(value)<=schema.get('maxLength',math.inf),f'{path}: string length')
    if type(value) in (float,int):check(math.isfinite(value) and value>=schema.get('minimum',-math.inf) and value<=schema.get('maximum',math.inf),f'{path}: numeric range')

def schema_definition(schema):
    supported={'type','properties','required','additionalProperties','items','enum','const','minLength','maxLength','minItems','maxItems','uniqueItems','minimum','maximum','description'}
    check(isinstance(schema,dict) and not set(schema)-supported,'Unsupported output schema')
    if 'type' in schema:check(schema['type'] in ('object','array','string','integer','number','boolean','null'),'Unsupported schema type')
    if 'additionalProperties' in schema:check(type(schema['additionalProperties']) is bool,'additionalProperties must be boolean')
    if 'uniqueItems' in schema:check(type(schema['uniqueItems']) is bool,'uniqueItems must be boolean')
    for key in ('minLength','maxLength','minItems','maxItems'):
        if key in schema:check(type(schema[key]) is int and schema[key]>=0,'Invalid schema bound')
    for key in ('minimum','maximum'):
        if key in schema:check(type(schema[key]) in (float,int) and math.isfinite(schema[key]),'Invalid numeric schema bound')
    for low,high in (('minLength','maxLength'),('minItems','maxItems'),('minimum','maximum')):
        if low in schema and high in schema:check(schema[low]<=schema[high],'Reversed schema bounds')
    if 'enum' in schema:check(isinstance(schema['enum'],list) and schema['enum'],'enum must be a nonempty array')
    if 'properties' in schema:
        check(isinstance(schema['properties'],dict),'properties must be an object')
        for child in schema['properties'].values():schema_definition(child)
    if 'required' in schema:check(isinstance(schema['required'],list) and all(isinstance(k,str) for k in schema['required']) and set(schema['required'])<=set(schema.get('properties',{})),'Invalid required properties')
    if 'items' in schema:schema_definition(schema['items'])

def ontology_validate(o):
    canonical(o)
    check(isinstance(o,dict),'Ontology must be an object')
    for k in ('name','version','concepts','relations','instruction','outputSchema'):check(k in o,f'Missing ontology field: {k}')
    for k in ('name','version','instruction'):check(isinstance(o[k],str) and o[k].strip(),f'{k} must be nonempty text')
    check(isinstance(o['concepts'],dict) and o['concepts'],'Concepts must be a nonempty mapping')
    for key,definition in o['concepts'].items():check(isinstance(definition,str) and definition.strip(),f'Empty definition: {key}')
    check(isinstance(o['relations'],list),'Relations must be an array')
    for r in o['relations']:
        check(isinstance(r,dict) and set(r)=={'subject','predicate','object'},'Relation requires subject, predicate, object')
        check(r['subject'] in o['concepts'] and r['object'] in o['concepts'],'Unknown relation concept')
        check(isinstance(r['predicate'],str) and r['predicate'].strip(),'Empty relation predicate')
    check(isinstance(o['outputSchema'],dict),'outputSchema must be an object')
    schema_definition(o['outputSchema'])
    return o

class Notella:
    """Immutable content-addressed artifacts; share this API across apps and transports."""
    def __init__(self, root):
        self.root=Path(root).resolve();self.root.mkdir(parents=True,exist_ok=True)
        for kind in ('ontologies','curricula','evaluations','plans'): (self.root/kind).mkdir(exist_ok=True)

    def put(self, kind, value):
        check(kind in ('ontologies','curricula','evaluations','plans'),'Unknown artifact type')
        raw=canonical(value);identity=hashlib.sha256(raw.encode()).hexdigest()
        path=self.root/kind/(identity+'.json')
        tmp=path.with_name(uuid.uuid4().hex+'.tmp')
        try:
            tmp.write_text(raw+'\n',encoding='utf-8')
            try:os.link(tmp,path)
            except FileExistsError:check(path.read_text(encoding='utf-8').strip()==raw,'Artifact integrity mismatch')
        finally:tmp.unlink(missing_ok=True)
        return {'id':identity,'artifact':value}

    def get(self,kind,identity):
        check(kind in ('ontologies','curricula','evaluations','plans'),'Unknown artifact type')
        check(isinstance(identity,str) and re.fullmatch('[0-9a-f]{64}',identity),'Invalid artifact ID')
        path=self.root/kind/(identity+'.json')
        if not path.exists():raise FileNotFoundError(identity)
        value=json.loads(path.read_text(encoding='utf-8'))
        check(fingerprint(value)==identity,'Stored artifact integrity failed')
        return value

    def register_ontology(self,ontology):return self.put('ontologies',ontology_validate(ontology))

    def compile(self,ontology_id,examples,exclusions=None):
        o=self.get('ontologies',ontology_id);check(isinstance(examples,list) and examples,'Examples must be a nonempty array')
        blocked=set(exclusions or []);ids=set();families={};prompts={};rows=[];counts={s:0 for s in ('train','validation','test')}
        instruction=o['instruction']+'\nOntology: '+canonical({'concepts':o['concepts'],'relations':o['relations']})+'\nReturn JSON matching: '+canonical(o['outputSchema'])
        for e in examples:
            check(isinstance(e,dict),'Example must be an object')
            for k in ('id','family','split','concepts','source','input','target'):check(k in e,f'Missing example field: {k}')
            check(isinstance(e['id'],str) and e['id'] and e['id'] not in ids,'Duplicate or invalid example ID');ids.add(e['id'])
            split=e['split'];check(isinstance(split,str) and split in counts,'Invalid split')
            family=e['family'];check(isinstance(family,str) and family,'Invalid family')
            check(family not in families or families[family]==split,'Family crosses splits');families[family]=split
            check(isinstance(e['concepts'],list) and e['concepts'] and set(e['concepts'])<=set(o['concepts']),'Unknown or empty concepts')
            source=e['source'];check(isinstance(source,dict),'Source must be an object')
            check(all(isinstance(source.get(k),str) and source[k].strip() for k in ('id','kind','reference','permission','labelAuthor')),'Source provenance is incomplete')
            check(source['kind'] in ('synthetic','document','field'),'Invalid source kind')
            if split=='train':check(source.get('trainingAllowed') is True,'Source not admitted for training')
            check(isinstance(e['input'],str) and e['input'].strip(),'Input must be nonempty text')
            validate_schema(e['target'],o['outputSchema'])
            prompt=[dict(role='system',content=instruction),dict(role='user',content=e['input'])]
            ph=fingerprint(prompt);input_hash=fingerprint(e['input'])
            check(ph not in blocked and input_hash not in blocked,'Excluded evaluation prompt entered curriculum')
            check(input_hash not in prompts or prompts[input_hash]==split,'Input crosses splits');prompts[input_hash]=split
            rows.append(dict(id=e['id'],family=family,split=split,concepts=e['concepts'],source=source,promptSha256=ph,
                datasetVersion='notella-curriculum-v1',outputSchema=canonical(o['outputSchema']),
                messages=prompt+[dict(role='assistant',content=canonical(e['target']))]))
            counts[split]+=1
        check(counts['train']>0,'At least one training example is required')
        return self.put('curricula',dict(formatVersion='notella.curriculum.v1',ontologyId=ontology_id,
            examples=rows,splits=counts,excludedPromptHashes=sorted(blocked),releaseEligible=False,
            limitations=['Schema and integrity validation do not establish semantic correctness.','Synthetic variants are not independent field incidents.']))

    def plan(self,curriculum_id,base_model,steps=100,rank=16,learning_rate=0.00005):
        c=self.get('curricula',curriculum_id)
        check(isinstance(base_model,str) and base_model.strip(),'baseModel must be a configured model identifier')
        check(type(steps) is int and 1<=steps<=100000,'steps outside 1..100000')
        check(type(rank) is int and 1<=rank<=128,'rank outside 1..128')
        check(type(learning_rate) in (float,int) and math.isfinite(learning_rate) and 0<learning_rate<=0.001,'Invalid learning rate')
        return self.put('plans',dict(formatVersion='notella.plan.v1',curriculumId=curriculum_id,baseModel=base_model,
            steps=steps,rank=rank,learningRate=learning_rate,splits=c['splits'],releaseEligible=False))

    def evaluate(self,curriculum_id,predictions,split='test'):
        check(split in ('validation','test'),'Evaluation split must be validation or test')
        c=self.get('curricula',curriculum_id);o=self.get('ontologies',c['ontologyId'])
        check(isinstance(predictions,dict),'Predictions must map example IDs to JSON objects')
        expected={e['id']:e for e in c['examples'] if e['split']==split}
        check(expected,'Selected split has no examples');check(set(predictions)<=set(expected),'Unknown or wrong-split prediction')
        results=[]
        for identity,e in expected.items():
            item=dict(id=identity,present=identity in predictions,schemaValid=False,exactTargetMatch=False)
            if item['present']:
                try:validate_schema(predictions[identity],o['outputSchema']);item['schemaValid']=True
                except ValidationError as error:item['error']=str(error)
                item['exactTargetMatch']=canonical(predictions[identity])==e['messages'][-1]['content']
            results.append(item)
        return self.put('evaluations',dict(curriculumId=curriculum_id,split=split,results=results,
            total=len(results),schemaPasses=sum(r['schemaValid'] for r in results),
            exactTargetMatches=sum(r['exactTargetMatch'] for r in results),semanticAccuracyMeasured=False,releaseEligible=False))
