import copy,json,unittest
from notella.scenarios import validate_scenario_set,validate_scenario,compile_scenario_examples
from notella.episodes import validate_episode_set
from profiles.network_scenarios.reference import teaching_scenarios,rule_state
from profiles.network_episodes.reference import teaching_episodes
from notella.core import fingerprint

class ScenarioTerminologyTests(unittest.TestCase):
 def test_public_prefixes_use_scenario_terms_without_mutating_sources(self):
  o,records=teaching_scenarios();before=copy.deepcopy(records);r=validate_scenario_set(o,records);rows=compile_scenario_examples(o,records)
  self.assertEqual((r['scenarios'],r['steps'],r['uniquePrefixes']),(7,20,11));self.assertEqual(records,before)
  frame=json.loads(rows[0]['input']);self.assertIn('scenarioId',frame);self.assertNotIn('episodeId',frame);self.assertEqual(frame['formatVersion'],'notella.scenario-prefix.v1')
  self.assertEqual(r['receipts'][0]['scenarioSha256'],fingerprint(records[0]));self.assertFalse(rows[0]['source']['trainingAllowed'])
 def test_legacy_artifacts_remain_accepted_and_unchanged(self):
  o,records=teaching_episodes();before=fingerprint(records);old=validate_episode_set(o,records);new=validate_scenario_set(o,records)
  self.assertEqual(old['steps'],new['steps']);self.assertEqual(before,fingerprint(records))
 def test_renaming_does_not_bypass_future_evidence_checks(self):
  o,records=teaching_scenarios();records[0]['steps'][0]['target']['assessment']['evidenceRefs']=['access-1']
  with self.assertRaises(ValueError):validate_scenario(o,records[0])
 def test_reference_trajectories_unchanged(self):
  o,records=teaching_scenarios()
  for record in records:
   for step in record['steps']:self.assertEqual(rule_state(record,step['asOfMs']),step['target'])
if __name__=='__main__':unittest.main()
