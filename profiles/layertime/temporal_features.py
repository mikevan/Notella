"""LayerTime profile adapter: measured temporal relations, never warning decisions."""
import hashlib,math
from notella.core import canonical,check
from notella.correlation import temporal_link

SHARED_CLOCK='relative milliseconds on a shared clock'

def derive_temporal_fact(observation):
    check(isinstance(observation,dict),'Observation must be an object')
    a=observation['disruption'];b=observation['drone'];window=observation['linkingWindowMs']
    for value in (a['uncertaintyMs'],b['uncertaintyMs'],window):
        check(type(value) in (int,float) and math.isfinite(value) and value>=0,'Invalid uncertainty/window')
    check(window>0,'Window must be positive')
    for event in (a,b):
        value=event['timeMs'];check(value is None or type(value) in (int,float) and math.isfinite(value),'Invalid timestamp')
    comparable=observation.get('timeBasis')==SHARED_CLOCK
    if comparable:
        measurement=temporal_link(a['timeMs'],b['timeMs'],a['uncertaintyMs'],b['uncertaintyMs'],window)
    else:
        measurement=dict(order='unknown',withinWindow=None,causationEstablished=False,reason='Shared-clock alignment is not supplied; times cannot be compared.')
    return dict(factId='computed_temporal_link',value=dict(
        kind='derived_measurement',algorithm='notella.correlation.temporal_link',algorithmVersion='interval-v1',
        sourceFactId='capture_summary',sourceObservationSha256=hashlib.sha256(canonical(observation).encode()).hexdigest(),
        clockComparabilityAssertedByInput=comparable,clockAlignmentIndependentlyVerified=False,
        configuredWindowMs=window,measurement=measurement,
        scope='Timestamp interval arithmetic only; no drone identity, source independence, warning posture or attack probability is computed.'))
