import copy,json,tempfile,unittest
from notella import Notella,ValidationError
from notella.episodes import validate_episode,validate_episode_set,compile_episode_examples
from profiles.network_episodes.reference import teaching_episodes,rule_state

class EpisodeTests(unittest.TestCase):
 def setUp(self):self.ontology,self.episodes=teaching_episodes()
 def test_full_set_and_future_evidence_exclusion(self):
  r=validate_episode_set(self.ontology,self.episodes);self.assertEqual((r['episodes'],r['steps']),(7,20))
  rows=compile_episode_examples(self.ontology,self.episodes)
  first=json.loads(rows[0]['input']);self.assertEqual([e['id'] for e in first['evidence']],['scan-1'])
  self.assertNotIn('target',first);self.assertNotIn('steps',first);self.assertFalse(rows[0]['source']['trainingAllowed'])
 def test_future_reference_rejected(self):
  e=self.episodes[0];e['steps'][0]['target']['assessment']['evidenceRefs'].append('access-1')
  with self.assertRaisesRegex(ValidationError,'future'):validate_episode(self.ontology,e)
 def test_prefix_must_preserve_all_variants_in_one_split(self):
  self.episodes[1]['split']='test'
  with self.assertRaisesRegex(ValidationError,'family crosses'):validate_episode_set(self.ontology,self.episodes)
 def test_relabelling_a_shared_prefix_cannot_bypass_split_guard(self):
  self.episodes[1]['family']='invented-new-family';self.episodes[1]['split']='test'
  with self.assertRaisesRegex(ValidationError,'Shared prefix'):validate_episode_set(self.ontology,self.episodes)
 def test_duplicate_reports_do_not_multiply_underlying_support(self):
  e=next(e for e in self.episodes if e['id']=='duplicate-reports');state=e['steps'][-1]['target'];h=next(n for n in state['nodes'] if n['kind']=='hypothesis')
  self.assertEqual(h['counts'],dict(reportCount=2,underlyingEventCount=1,provenanceRootCount=1));self.assertEqual(state['assessment']['criticality'],'contextual')
 def test_forged_deduplication_count_rejected(self):
  e=self.episodes[0];e['steps'][0]['target']['nodes'][-1]['counts']['underlyingEventCount']=2
  with self.assertRaisesRegex(ValidationError,'counts inconsistent'):validate_episode(self.ontology,e)
 def test_source_correction_revises_without_erasing_history(self):
  e=next(e for e in self.episodes if e['id']=='source-correction')
  self.assertEqual([s['target']['assessment']['criticality'] for s in e['steps']],['contextual','high','critical','high'])
  final=e['steps'][-1]['target'];self.assertEqual(next(n for n in final['nodes'] if n['id']=='obs:access-1')['status'],'retracted')
  self.assertTrue(any(edge['status']=='inactive' and edge['from']=='obs:access-1' for edge in final['edges']))
 def test_retracted_evidence_cannot_remain_active_support(self):
  e=next(e for e in self.episodes if e['id']=='source-correction');edge=next(x for x in e['steps'][-1]['target']['edges'] if x['from']=='obs:access-1' and x['relation']=='supports');edge['status']='active'
  with self.assertRaisesRegex(ValidationError,'withdrawn'):validate_episode(self.ontology,e)
 def test_cross_asset_link_rejected(self):
  e=next(e for e in self.episodes if e['id']=='unrelated-asset');state=e['steps'][-1]['target'];edge=copy.deepcopy(state['edges'][0]);edge['id']='false-link';edge['from']='obs:scan-other';edge['evidenceRefs']=['scan-other'];state['edges'].append(edge)
  with self.assertRaisesRegex(ValidationError,'Cross-asset'):validate_episode(self.ontology,e)
 def test_overlapping_time_does_not_establish_precedence(self):
  e=self.episodes[0];e['evidence'][1]['uncertaintyMs']=4000
  with self.assertRaisesRegex(ValidationError,'temporal precedence'):validate_episode(self.ontology,e)
 def test_late_arrival_is_not_available_in_earlier_prefix(self):
  e=next(e for e in self.episodes if e['id']=='late-arrival');rows=compile_episode_examples(self.ontology,[e]);self.assertNotIn('access-late',json.loads(rows[1]['input'])['evidence'][0]['id'])
  self.assertFalse(any(x['id']=='access-late' for x in json.loads(rows[1]['input'])['evidence']))
  self.assertFalse(any(x['from']=='obs:auth-1' and x['to']=='obs:access-late' for x in e['steps'][-1]['target']['edges']))
 def test_observations_and_edges_cannot_disappear(self):
  e=self.episodes[0];e['steps'][1]['target']['nodes']=[n for n in e['steps'][1]['target']['nodes'] if n['id']!='obs:scan-1']
  with self.assertRaises(ValidationError):validate_episode(self.ontology,e)
 def test_unknown_clock_requires_review_and_has_no_order_edge(self):
  e=next(e for e in self.episodes if e['id']=='unresolved-clock');final=e['steps'][-1]['target'];self.assertEqual(final['assessment']['status'],'review_required');self.assertFalse(any(x['relation']=='precedes' for x in final['edges']))
 def test_unreviewed_material_cannot_enter_training(self):
  with tempfile.TemporaryDirectory() as d:
   api=Notella(d);oid=api.register_ontology(self.ontology)['id']
   with self.assertRaisesRegex(ValidationError,'not admitted'):api.compile(oid,compile_episode_examples(self.ontology,self.episodes))
 def test_contract_validity_does_not_prove_criticality_correctness(self):
  e=self.episodes[0];e['steps'][0]['target']['assessment']['criticality']='critical'
  validate_episode(self.ontology,e)
  self.assertNotEqual(e['steps'][0]['target'],rule_state(e,e['steps'][0]['asOfMs']))


