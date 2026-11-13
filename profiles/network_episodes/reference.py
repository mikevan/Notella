"""A proposed, synthetic network-episode semantic model and explicit rule baseline.

Classifications and provenance are supplied assertions. This is not a detector,
causal model, production risk policy, or independently reviewed curriculum.
"""
import copy
from notella.core import fingerprint,canonical,check
from notella.episodes import visible_evidence,evidence_counts,episode_output_schema
from notella.correlation import temporal_link

POLICY_ID='network-episode-policy-v1-development'

def ontology():
    concepts=dict(reconnaissance='An observed scan of an identified asset; not proof of compromise.',credential_activity='Observed authentication failures; not proof of successful access.',compromise_evidence='A supplied reviewed assertion of unauthorized privileged access; authenticity is established outside this model.',benign_operation='A supplied reviewed explanation for explicitly referenced observations; not a universal clearance.',source_correction='An explicit retraction of earlier available evidence; retain the claim and its correction.',attack_hypothesis='A scoped interpretation of potentially related hostile activity, distinct from causal proof or perpetrator attribution.')
    schema=episode_output_schema(concepts)
    relations=[dict(subject=c,predicate='supports',object='attack_hypothesis') for c in ['reconnaissance','credential_activity','compromise_evidence']]
    relations += [dict(subject='benign_operation',predicate='contradicts',object='attack_hypothesis'),dict(subject='source_correction',predicate='contradicts',object='compromise_evidence'),dict(subject='reconnaissance',predicate='precedes',object='credential_activity'),dict(subject='credential_activity',predicate='precedes',object='compromise_evidence')]
    instruction='The ontology represents the semantic model. Reconstruct the evidence-backed semantic state from only the visible episode prefix and interpret its morphology. Preserve observations, duplicates, corrections and previous graph identities. Use policy '+POLICY_ID+': primary asset only; retractions invalidate all reports of the retracted underlying event. A current supplied reviewed compromise_evidence assertion warrants critical. Otherwise reconnaissance followed by credential_activity on the primary asset, with strictly supported order and an entire delay interval within 120000 ms, warrants high. Either alone is contextual. A benign_operation negates this scan/credential association only when its explains list covers both reports; it does not negate separate compromise evidence. Unresolved clocks or uncertain order for an otherwise relevant pair require review, not a guessed link. After a compromise retraction reassess the remaining evidence. Do not link unrelated assets, turn report counts into independent corroboration, or infer causation, actor identity or numerical attack probability. Full-prefix reconstruction is not evidence of persistent model memory.'
    return dict(name='Network episode semantic interpretation',version='0.1.1-development',concepts=concepts,relations=relations,instruction=instruction,outputSchema=schema)

