"""Domain-neutral full-prefix episode contracts. No model or automatic policy inference."""
import copy
from .core import canonical,check,fingerprint,ontology_validate,validate_schema
from .correlation import temporal_link


def episode_output_schema(concepts):
    """Closed graph-state v1 contract; profiles may add stricter constraints."""
    text=dict(type='string',minLength=1)
    refs=dict(type='array',items=text,minItems=1,uniqueItems=True)
    counts=dict(type='object',additionalProperties=False,required=['reportCount','underlyingEventCount','provenanceRootCount'],properties={k:dict(type='integer',minimum=0) for k in ['reportCount','underlyingEventCount','provenanceRootCount']})
    node=dict(type='object',additionalProperties=False,required=['id','kind','concept','assetRef','status','evidenceRefs','counts'],properties=dict(id=text,kind=dict(type='string',enum=['observation','hypothesis']),concept=dict(type='string',enum=list(concepts)),assetRef=text,status=dict(type='string',enum=['observed','retracted','proposed','supported','weakened','withdrawn']),evidenceRefs=refs,counts=counts))
    edge=dict(type='object',additionalProperties=False,required=['id','from','to','relation','status','evidenceRefs','counts'],properties={'id':text,'from':text,'to':text,'relation':text,'status':dict(type='string',enum=['active','inactive']),'evidenceRefs':refs,'counts':counts})
    assessment=dict(type='object',additionalProperties=False,required=['criticality','status','evidenceRefs','rationale'],properties=dict(criticality=dict(type='string',enum=['contextual','high','critical']),status=dict(type='string',enum=['assessed','review_required']),evidenceRefs=refs,rationale=text))
    change=dict(type='object',additionalProperties=False,required=['evidenceRefs','summary'],properties=dict(evidenceRefs=refs,summary=text))
    return dict(type='object',additionalProperties=False,required=['asOfMs','nodes','edges','assessment','change'],properties=dict(asOfMs=dict(type='integer',minimum=0),nodes=dict(type='array',minItems=1,items=node),edges=dict(type='array',items=edge),assessment=assessment,change=change))

def evidence_counts(evidence,refs):
    """Counts are provenance assertions, never confidence or statistical independence."""
    rows=[evidence[r] for r in refs]
    return dict(reportCount=len(rows),underlyingEventCount=len({e['originEventId'] for e in rows}),provenanceRootCount=len({e['sourceRoot'] for e in rows}))

def visible_evidence(episode,as_of):
    return [copy.deepcopy(e) for e in episode['evidence'] if e['availableAtMs']<=as_of]

def _text(value,label):check(isinstance(value,str) and bool(value.strip()),label+' required')
def _time(value,label):check(type(value) is int and value>=0,label+' must be nonnegative integer milliseconds')
def _refs(refs,available,label):
    check(isinstance(refs,list) and bool(refs) and all(isinstance(r,str) for r in refs),label+' requires evidence references')
    check(len(refs)==len(set(refs)) and set(refs)<=set(available),label+' contains duplicate, unknown or future evidence')