class EpisodeBoundaryRegressionTests(unittest.TestCase):
 def test_loose_domain_schema_cannot_bypass_core_graph_contract(self):
  o,episodes=teaching_episodes();o['outputSchema']={'type':'object'}
  from notella.core import fingerprint
  e=episodes[0];e['ontologyId']=fingerprint(o);e['steps'][0]['target']={}
  with self.assertRaises(ValidationError):validate_episode(o,e)
 def test_benign_explanation_applies_to_reposts_of_the_same_event(self):
  o,episodes=teaching_episodes();e=next(e for e in episodes if e['id']=='benign-branch');dup=copy.deepcopy(e['evidence'][1]);dup['id']='auth-repost';dup['availableAtMs']=6500;e['evidence'].insert(2,dup)
  self.assertEqual(rule_state(e,e['steps'][-1]['asOfMs'])['assessment']['criticality'],'contextual')
 def test_duplicate_observation_nodes_rejected(self):
  o,episodes=teaching_episodes();e=episodes[0];dup=copy.deepcopy(e['steps'][0]['target']['nodes'][0]);dup['id']='copy-of-report';e['steps'][0]['target']['nodes'].append(dup)
  with self.assertRaisesRegex(ValidationError,'multiple observation nodes'):validate_episode(o,e)



class CorrectionRelationshipTests(unittest.TestCase):
 def test_correction_can_contradict_a_retained_withdrawn_claim(self):
  o,episodes=teaching_episodes();e=next(e for e in episodes if e['id']=='source-correction');validate_episode(o,e)
  final=e['steps'][-1]['target'];edge=next(x for x in final['edges'] if x['from']=='obs:correction-1')
  self.assertEqual((edge['relation'],edge['status'],edge['to']),('contradicts','active','obs:access-1'))
  self.assertEqual(edge['evidenceRefs'],['correction-1'])



class ClockDomainTests(unittest.TestCase):
 def test_unresolved_occurrence_clock_is_not_compared_to_ingest_clock(self):
  o,episodes=teaching_episodes();e=next(e for e in episodes if e['id']=='unresolved-clock');e['evidence'][1]['timeMs']=999000000
  validate_episode(o,e)
  self.assertEqual(rule_state(e,e['steps'][-1]['asOfMs'])['assessment']['status'],'review_required')

if __name__=='__main__':unittest.main()
