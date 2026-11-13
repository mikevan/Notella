import unittest
from notella.inference_policy import OutputBudget, AssessmentContinuity, run_guarded_generation
from notella.focus import FocusMonitor

class InferencePolicyTests(unittest.TestCase):
    def test_retry_grows_within_context(self):
        b = OutputBudget()
        self.assertEqual(b.allowance(1700),1536)
        self.assertEqual(b.after_limit(1700)['maxNewTokens'],2396)
        self.assertEqual(b.after_limit(1700,1)['action'],'review')

    def test_context_exhaustion_and_invalid_budgets(self):
        b=OutputBudget(context_tokens=2000)
        self.assertEqual(b.after_limit(1800)['reason'],'context_or_output_budget_exhausted')
        with self.assertRaises(ValueError):b.allowance(2000)
        with self.assertRaises(ValueError):OutputBudget(max_retries=99)

    def test_cap_cannot_clear_validated_warning_or_focus(self):
        c=AssessmentContinuity(lambda a,r:a.get('criticality')=='critical')
        self.assertTrue(c.finish(dict(criticality='critical'),1,1)['accepted'])
        m=FocusMonitor();m.focus('incident',1,'Validated trigger',['site'],[dict(id='trigger')])
        failed=c.finish(dict(criticality='contextual'),2,2,'token_limit')
        self.assertFalse(failed['accepted']);self.assertFalse(failed['clearanceApplied'])
        self.assertEqual(failed['lastValidatedAssessment']['criticality'],'critical')
        warning=c.warning_state(m,failed)
        self.assertTrue(warning['requiresAttention']);self.assertEqual(warning['activeIncidentIds'],['incident'])
        self.assertFalse(warning['assessmentCurrent'])

    def test_first_generation_failure_does_not_invent_a_threat_level(self):
        c=AssessmentContinuity(lambda a,r:True)
        r=c.finish(None,1,1,'generation_error')
        self.assertIsNone(r['lastValidatedAssessment']);self.assertTrue(r['requiresAttention'])

    def test_stale_and_invalid_results_do_not_replace_history(self):
        c=AssessmentContinuity(lambda a,r: a.get('evidenceRefs')==['valid'])
        c.finish(dict(evidenceRefs=['valid']),1,1)
        for r in [c.finish(dict(evidenceRefs=['wrong']),2,2),c.finish(dict(evidenceRefs=['valid']),2,3)]:
            self.assertFalse(r['accepted']);self.assertEqual(r['lastValidatedRevision'],1)
        self.assertTrue(c.finish(dict(evidenceRefs=['valid']),3,3)['accepted'])

    def test_failed_new_revision_still_prevents_backwards_evidence_history(self):
        c=AssessmentContinuity(lambda a,r:True)
        c.finish(dict(criticality='critical'),1,1)
        c.finish(None,4,4,'token_limit')
        with self.assertRaises(ValueError):c.finish(dict(criticality='contextual'),3,3)

    def test_non_json_assessment_returns_incomplete_without_losing_history(self):
        c=AssessmentContinuity(lambda a,r:True)
        c.finish(dict(criticality='critical'),1,1)
        r=c.finish(dict(invalid={1,2}),2,2)
        self.assertFalse(r['accepted']);self.assertEqual(r['lastValidatedRevision'],1)

    def test_validated_deescalation_remains_possible(self):
        c=AssessmentContinuity(lambda a,r:True)
        c.finish(dict(criticality='critical'),1,1)
        r=c.finish(dict(criticality='contextual'),2,2)
        self.assertTrue(r['accepted']);self.assertEqual(r['lastValidatedAssessment']['criticality'],'contextual')

