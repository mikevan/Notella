"""Machine-readable discovery for API clients."""
def specification():
    text={'type':'string'}
    def body(properties,required):return {'type':'object','properties':properties,'required':required}
    requests={
      'ontologies':body({'name':text,'version':text,'concepts':{'type':'object','additionalProperties':text},'relations':{'type':'array','items':body({'subject':text,'predicate':text,'object':text},['subject','predicate','object'])},'instruction':text,'outputSchema':{'type':'object'}},['name','version','concepts','relations','instruction','outputSchema']),
      'curricula':body({'ontologyId':text,'examples':{'type':'array','items':{'type':'object'}},'excludedPromptHashes':{'type':'array','items':text}},['ontologyId','examples']),
      'plans':body({'curriculumId':text,'baseModel':text,'steps':{'type':'integer','minimum':1,'maximum':100000},'rank':{'type':'integer','minimum':1,'maximum':128},'learningRate':{'type':'number','exclusiveMinimum':0,'maximum':0.001}},['curriculumId','baseModel']),
      'jobs':body({'planId':text},['planId']),
      'interpretation-reviews':body({'curriculumId':text,'exampleId':text,'output':text,'reviewer':body({'name':text,'kind':{'type':'string','enum':['human','agent']},'independent':{'type':'boolean'}},['name','kind','independent']),'criteria':{'type':'array','items':body({'id':text,'description':text},['id','description'])},'judgments':{'type':'array','items':body({'criterionId':text,'status':{'type':'string','enum':['pass','fail','not_assessed']},'rationale':text},['criterionId','status','rationale'])},'split':{'type':'string','enum':['validation','test']}},['curriculumId','exampleId','output','reviewer','criteria','judgments']),
      'evaluations':body({'curriculumId':text,'predictions':{'type':'object'},'split':{'type':'string','enum':['validation','test']}},['curriculumId','predictions'])}
    paths={'/health':{'get':{'security':[],'responses':{'200':{'description':'Service health'}}}}}
    for resource,schema in requests.items():
        paths['/v1/'+resource]={'post':{'operationId':'create_'+resource,'requestBody':{'required':True,'content':{'application/json':{'schema':schema}}},'responses':{'201':{'description':'Created artifact or training job'},'400':{'description':'Validation failure'},'401':{'description':'Unauthorized'}}}}
        paths['/v1/'+resource+'/{id}']={'get':{'operationId':'get_'+resource,'parameters':[{'name':'id','in':'path','required':True,'schema':text}],'responses':{'200':{'description':'Stored artifact or job'},'404':{'description':'Not found'}}}}
    return {'openapi':'3.1.0','info':{'title':'Notella API','version':'0.1.0','description':'Ontology-guided semantic LoRA training. Local developer API.'},'servers':[{'url':'http://127.0.0.1:8765'}],
      'security':[{'bearerAuth':[]}],'components':{'securitySchemes':{'bearerAuth':{'type':'http','scheme':'bearer'}}},'paths':paths}