def rule_state(episode,as_of):
    """Explicit development reference; never learns or consults future evidence."""
    check(episode['policyId']==POLICY_ID,'Unknown network episode policy')
    visible=visible_evidence(episode,as_of);evidence={e['id']:e for e in visible}
    withdrawn_origins={evidence[r]['originEventId'] for e in visible for r in e.get('retracts',[])}
    withdrawn={r for r,e in evidence.items() if e['originEventId'] in withdrawn_origins}
    relevant=[e for e in visible if e['assetRef']==episode['primaryAsset']]
    active=[e for e in relevant if e['id'] not in withdrawn]
    nodes=[]
    for e in visible:
        refs=[e['id']];nodes.append(dict(id='obs:'+e['id'],kind='observation',concept=e['concept'],assetRef=e['assetRef'],status='retracted' if e['id'] in withdrawn else 'observed',evidenceRefs=refs,counts=evidence_counts(evidence,refs)))
    # Counts retain reports while the policy evaluates distinct underlying events.
    unique={e['originEventId']:e for e in active};events=list(unique.values())
    scans=[e for e in events if e['concept']=='reconnaissance'];credentials=[e for e in events if e['concept']=='credential_activity'];compromise=[e for e in events if e['concept']=='compromise_evidence'];benign=[e for e in events if e['concept']=='benign_operation']
    link=False;unresolved=False;explained=False
    for a in scans:
        for b in credentials:
            if any({a['originEventId'],b['originEventId']}<={evidence[r]['originEventId'] for r in e.get('explains',[])} for e in benign):explained=True;continue
            if episode['timeBasis']!='shared-clock-asserted':unresolved=True;continue
            relation=temporal_link(a['timeMs'],b['timeMs'],a['uncertaintyMs'],b['uncertaintyMs'],120000)
            link |= relation['order']=='after' and relation['withinWindow'] is True
            unresolved |= relation['order']=='uncertain' or (relation['order']=='after' and relation['withinWindow'] is None)
    if compromise:level='critical';status='supported';rationale='The visible prefix contains supplied reviewed unauthorized-access evidence on the primary asset.'
    elif link:level='high';status='supported';rationale='A supported scan-to-authentication sequence remains on the primary asset; compromise is not established.'
    elif explained:level='contextual';status='weakened';rationale='A supplied benign explanation covers the referenced scan and authentication observations; no separate current compromise evidence remains.'
    elif withdrawn:level='contextual';status='weakened';rationale='Retraction removes the compromise support; remaining evidence does not establish the configured scan/authentication link.'
    else:level='contextual';status='proposed';rationale='The available primary-asset evidence does not establish the configured association or compromise.'
    active_refs=[e['id'] for e in active]
    if not active_refs:active_refs=[e['id'] for e in relevant if e['concept']=='source_correction']
    check(bool(active_refs),'Profile requires visible primary-asset evidence')
    hypothesis=dict(id='hypothesis:primary',kind='hypothesis',concept='attack_hypothesis',assetRef=episode['primaryAsset'],status=status,evidenceRefs=active_refs,counts=evidence_counts(evidence,active_refs));nodes.append(hypothesis)
    edges=[]
    corrections=[e['id'] for e in relevant if e.get('retracts')]
    for e in relevant:
        if e['concept'] not in ('reconnaissance','credential_activity','compromise_evidence','benign_operation'):continue
        refs=[e['id']];retired=e['id'] in withdrawn
        if retired:refs+=corrections
        edges.append(dict(id='interpret:'+e['id'],**{'from':'obs:'+e['id'],'to':hypothesis['id']},relation='contradicts' if e['concept']=='benign_operation' else 'supports',status='inactive' if retired else 'active',evidenceRefs=refs,counts=evidence_counts(evidence,refs)))
    # Persist temporal edges once created, marking them inactive after a retraction.
    allowed_pairs={('reconnaissance','credential_activity'),('credential_activity','compromise_evidence')}
    if episode['timeBasis']=='shared-clock-asserted':
        for a in relevant:
            for b in relevant:
                if (a['concept'],b['concept']) not in allowed_pairs:continue
                if temporal_link(a['timeMs'],b['timeMs'],a['uncertaintyMs'],b['uncertaintyMs'])['order']!='after':continue
                refs=[a['id'],b['id']];retired=bool(set(refs)&withdrawn)
                if retired:refs+=corrections
                refs=list(dict.fromkeys(refs));edges.append(dict(id='order:'+a['id']+':'+b['id'],**{'from':'obs:'+a['id'],'to':'obs:'+b['id']},relation='precedes',status='inactive' if retired else 'active',evidenceRefs=refs,counts=evidence_counts(evidence,refs)))
    # A correction actively contradicts the retained withdrawn claim; it does not support it.
    for e in relevant:
        for ref in e.get('retracts',[]):
            refs=[e['id']]
            edges.append(dict(id='correct:'+e['id']+':'+ref,**{'from':'obs:'+e['id'],'to':'obs:'+ref},relation='contradicts',status='active',evidenceRefs=refs,counts=evidence_counts(evidence,refs)))
    # All newly visible IDs support the change explanation; include late arrivals.
    latest=max(e['availableAtMs'] for e in visible);new_refs=[e['id'] for e in visible if e['availableAtMs']==latest]
    return dict(asOfMs=as_of,nodes=nodes,edges=edges,assessment=dict(criticality=level,status='review_required' if unresolved and not compromise else 'assessed',evidenceRefs=active_refs,rationale=rationale),change=dict(evidenceRefs=new_refs,summary='New evidence: '+', '.join(new_refs)+'. '+rationale))

def teaching_episodes():
    o=ontology();oid=fingerprint(o)
    def event(identity,concept,t,asset='host-A',**extra):return dict(id=identity,concept=concept,assetRef=asset,timeMs=t,uncertaintyMs=100,availableAtMs=t+100,sourceRoot='root:'+concept,originEventId='event:'+identity,statement='Synthetic supplied '+concept+' on '+asset,**extra)
    scan=event('scan-1','reconnaissance',1000);auth=event('auth-1','credential_activity',4000);access=event('access-1','compromise_evidence',9000)
    maintenance=event('benign-1','benign_operation',10000,explains=['scan-1','auth-1'])
    correction=event('correction-1','source_correction',13000,retracts=['access-1'])
    repost=copy.deepcopy(auth);repost['id']='auth-repost';repost['availableAtMs']=6500
    unrelated=event('scan-other','reconnaissance',9000,asset='host-B')
    late=event('access-late','compromise_evidence',2500);late['availableAtMs']=12000
    definitions=[('developing-access','access-family-001',[scan,auth,access],'shared-clock-asserted'),('benign-branch','access-family-001',[scan,auth,maintenance],'shared-clock-asserted'),('source-correction','access-family-001',[scan,auth,access,correction],'shared-clock-asserted'),('unrelated-asset','access-family-001',[scan,auth,unrelated],'shared-clock-asserted'),('duplicate-reports','duplicate-family-001',[auth,repost],'shared-clock-asserted'),('late-arrival','late-family-001',[scan,auth,late],'shared-clock-asserted'),('unresolved-clock','clock-family-001',[scan,auth],'unresolved')]
    episodes=[]
    for identity,family,events,clock in definitions:
        episode=dict(formatVersion='notella.episode.v1',id=identity,family='network-access-authored-family-001',split='train',ontologyId=oid,policyId=POLICY_ID,primaryAsset='host-A',assets=['host-A','host-B'],timeBasis=clock,evidence=copy.deepcopy(events),source=dict(id='network-episode-authoring-v1',kind='synthetic',reference='profiles/network_episodes/reference.py',permission='Project-authored development fixtures; admission pending',labelAuthor='Explicit agent-authored rule baseline, not independent domain review',trainingAllowed=False),steps=[])
        for cutoff in sorted({e['availableAtMs'] for e in events}):episode['steps'].append(dict(asOfMs=cutoff,target=rule_state(episode,cutoff)))
        episodes.append(episode)
    return o,episodes
