"""Run: python -m examples.window_tutorial"""
import json
from notella.windows import RollingInterceptWindow, LatestWindowWork

def main():
    window = RollingInterceptWindow()
    for second in range(1, 11):
        window.ingest(dict(id=f'intercept-{second}', observedAtMs=second*1000, availableAtMs=second*1000))
    first = window.advance(10000)
    window.ingest(dict(id='intercept-11', observedAtMs=11000, availableAtMs=11000))
    next_frame = window.advance(11000)
    assert first['activeCount'] == next_frame['activeCount'] == 10
    assert next_frame['expiredIds'] == ['intercept-1']
    assert [r['id'] for r in next_frame['added']] == ['intercept-11']
    assert next_frame['retainedCount'] == 9
    # Domain projection supplies complete semantic snapshots, not raw radio samples.
    work = LatestWindowWork()
    work.offer(dict(revision=1, state=dict(nodes=[dict(id='signal', count=10)], edges=[])))
    work.begin()
    assert work.finish(1, accepted=True)['accepted']
    work.offer(dict(revision=2, state=dict(nodes=[dict(id='signal', count=11)], edges=[])))
    delta = work.begin()['delta']
    assert len(delta['nodes']['updated']) == 1
    print(json.dumps(dict(active=next_frame['activeCount'], retained=next_frame['retainedCount'], added=[r['id'] for r in next_frame['added']], expired=next_frame['expiredIds'], updatedSemanticNodes=len(delta['nodes']['updated']), modelCalled=False), indent=2))

if __name__ == '__main__':
    main()
