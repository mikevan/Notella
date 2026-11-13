"""No-model scenario-scoring example; fixtures are not model predictions."""
import copy,json
from notella.scenario_scoring import score_scenario_output
from profiles.network_scenarios.reference import teaching_scenarios

def main():
 ontology,scenarios=teaching_scenarios();scenario=scenarios[0];step=scenario['steps'][1];target=step['target']
 good=score_scenario_output(ontology,scenario,step['asOfMs'],json.dumps(target))
 bad=copy.deepcopy(target);bad['assessment']['evidenceRefs']=['access-1']
 rejected=score_scenario_output(ontology,scenario,step['asOfMs'],json.dumps(bad))
 assert good['fullStateMatch'] and rejected['criticalityMatch'] and not rejected['contractAndDecisionMatch']
 print(json.dumps(dict(fixtureOnly=True,modelLoaded=False,referenceStateMatches=good['fullStateMatch'],correctLabelWithFutureEvidenceRejected=not rejected['contractAndDecisionMatch'],semanticAccuracyMeasured=False),indent=2))
if __name__=='__main__':main()
