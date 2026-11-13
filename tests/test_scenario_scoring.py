import copy,json,unittest
from notella.scenario_scoring import score_scenario_output
from profiles.network_scenarios.reference import teaching_scenarios

class ScenarioScoringTests(unittest.TestCase):
 def setUp(self):self.o,self.records=teaching_scenarios();self.s=self.records[0];self.step=self.s['steps'][1]
 def score(self,target,**kwargs):return score_scenario_output(self.o,self.s,self.step['asOfMs'],json.dumps(target),**kwargs)
 def test_arbitrary_node_names_do_not_change_structural_agreement(self):
  target=copy.deepcopy(self.step['target']);mapping={n['id']:'node-'+str(i) for i,n in enumerate(target['nodes'])}
  for n in target['nodes']:n['id']=mapping[n['id']]
  for i,e in enumerate(target['edges']):e['id']='link-'+str(i);e['from']=mapping[e['from']];e['to']=mapping[e['to']]
  r=self.score(target);self.assertTrue(r['contractValid']);self.assertTrue(r['nodesMatch']);self.assertTrue(r['edgesMatch'])
 def test_correct_label_does_not_rescue_future_reference(self):
  target=copy.deepcopy(self.step['target']);target['assessment']['evidenceRefs']=['access-1'];r=self.score(target)
  self.assertTrue(r['criticalityMatch']);self.assertFalse(r['contractAndDecisionMatch'])
 def test_truncated_result_cannot_count_as_usable(self):
  r=self.score(self.step['target'],token_limit_reached=True);self.assertTrue(r['schemaValid']);self.assertFalse(r['contractAndDecisionMatch'])
 def test_missing_edge_is_reported_even_when_label_matches(self):
  target=copy.deepcopy(self.step['target']);target['edges'].pop();r=self.score(target)
  self.assertTrue(r['criticalityMatch']);self.assertFalse(r['edgesMatch']);self.assertEqual(r['missingEdgeRecords'],1)
 def test_old_evidence_cannot_be_the_only_change_justification(self):
  target=copy.deepcopy(self.step['target']);target['change']['evidenceRefs']=['scan-1'];r=self.score(target)
  self.assertFalse(r['contractValid']);self.assertIn('newly available',r['error'])
 def test_duplicate_json_keys_rejected(self):
  r=score_scenario_output(self.o,self.s,self.step['asOfMs'],'{"asOfMs":1,"asOfMs":2}')
  self.assertFalse(r['jsonValid'])


class DecisionVersusSerializationTests(unittest.TestCase):
 def test_correct_decision_can_be_reported_when_graph_schema_fails(self):
  o,records=teaching_scenarios();scenario=records[0];step=scenario['steps'][0];value=copy.deepcopy(step['target']);value['nodes'][0].pop('counts')
  r=score_scenario_output(o,scenario,step['asOfMs'],json.dumps(value))
  self.assertTrue(r['criticalityMatch']);self.assertTrue(r['assessmentStatusMatch']);self.assertFalse(r['schemaValid']);self.assertFalse(r['contractAndDecisionMatch']);self.assertFalse(r['fullStateMatch'])

if __name__=='__main__':unittest.main()