def validate_episode(ontology,episode):
    """Validate declared structure, visibility, provenance consistency and graph transitions.

    Does not establish physical truth, reviewer independence, causal inference or
    correct domain criticality. Domain policy needs a separate reference/review.
    """
    ontology_validate(ontology);canonical(episode)
    check(episode.get('formatVersion')=='notella.episode.v1','Unsupported episode format')
    for k in ('id','family','policyId','primaryAsset'):_text(episode.get(k),k)
    check(episode.get('split') in ('train','validation','test'),'Invalid episode split')
    check(episode.get('ontologyId')==fingerprint(ontology),'Episode ontology identity mismatch')
    check(episode.get('timeBasis') in ('shared-clock-asserted','unresolved'),'Unsupported episode time basis')
    assets=episode.get('assets');check(isinstance(assets,list) and assets and all(isinstance(a,str) and a for a in assets) and len(assets)==len(set(assets)),'Unique assets required')
    check(episode['primaryAsset'] in assets,'Primary asset outside scope')
    source=episode.get('source');check(isinstance(source,dict),'Source required')
    for k in ('id','kind','reference','permission','labelAuthor'):_text(source.get(k),'source.'+k)
    check(source['kind'] in ('synthetic','document','field'),'Invalid source kind')
    check(type(source.get('trainingAllowed')) is bool,'Explicit training admission status required')
    check(isinstance(episode.get('evidence'),list) and episode['evidence'],'Evidence required')
    evidence={};origins={}
    for e in episode['evidence']:
        check(isinstance(e,dict),'Evidence must be an object')
        for k in ('id','concept','assetRef','sourceRoot','originEventId','statement'):_text(e.get(k),'evidence.'+k)
        check(e['id'] not in evidence,'Duplicate evidence id');check(e['concept'] in ontology['concepts'],'Unknown evidence concept');check(e['assetRef'] in assets,'Evidence asset outside scope')
        for k in ('timeMs','uncertaintyMs','availableAtMs'):_time(e.get(k),'evidence.'+k)
        # The occurrence interval's lower bound cannot be wholly after availability.
        if episode['timeBasis']=='shared-clock-asserted':
            check(e['timeMs']-e['uncertaintyMs']<=e['availableAtMs'],'Evidence available before its possible occurrence')
        signature=canonical({k:e[k] for k in ('concept','assetRef','timeMs','uncertaintyMs','sourceRoot','statement')})
        check(e['originEventId'] not in origins or origins[e['originEventId']]==signature,'Same underlying event has conflicting provenance or content')
        origins[e['originEventId']]=signature;evidence[e['id']]=e
    for e in evidence.values():
        if 'explains' in e:
            check(isinstance(e['explains'],list) and bool(e['explains']) and all(isinstance(r,str) for r in e['explains']),'Explanation references required')
            check(len(e['explains'])==len(set(e['explains'])),'Duplicate explanation reference')
            for ref in e['explains']:
                check(ref in evidence and ref!=e['id'] and evidence[ref]['availableAtMs']<e['availableAtMs'],'Explanation needs previously available evidence')
                check(evidence[ref]['assetRef']==e['assetRef'],'Explanation crosses asset scope')
        if 'retracts' in e:
            check(isinstance(e['retracts'],list) and bool(e['retracts']) and all(isinstance(r,str) for r in e['retracts']),'Retraction references required')
            check(len(e['retracts'])==len(set(e['retracts'])),'Duplicate retraction reference')
            for ref in e['retracts']:
                check(ref in evidence and ref!=e['id'],'Unknown/self retraction')
                target=evidence[ref]
                check(target['availableAtMs']<e['availableAtMs'],'Retraction must refer to previously available evidence')
                check('retracts' not in target,'Retraction of a correction is outside v1 scope')
                check(target['assetRef']==e['assetRef'],'Retraction crosses asset scope')
    allowed={(r['subject'],r['predicate'],r['object']) for r in ontology['relations']}
    check(isinstance(episode.get('steps'),list) and episode['steps'],'Steps required')
    previous_time=-1;previous_nodes={};previous_edges={};prefix_hashes=[]
    for step in episode['steps']:
        check(isinstance(step,dict),'Step must be an object')
        _time(step.get('asOfMs'),'asOfMs');now=step['asOfMs'];check(now>previous_time,'Step cutoffs must increase strictly')
        available={e['id']:e for e in visible_evidence(episode,now)};check(available,'Empty episode prefix')
        newly_available=set(available)-{e['id'] for e in visible_evidence(episode,previous_time)}
        check(newly_available,'Each v1 step requires newly available evidence')
        target=step.get('target');validate_schema(target,episode_output_schema(ontology['concepts']));validate_schema(target,ontology['outputSchema'])
        check(target['asOfMs']==now,'Target cutoff mismatch')
        withdrawn={ref for e in available.values() for ref in e.get('retracts',[])}
        withdrawn_origins={available[ref]['originEventId'] for ref in withdrawn}
        withdrawn={r for r,e in available.items() if e['originEventId'] in withdrawn_origins}
        nodes={};represented=set()
        for node in target['nodes']:
            check(node['id'] not in nodes,'Duplicate node id');check(node['concept'] in ontology['concepts'],'Unknown node concept');check(node['assetRef'] in assets,'Node asset outside scope')
            _refs(node['evidenceRefs'],available,'Node');check(node['counts']==evidence_counts(available,node['evidenceRefs']),'Node match counts inconsistent')
            if node['kind']=='observation':
                check(len(node['evidenceRefs'])==1,'Observation node must bind one report')
                ref=node['evidenceRefs'][0];event=available[ref];check(ref not in represented,'One report has multiple observation nodes');represented.add(ref)
                check(node['concept']==event['concept'] and node['assetRef']==event['assetRef'],'Observation node changes supplied concept or asset')
                check(node['status']==('retracted' if ref in withdrawn else 'observed'),'Observation retraction status mismatch')
            else:
                check(node['status'] in ('proposed','supported','weakened','withdrawn'),'Invalid hypothesis state')
            check(node['kind']!='hypothesis' or node['status']!='supported' or bool(set(node['evidenceRefs'])-withdrawn),'Supported hypothesis relies entirely on retracted evidence')
            if node['id'] in previous_nodes:
                old=previous_nodes[node['id']]
                check(all(node[k]==old[k] for k in ('kind','concept','assetRef')),'Existing node identity changed')
                if node!=old and node['kind']=='hypothesis':
                    check(bool(set(node['evidenceRefs'])&newly_available),'Changed node lacks newly available justification')
            nodes[node['id']]=node
        check(represented==set(available),'Target must retain every visible report, including retractions and duplicates')
        check(set(previous_nodes)<=set(nodes),'Previously recorded nodes disappeared')
        edges={}
        for edge in target['edges']:
            check(edge['id'] not in edges,'Duplicate edge id');check(edge['from'] in nodes and edge['to'] in nodes and edge['from']!=edge['to'],'Unknown/self edge endpoint')
            a=nodes[edge['from']];b=nodes[edge['to']]
            check((a['concept'],edge['relation'],b['concept']) in allowed,'Undeclared ontology relationship')
            check(a['assetRef']==b['assetRef'],'Cross-asset links require a future explicit bridge contract')
            _refs(edge['evidenceRefs'],available,'Edge');check(edge['counts']==evidence_counts(available,edge['evidenceRefs']),'Edge match counts inconsistent')
            if edge['status']=='active':
                check(not (set(edge['evidenceRefs'])&withdrawn),'Active edge cites withdrawn evidence')
                check(a['status'] not in ('retracted','withdrawn') and (edge['relation']=='contradicts' or b['status'] not in ('retracted','withdrawn')),'Active support/order edge has withdrawn endpoint')
                if edge['relation']=='precedes':
                    check(a['kind']==b['kind']=='observation','Precedes requires observation endpoints')
                    ea=available[a['evidenceRefs'][0]];eb=available[b['evidenceRefs'][0]]
                    check(set(a['evidenceRefs']+b['evidenceRefs'])<=set(edge['evidenceRefs']),'Temporal edge must cite endpoint reports')
                    check(episode.get('timeBasis')=='shared-clock-asserted','Temporal comparison requires asserted shared clock')
                    check(temporal_link(ea['timeMs'],eb['timeMs'],ea['uncertaintyMs'],eb['uncertaintyMs'])['order']=='after','Unsupported temporal precedence')
            if edge['id'] in previous_edges:
                old=previous_edges[edge['id']]
                check(all(edge[k]==old[k] for k in ('from','to','relation')),'Existing edge identity changed')
                if edge!=old:check(bool(set(edge['evidenceRefs'])&newly_available),'Changed edge lacks newly available justification')
            edges[edge['id']]=edge
        check(set(previous_edges)<=set(edges),'Previously recorded edges disappeared')
        assessment=target['assessment'];_refs(assessment['evidenceRefs'],available,'Assessment')
        check(not(set(assessment['evidenceRefs'])&withdrawn),'Assessment cites withdrawn evidence as active support')
        if assessment['criticality']=='critical':check(assessment['status']=='assessed','Critical assessment cannot be deferred')
        _refs(target['change']['evidenceRefs'],available,'Change')
        check(bool(set(target['change']['evidenceRefs'])&newly_available),'Change must cite new evidence')
        previous_time=now;previous_nodes=nodes;previous_edges=edges
        prefix_hashes.append(fingerprint(dict(policyId=episode['policyId'],primaryAsset=episode['primaryAsset'],assets=episode['assets'],timeBasis=episode.get('timeBasis'),asOfMs=now,evidence=list(available.values()))))
    return dict(episodeId=episode['id'],steps=len(episode['steps']),prefixSha256=prefix_hashes,episodeSha256=fingerprint(episode),semanticCorrectnessEstablished=False,sourceAuthenticityVerified=False)

