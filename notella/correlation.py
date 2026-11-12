"""Clock-aware temporal association; never converts timing into causal probability."""
import math
from .core import check

def temporal_link(a_ms,b_ms,a_uncertainty_ms=0,b_uncertainty_ms=0,window_ms=120000):
    if a_ms is None or b_ms is None:
        return dict(order='unknown',withinWindow=None,causationEstablished=False,reason='Missing timestamp')
    values=(a_ms,b_ms,a_uncertainty_ms,b_uncertainty_ms,window_ms)
    check(all(type(v) in (int,float) and math.isfinite(v) for v in values),'Times must be finite numbers')
    check(a_uncertainty_ms>=0 and b_uncertainty_ms>=0 and window_ms>0,'Invalid uncertainty or window')
    low=(b_ms-b_uncertainty_ms)-(a_ms+a_uncertainty_ms)
    high=(b_ms+b_uncertainty_ms)-(a_ms-a_uncertainty_ms)
    order='after' if low>0 else 'before' if high<0 else 'uncertain'
    inside=True if low>0 and high<=window_ms else False if high<=0 or low>window_ms else None
    return dict(order=order,delayIntervalMs=[low,high],withinWindow=inside,causationEstablished=False,
        reason='Timing qualifies association only; identity, location, provenance and alternatives require separate evidence')
