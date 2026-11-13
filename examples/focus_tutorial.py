"""Run: python -m examples.focus_tutorial"""
import json
from notella.windows import RollingInterceptWindow
from notella.focus import FocusMonitor

def main():
    window = RollingInterceptWindow()
    window.ingest(dict(id='report-1', observedAtMs=1000, availableAtMs=1000, payload={'entity':'site-A', 'kind':'reviewed-interesting-pattern'}))
    frame = window.advance(10000)
    monitor = FocusMonitor()
    # A domain policy or validated AI assessment supplies this decision.
    monitor.focus('incident-A', frame['revision'], 'Validated pattern warrants tracking', ['site-A'], frame['added'])
    expired = window.advance(11000)
    focused = monitor.plan(['site-A'])
    assert expired['expiredIds'] == ['report-1']
    assert focused['priorityIncidentIds'] == ['incident-A']
    assert 'report-1' in monitor.snapshot()['incident-A']['evidence']
    assert monitor.plan(['site-B'])['priorityIncidentIds'] == []
    monitor.resolve('incident-A', expired['revision'], 'Reviewed independent evidence resolves the concern', 'evidence_review')
    print(json.dumps(dict(afterExpiry=focused, afterResolution=monitor.plan([]), retainedEvidence=list(monitor.snapshot()['incident-A']['evidence']), modelCalled=False), indent=2))

if __name__ == '__main__': main()