class GuardedGenerationTests(unittest.TestCase):
    def setup(self):
        c=AssessmentContinuity(lambda a,r:a==dict(criticality='critical'))
        c.finish(dict(criticality='critical'),1,1)
        m=FocusMonitor();m.focus('incident',1,'Validated trigger',['site'],[dict(id='trigger')])
        return c,m

    def test_warning_is_exposed_before_generation_and_retry(self):
        c,m=self.setup();events=[];calls=[]
        def generate(limit):
            self.assertTrue(events);self.assertEqual(events[0]['activeIncidentIds'],['incident'])
            calls.append(limit)
            return dict(text='partial',finishReason='token_limit') if len(calls)==1 else dict(text='{"criticality":"critical"}',finishReason='complete')
        result=run_guarded_generation(generate,c,m,OutputBudget(),1700,2,lambda:2,events.append)
        self.assertEqual(calls,[1536,2396]);self.assertTrue(result['outcome']['accepted']);self.assertIsNone(result['retryPlan'])
        self.assertEqual(result['attempts'][0]['text'],'partial');self.assertEqual(len(events),3)

    def test_repetition_cannot_retry_forever(self):
        c,m=self.setup();calls=[]
        def generate(limit):calls.append(limit);return dict(text='repeat',finishReason='token_limit')
        result=run_guarded_generation(generate,c,m,OutputBudget(),1700,2,lambda:2,lambda s:None)
        self.assertEqual(len(calls),2);self.assertFalse(result['outcome']['accepted'])
        self.assertEqual(result['warning']['activeIncidentIds'],['incident'])

    def test_stale_input_is_not_retried(self):
        c,m=self.setup();latest=[2]
        def generate(limit):latest[0]=3;return dict(text='partial',finishReason='token_limit')
        result=run_guarded_generation(generate,c,m,OutputBudget(),1700,2,lambda:latest[0],lambda s:None)
        self.assertEqual(len(result['attempts']),1);self.assertEqual(result['outcome']['reason'],'stale_result')

    def test_complete_old_result_can_be_explicitly_revalidated_against_live_evidence(self):
        c,m=self.setup();latest=[2];checks=[]
        def generate(limit):latest[0]=3;return dict(text='{"criticality":"critical"}',finishReason='complete')
        def revalidate(value,original,current):checks.append((original,current));return value==dict(criticality='critical')
        result=run_guarded_generation(generate,c,m,OutputBudget(),1700,2,lambda:latest[0],lambda s:None,revalidate=revalidate)
        self.assertTrue(result['outcome']['accepted']);self.assertEqual(checks,[(2,3)])
        self.assertEqual(result['attempts'][0]['inputRevision'],2)
        self.assertEqual(result['outcome']['lastValidatedRevision'],3)

    def test_revalidation_cannot_accept_while_current_evidence_changes_again(self):
        c,m=self.setup();latest=[2]
        def generate(limit):latest[0]=3;return dict(text='{"criticality":"critical"}',finishReason='complete')
        def revalidate(value,original,current):latest[0]=4;return True
        result=run_guarded_generation(generate,c,m,OutputBudget(),1700,2,lambda:latest[0],lambda s:None,revalidate=revalidate)
        self.assertFalse(result['outcome']['accepted']);self.assertEqual(result['outcome']['reason'],'stale_result')

    def test_normal_pending_broad_monitoring_does_not_invent_an_alert(self):
        c=AssessmentContinuity(lambda a,r:True);m=FocusMonitor();events=[]
        run_guarded_generation(lambda n:dict(text='{}',finishReason='complete'),c,m,OutputBudget(),100,1,lambda:1,events.append)
        self.assertEqual(events[0]['inferenceStatus'],'assessment_pending')
        self.assertFalse(events[0]['requiresAttention'])

    def test_backend_failure_preserves_prior_warning(self):
        c,m=self.setup();events=[]
        def generate(limit):raise RuntimeError('backend failure')
        result=run_guarded_generation(generate,c,m,OutputBudget(),1700,2,lambda:2,events.append)
        self.assertEqual(result['outcome']['reason'],'generation_error')
        self.assertEqual(result['warning']['lastValidatedAssessment']['criticality'],'critical')
        self.assertEqual(len(events),2)

    def test_duplicate_json_keys_are_not_repaired_or_accepted(self):
        c,m=self.setup()
        result=run_guarded_generation(lambda n:dict(text='{"criticality":"contextual","criticality":"critical"}',finishReason='complete'),c,m,OutputBudget(),1700,2,lambda:2,lambda s:None)
        self.assertFalse(result['outcome']['accepted']);self.assertEqual(len(result['attempts']),1)

if __name__=='__main__':unittest.main()
