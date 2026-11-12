"""LayerTime decision-task boundary. Legacy fixture labels require explicit registries.

This adapter does not validate physical sensors and does not derive warning decisions.
"""
import hashlib
from notella.core import canonical,check
from notella.lineage import summarize_lineage
from notella.output_contracts import inspect_output
from .temporal_features import derive_temporal_fact

DISRUPTION_KINDS={
 'credible independently reviewed deliberate Wi-Fi denial of service':'reviewed_deliberate_disruption',
 'Wi-Fi outage; cause unknown':'outage_cause_unknown',
 'verified scheduled maintenance outage':'verified_maintenance'}
DRONE_KINDS={
 'corroborated drone presence':'corroborated_drone_identity',
 'unidentified RF signature; drone classifier uncertain':'unidentified_rf',
 'unverified drone report':'unverified_drone_report',
 'verified authorized humanitarian aid drone':'verified_humanitarian_drone'}
AREAS={'camp-area':'local_area','verified different area 20 km away':'different_area'}

def project_observation(observation,registry,ongoing_threat):
    check(isinstance(observation,dict) and type(ongoing_threat) is bool,'Observation and trusted boolean context required')
    d=observation['disruption'];b=observation['drone']
    check(d['kind'] in DISRUPTION_KINDS and b['kind'] in DRONE_KINDS,'Unmapped observation kind; review the input contract')
    check(d['location'] in AREAS and b['location'] in AREAS,'Unmapped location reference; review the input contract')
    lineage=summarize_lineage(b['sources'],registry);temporal=derive_temporal_fact(observation)
    measurement=temporal['value']['measurement']
    model=dict(formatVersion='layertime.decision-observation.v1',context=dict(ongoingThreat=ongoing_threat),
        disruption=dict(classification=DISRUPTION_KINDS[d['kind']],areaRef=AREAS[d['location']]),
        drone=dict(classification=DRONE_KINDS[b['kind']],areaRef=AREAS[b['location']],sourceLineage=lineage['summary']),
        time=dict(order=measurement['order'],withinWindow=measurement['withinWindow'],configuredWindowMs=observation['linkingWindowMs']))
    if 'delayIntervalMs' in measurement:model['time']['delayIntervalMs']=measurement['delayIntervalMs']
    unsupported=[]
    if not ongoing_threat:unsupported.append('standing_context_outside_profile')
    if lineage['summary']['relationship']=='unknown':unsupported.append('source_lineage_unknown')
    if lineage['summary']['relationship']=='single_origin' and model['drone']['classification'] in ('corroborated_drone_identity','unverified_drone_report'):
        unsupported.append('single_origin_drone_report_not_covered_by_output_taxonomy')
    if measurement['order']=='after' and measurement['withinWindow'] is None:unsupported.append('window_membership_uncertain')
    return dict(modelInput=model,eligibleForModel=not unsupported,unsupportedConditions=unsupported,
        receipt=dict(observationSha256=hashlib.sha256(canonical(observation).encode()).hexdigest(),lineage=lineage['receipt'],
          temporal=temporal,untrustedFreeTextPassedToModel=False,
          scope='Controlled legacy fixture mapping and caller assertions; not a sensor classifier, independent verification or warning decision.'))

def inspect_warning_output(output,projection,schema,allowed_states):
    result=inspect_output(output,schema,allowed_states,['posture','combinedTrigger','evidenceClass'])
    if not projection['eligibleForModel']:
        result['violations'].append(dict(code='unsupported_input',message='Input requires review before a model decision.'))
    value=result['value'];frame=projection['modelInput'];time=frame['time']
    if isinstance(value,dict) and result['schemaValid']:
        kind=value['evidenceClass'];relation=frame['drone']['sourceLineage']['relationship']
        def require(condition,code,message):
            if not condition:result['violations'].append(dict(code=code,message=message))
        if value['combinedTrigger']=='met':
            require(time['order']=='after' and time['withinWindow'] is True,'unsupported_temporal_link','A met trigger requires a supported later relation inside the configured window.')
        if kind=='reversed_sequence':require(time['order']=='before','wrong_temporal_reason','Reversed sequence requires an earlier drone observation.')
        if kind=='outside_window':require(time['order']=='after' and time['withinWindow'] is False,'wrong_temporal_reason','Outside-window reason requires a later interval outside the window.')
        if kind=='unknown_time':require(time['order']=='unknown','wrong_temporal_reason','Unknown-time reason requires unresolved time/alignment.')
        if kind=='uncertain_order':require(time['order']=='uncertain','wrong_temporal_reason','Uncertain-order reason requires overlapping time uncertainty.')
        if kind=='different_location':require(frame['drone']['areaRef']!=frame['disruption']['areaRef'],'wrong_location_reason','Different-location reason requires different area references.')
        if kind=='benign_explanation':require(frame['disruption']['classification']=='verified_maintenance' or frame['drone']['classification']=='verified_humanitarian_drone','wrong_benign_reason','No declared verified benign operation supports this reason.')
        if kind=='cause_unresolved':require(frame['disruption']['classification']=='outage_cause_unknown','wrong_cause_reason','Cause-unresolved reason requires an unresolved outage cause.')
        if kind=='unidentified_signal':require(frame['drone']['classification']=='unidentified_rf','wrong_identity_reason','This profile uses unidentified_signal for an unresolved RF identity.')
        if kind=='dependent_reports':require(relation=='shared_origin','wrong_lineage_reason','Dependent-report reason requires a shared upstream origin.')
        if value['posture']=='critical':
            require(frame['context']['ongoingThreat'] and frame['disruption']['classification']=='reviewed_deliberate_disruption'
                and frame['drone']['classification']=='corroborated_drone_identity' and relation=='distinct_reviewed_origins'
                and frame['drone']['areaRef']==frame['disruption']['areaRef'],'unsupported_critical_evidence','The supplied typed evidence does not support this critical combined trigger.')
    result['checksPassed']=not result['violations'];result['failureAction']='none' if result['checksPassed'] else 'needs_review_no_repair'
    return result
