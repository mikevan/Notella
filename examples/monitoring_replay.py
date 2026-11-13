"""Synthetic end-to-end reference replay, not an RF detector or trained policy.

Run: python -m examples.monitoring_replay
"""
import json
from notella.windows import RollingInterceptWindow, semantic_delta
from notella.focus import FocusMonitor


def project(records):
    """Example ontology projection of already-classified, trusted demo reports."""
    nodes = []
    for record in sorted(records, key=lambda r: r['id']):
        payload = record['payload']
        nodes.append(dict(id=record['id'], concept=payload['kind'], entityKey=payload['site'], observedAtMs=record['observedAtMs']))
    edges = []
    for first in nodes:
        for second in nodes:
            if (first['concept'] == 'wifi_disruption' and second['concept'] == 'drone_signature'
                    and first['entityKey'] == second['entityKey']
                    and 0 < second['observedAtMs'] - first['observedAtMs'] <= 10000):
                edges.append(dict(id=first['id']+'->'+second['id'], relation='observed_before', source=first['id'], target=second['id'], entityKey=first['entityKey']))
    return dict(nodes=nodes, edges=edges)


def run_replay():
    window = RollingInterceptWindow()
    monitor = FocusMonitor()
    active = {}
    previous = dict(nodes=[], edges=[])
    reports = [
        dict(id='wifi-1', observedAtMs=1000, availableAtMs=1000, payload=dict(site='camp-A', kind='wifi_disruption')),
        dict(id='drone-1', observedAtMs=5000, availableAtMs=5000, payload=dict(site='camp-A', kind='drone_signature')),
        dict(id='related-1', observedAtMs=7000, availableAtMs=7000, payload=dict(site='camp-A', kind='unidentified_signal')),
        dict(id='other-1', observedAtMs=11000, availableAtMs=11000, payload=dict(site='site-B', kind='unidentified_signal')),
    ]
    events = []
    for end in range(1000, 17000, 1000):
        for report in reports:
            if report['availableAtMs'] == end:
                assert window.ingest(report)['accepted']
        frame = window.advance(end)
        for identity in frame['expiredIds']:
            active.pop(identity, None)
        active.update({r['id']:r for r in frame['added']})
        state = project(active.values())
        delta = semantic_delta(previous, state)
        changed = sorted({r['payload']['site'] for r in frame['added']} | {
            n['entityKey'] for n in delta['nodes']['removed']})
        for edge in delta['edges']['added']:
            # Illustrative conservative policy, not causation or attack probability.
            identity = 'incident:'+edge['id']
            monitor.focus(identity, frame['revision'],
                'Same-site Wi-Fi disruption followed by drone signature: precautionary focused tracking; causation unproven',
                [edge['entityKey']], [active[edge['source']], active[edge['target']]])
        # Preserve new related evidence while the incident is focused.
        for identity, incident in monitor.snapshot().items():
            related = [r for r in frame['added'] if r['payload']['site'] in incident['entityKeys']]
            if incident['status'] == 'focused' and related:
                monitor.focus(identity, frame['revision'], 'Additional related report retained', incident['entityKeys'], related)
        plan = monitor.plan(changed)
        events.append(dict(endMs=end, activeIntercepts=frame['activeCount'], added=[r['id'] for r in frame['added']], expired=frame['expiredIds'], newEdges=len(delta['edges']['added']), plan=plan))
        previous = state
    return dict(synthetic=True, modelCalled=False, events=events, incidents=monitor.snapshot())


def main():
    result = run_replay()
    print(json.dumps(result, indent=2))

if __name__ == '__main__': main()
