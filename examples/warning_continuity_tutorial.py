"""Run: python -m examples.warning_continuity_tutorial"""
import json
from notella.inference_policy import OutputBudget, AssessmentContinuity, run_guarded_generation
from notella.focus import FocusMonitor


def main():
    # Synthetic, prevalidated policy outcomes; not a field threat classifier.
    expected={r:dict(criticality='critical',evidenceRefs=['trigger']) for r in (1,2)}
    continuity=AssessmentContinuity(lambda result,revision:result==expected[revision])
    monitor=FocusMonitor()
    monitor.focus('incident',1,'Validated synthetic trigger warrants focus',['site-A'],[dict(id='trigger',payload='retained evidence')])
    assert continuity.finish(expected[1],1,1)['accepted']
    failed=continuity.finish(None,2,2,'token_limit')
    warning=continuity.warning_state(monitor,failed)
    retry=OutputBudget().after_limit(input_tokens=1700)
    assert warning['activeIncidentIds']==['incident'] and warning['requiresAttention']
    assert warning['lastValidatedAssessment']['criticality']=='critical'
    assert not warning['assessmentCurrent']
    assert retry['maxNewTokens']==2396
    calls=[];events=[]
    def simulated_backend(limit):
        assert events and events[0]['activeIncidentIds']==['incident']
        calls.append(limit)
        return dict(text='incomplete synthetic output',finishReason='token_limit') if len(calls)==1 else dict(text=json.dumps(expected[2]),finishReason='complete')
    result=run_guarded_generation(simulated_backend,continuity,monitor,OutputBudget(),1700,2,lambda:2,events.append)
    assert events[0]['activeIncidentIds']==['incident']
    assert result['outcome']['accepted'] and len(result['attempts'])==2
    print(json.dumps(dict(warningAvailableWithoutExplanation=warning,retryPlan=retry,simulatedAttemptLimits=calls,warningEmittedBeforeBackend=True,finalAssessmentAccepted=result['outcome']['accepted'],realModelCalled=False),indent=2))

if __name__=='__main__':main()