def validate_episode_set(ontology,episodes):
    check(isinstance(episodes,list) and bool(episodes),'Episode list required')
    ids=set();families={};receipts=[];inputs={}
    for episode in episodes:
        check(episode['id'] not in ids,'Duplicate episode identity');ids.add(episode['id'])
        family=episode['family'];split=episode['split'];check(family not in families or families[family]==split,'Episode family crosses splits');families[family]=split
        receipt=validate_episode(ontology,episode);receipts.append(receipt)
        for digest in receipt['prefixSha256']:
            check(digest not in inputs or inputs[digest]==(family,split),'Shared prefix changes original family or split');inputs[digest]=(family,split)
    return dict(episodes=len(episodes),steps=sum(r['steps'] for r in receipts),uniquePrefixes=len(inputs),originalFamilies=len(families),receipts=receipts,semanticCorrectnessEstablished=False)

def compile_episode_examples(ontology,episodes):
    """Full visible-prefix reconstruction. Never sends prior/future authored targets."""
    validate_episode_set(ontology,episodes);rows=[]
    for episode in episodes:
        for i,step in enumerate(episode['steps']):
            frame=dict(formatVersion='notella.episode-prefix.v1',episodeId=episode['id'],policyId=episode['policyId'],primaryAsset=episode['primaryAsset'],assets=episode['assets'],timeBasis=episode.get('timeBasis'),asOfMs=step['asOfMs'],evidence=visible_evidence(episode,step['asOfMs']))
            rows.append(dict(id=episode['id']+'-step-'+str(i+1),family=episode['family'],split=episode['split'],concepts=list(ontology['concepts']),source=copy.deepcopy(episode['source']),input=canonical(frame),target=copy.deepcopy(step['target'])))
    return rows
