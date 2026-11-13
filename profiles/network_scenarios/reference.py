"""Scenario terminology for the network reference profile; preserves legacy fixtures."""
import copy,re
from notella.core import fingerprint,check
from profiles.network_episodes import reference as legacy
POLICY_ID='network-scenario-policy-v1-development'

def ontology():
    value=copy.deepcopy(legacy.ontology());value['name']='Network scenario semantic interpretation';value['version']='0.1.2-development'
    value['instruction']=value['instruction'].replace(legacy.POLICY_ID,POLICY_ID)
    value['instruction']=re.sub(r'\bepisode\b','scenario',value['instruction'])
    return value

def teaching_scenarios():
    _,records=legacy.teaching_episodes();definition=ontology();identity=fingerprint(definition)
    for record in records:
        record.update(formatVersion='notella.scenario.v1',ontologyId=identity,policyId=POLICY_ID)
        record['source'].update(id='network-scenario-authoring-v1',reference='profiles/network_scenarios/reference.py')
    return definition,records

def rule_state(scenario,as_of):
    check(scenario['policyId']==POLICY_ID,'Unknown network scenario policy')
    value=copy.deepcopy(scenario);value['policyId']=legacy.POLICY_ID
    return legacy.rule_state(value,as_of)
