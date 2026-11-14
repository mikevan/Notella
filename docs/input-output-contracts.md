# Tutorial 9: bind a semantic task to trusted input and output contracts

People need findings anchored to evidence rather than instructions hidden inside captured material. Explicit input and output boundaries help keep tools for self-protection accountable without treating an untrusted payload as authority.

**Outcome:** keep irrelevant captured instructions out of a decision task, represent source provenance explicitly and reject inconsistent answers without rewriting them. This tutorial uses synthetic fixtures and loads no model.

## Run the working example

From C:\workspace\Notella:

```powershell
python -m examples.decision_contract_tutorial
```

Expect fixtureOnly=true, modelLoaded=false, capturedTextExcluded=true, origin groups [0,1], validOutputChecksPassed=true, inconsistentOutputRejected=true, outputRepaired=false and groundTruthVerified=false. These demonstrate contract behavior, not model accuracy.

## Separate the four responsibilities

1. Preserve the original observation. It remains available in the source artifact; projection does not edit it.
2. Project only fields relevant to this particular decision task. The LayerTime adapter accepts controlled observation kinds, area references, time measurements and a caller-supplied provenance registry. Raw captured text and free-form context are not model instructions.
3. Train and infer with the same typed representation and trusted ontology instructions. A model trained on the old descriptive format should not be assumed to perform equally on a new format.
4. Check generated output against declared allowed states and necessary evidence relationships. Keep the raw answer and its hash. Rejection means review is required, not that a replacement decision is known.

Notella's generic compiler does not automatically apply these profile-specific boundaries to every application. Callers must invoke the projection and output checks when integrating this task. Other tasks may need different fields, including safely handled text; the rule is task-specific, not blanket deletion of evidence.

## Represent lineage as assertions, not word matching

```python
from notella.lineage import summarize_lineage

registry = {
    'relay-a': {'originRef': 'report-7', 'reviewed': True},
    'relay-b': {'originRef': 'report-7', 'reviewed': True},
}
result = summarize_lineage(['relay-a', 'relay-b'], registry)
print(result['summary'])
```

Expect two records, originGroups=[0,0], one reviewed distinct origin and relationship=shared_origin. Two differently named reports do not become independent evidence. Unknown or unreviewed entries remain unknown rather than receiving invented origins.

The model sees counts, origin groups and controlled relationship labels. Raw source-label text and registry origin strings remain outside its decision view. The receipt keeps their hashes and registry assertions for audit.

**Registry lookup is not authentication.** Registry keys must represent trustworthy collector identities bound to reviewed provenance. Advertised SSIDs, spoofable radio addresses or arbitrary report text do not establish trusted origin. The included registry is authored synthetic material; reviewed=true does not certify independent field verification. Distinct provenance roots also do not prove statistical independence.

## Project a LayerTime observation

```python
from profiles.layertime.decision_contract import project_observation

projection = project_observation(observation, registry, ongoing_threat=True)
if not projection['eligibleForModel']:
    print(projection['unsupportedConditions'])
else:
    model_input = projection['modelInput']
```

Use the complete observation from the runnable example. The ongoing_threat boolean comes from trusted owner configuration; it is not inferred from captured text. The adapter's closed legacy kind/location dictionaries map the existing authored fixtures. Unknown kinds or areas are not guessed. This is not a general-purpose sensor classifier or geocoder.

The model input contains controlled classifications, canonical area references, lineage topology and measured temporal relations. It contains no warning target. The receipt retains the original observation hash, registry receipt, time calculation and assumption scope.

Inputs outside the current output taxonomy are deferred. Examples include unreviewed source lineage, uncertainty straddling the timing-window boundary, and an unsupported standing-context case. Deferral is not a negative finding or a low-threat assessment. Preserve the evidence and route it for review rather than silently downgrading a warning.

## Declare allowed output states

```python
from notella.output_contracts import inspect_output

allowed_states = [
    {'posture': 'critical', 'combinedTrigger': 'met', 'evidenceClass': 'corroborated_drone'},
    {'posture': 'high', 'combinedTrigger': 'unconfirmed', 'evidenceClass': 'unidentified_signal'},
]
result = inspect_output(exact_generated_text, schema, allowed_states,
                        ['posture', 'combinedTrigger', 'evidenceClass'])
```

Supply the schema and exact output as in the runnable example. Individual field values can be legal while their combination is contradictory. The helper checks both schema and the declared state combination; duplicate JSON keys and malformed output are rejected. It does not rewrite the answer or claim ground truth.

The LayerTime-specific inspect_warning_output also checks necessary relations: a met temporal trigger needs a supported later interval within the window; a reversed reason needs earlier order; an unknown-time reason needs unresolved time; and critical evidence needs the supplied context, deliberate disruption, corroborated identity, distinct reviewed origins and matching areas. Other reason codes are checked against the typed facts. These checks validate the declared policy consistency, not the truth of sensors or the policy's empirical effectiveness.

For a simple, fully structured safety policy, deterministic code can compute or validate many decisions directly. This experiment trains consistent execution of the semantic task; it does not justify making an SLM the sole authority for a rule that can be checked reliably in code.

## Keep evaluation roles honest after normalization

Projection deliberately removes irrelevant differences. Several old examples that differed only by clock origin become identical typed inputs. Counting them as fresh held-out tests after training on that view would be misleading.

The v6 pack reports 45 training rows, 30 authored source variants, 24 distinct projected inputs and 15 explicit replays separately. Its ten new development controls have zero exact cross-split input overlap. They remain related synthetic patterns, not independent field validation. Old anchors and payload/alias probes are reported as known-template regressions.

A captured-text invariance pass means the decision view does not change when excluded text changes. It is not proof that the model learned to resist adversarial instructions. A source-alias invariance pass can come from the registry and projection; do not attribute it to learned semantic generalization without a separate test.

## Reproduce and inspect results

The frozen inputs and compatibility diagnostic are in experiments/warning-v5-contracts. The typed training profile, new controls and protocol are in experiments/warning-v6-typed-training. The latter's profile.json reproduces its exact ontology, curriculum and plan through prepare_profile.

Keep raw agreement, schema compliance, contract passes, accepted-wrong, rejected-correct and input deferrals separate. Neither rejection nor deferral increases model accuracy. Model weights and runtime outputs remain local; no result here is a phone-installation or field-release qualification.
