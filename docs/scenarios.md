[Tutorial index](index.md) · [Tutorial 0: environment setup](setup.md)

# Tutorial 11: represent and validate an evolving semantic scenario

Recognizing danger requires relating observations over time. These controlled scenarios make that intended understanding testable as we develop tools for local awareness and informed decisions; they are not substitutes for field evidence.

**Outcome:** inspect a versioned semantic model, seven proposed teaching branches and their reference states, validate their evidence/graph boundaries, and export 20 prefix examples without training a model.

The ontology represents the semantic model. A prefix state represents what is supported at one point in the scenario. These fixtures teach the intended meaning of changes in nodes, typed edges, hypotheses and assessments. Their reference targets are authored with an explicit development rule baseline; they are not model-generated answers, independently reviewed truth or a calibrated threat policy.


## Terminology and scope

We use **scenario** in the simulation/training sense: the system, context, constraints and evolving events used to exercise interpretation. A **scenario instance** is one concrete realization. A **scenario family** groups instances derived from the same original authored situation; a **branch** is an alternative continuation, and a **step** is an evidence-availability cutoff with an expected semantic state/assessment. The seven records here are concrete branch instances of one authored family, not seven independent scenarios for evaluation purposes.

This usage aligns with scenario-based simulation terminology; LLM evaluation frameworks can use scenario more broadly for a task/domain/language setting. We do not claim one universal ML definition. [OpenSCENARIO introduction](https://www.asam.net/static_downloads/public/asam-openscenario/2.0.0/introduction.html) and [HELM terminology](https://crfm.stanford.edu/2022/11/17/helm.html) provide those respective contexts. We reserve episode for reinforcement-learning or other explicitly defined trajectory contexts when applicable; this workflow does not implement an RL environment, reward or action loop.

## 1. Run the tutorial

From `C:\workspace\Notella`, using Python 3.11 or later:

```powershell
python -m examples.scenario_tutorial --output runtime/scenario-tutorial-NEW
```

The directory must not already exist. No model, network connection or GPU is used. Expected summary:

```json
{
  "scenarios": 7,
  "prefixStates": 20,
  "uniqueVisiblePrefixes": 11,
  "originalFamilies": 1,
  "sharedPrefixVariants": true,
  "modelLoaded": false,
  "trainingStarted": false,
  "semanticAccuracyMeasured": false,
  "unreviewedTrainingAdmissionRefused": true
}
```

The 20 states include shared prefixes. All seven branches derive from one authored family and stay in the training split as provisional material. They are not seven independent incidents or a train/test benchmark. The tutorial verifies references against the explicit rule baseline and records receipts; it does not measure AI accuracy.

## 2. Inspect the semantic model and scenario fixtures

- [ontology.json](../profiles/network_scenarios/ontology.json): version `0.1.2-development`, concepts, typed relations, proposed policy and closed graph-state output schema.
- [scenarios.json](../profiles/network_scenarios/scenarios.json): frozen source fixtures, visible-evidence cutoffs and expected states.
- [reference.py](../profiles/network_scenarios/reference.py): transparent rule baseline and fixture-authoring helper. It is a source-checkout profile, not a detector or domain-neutral policy built into Notella.

The profile distinguishes reconnaissance, credential activity, supplied reviewed compromise evidence, benign operations, source corrections and an attack hypothesis. Its proposed policy is deliberately small: a scan alone or authentication failures alone are contextual; a supported same-asset scan/authentication sequence within 120 seconds is high; supplied current reviewed unauthorized-access evidence is critical. A scoped benign explanation can negate the scan/authentication association, but not separate compromise evidence. A correction requires reassessment of remaining evidence.

These classifications, asset identities and provenance roots are caller assertions. The profile does not classify raw traffic, independently authenticate sources, compute a calibrated attack probability, implement an asset-impact matrix or prove causation. Critical evidence persists until a correction in this v1 profile; automatic expiry/decay is not implemented.

## 3. Follow the authored reference trajectories

| Branch | Criticality trajectory | Intended distinction |
|---|---|---|
| Developing access | contextual -> high -> critical | Additional supported evidence can justify escalation. |
| Benign branch | contextual -> high -> contextual | A supported explanation can change the interpretation of earlier activity. |
| Source correction | contextual -> high -> critical -> high | Retract the invalid support, retain history and reassess the rest. |
| Unrelated asset | contextual -> high -> high | A new event on another asset does not strengthen this primary-asset hypothesis. |
| Duplicate reports | contextual -> contextual | More reports do not create more underlying observations. |
| Late arrival | contextual -> high -> critical | New knowledge can arrive late; occurrence order differs from arrival order. |
| Unresolved clock | contextual -> contextual/review | Do not invent temporal precedence from incomparable times. |

These are expected outputs of the proposed rule policy, not results from an AI. The counts do not establish the policy's field validity.

## 4. Understand the evidence contract

Each scenario has an identity, original family, split, exact ontology ID, policy ID, primary asset, asset scope, time basis, source permission/admission metadata, evidence records and authored steps.

Each evidence record includes:

| Field | Meaning |
|---|---|
| `id` | This report's identity |
| `originEventId` | The asserted upstream observation that reports repeat; not independently verified physical-event identity |
| `sourceRoot` | Asserted provenance root; distinct roots do not prove statistical independence |
| `concept` / `assetRef` | Supplied classification and asset scope |
| `timeMs` / `uncertaintyMs` | Occurrence time and uncertainty, in integer milliseconds |
| `availableAtMs` | When the report becomes available to the scenario interpreter |
| `statement` | Controlled synthetic description; not a model instruction |
| `retracts` / `explains` | Optional references to previously available evidence |

A record with an earlier occurrence time but later availability must not appear in earlier prompts. Corrections target prior reports; retracting one upstream observation invalidates all its duplicate reports as active support. Retractions of corrections are outside v1 scope. Raw field text and prompt-injection robustness need further boundaries before admitting field data; the current fixtures contain controlled author text.

## 5. Understand node and edge changes

Every visible report remains represented by one observation node, including duplicates and retracted reports. A separate hypothesis node records a proposed, supported or weakened interpretation. Node identity, kind, concept and asset cannot silently change across prefix states.

Edges carry identity, endpoints, declared relationship type, active/inactive status, evidence references and counts. The ontology specifies which concept/type combinations are permitted. Retracted support makes the corresponding edge inactive rather than erasing it. A changed edge must cite newly available evidence. Cross-asset edges require a future explicit bridge contract and are rejected in v1.

The three count fields retain different meanings:

```json
{"reportCount": 2, "underlyingEventCount": 1, "provenanceRootCount": 1}
```

That is the duplicate-report branch: two reports, one asserted originating observation and one root. These summarize the cited evidence bundle, not confidence or causation. An inactive edge may cite both an old report and its correction; its count is not a measure of remaining positive support. This v1 contract does not yet implement a general ELINT attribute-bucket or joint-match engine. Active temporal edges require observation endpoints, explicit endpoint references, an asserted shared clock and strictly separated occurrence intervals. A later arrival is not evidence of a later occurrence. Availability and step cutoffs use the ingest clock; unresolved occurrence clocks are not compared numerically with that clock. An active contradiction may point to a retained withdrawn claim while citing the current correction; active support and temporal-order edges may not use withdrawn endpoints.

Full snapshots retain earlier nodes and edges. Missing graph entries are rejected; v1 expresses retirement with status, not deletion. Corrections remain in the evidence history and give a reason to revise the current interpretation.

## 6. Use the reusable Python API

```python
import json
from pathlib import Path
from notella.scenarios import validate_scenario_set, compile_scenario_examples

profile = Path('profiles/network_scenarios')
ontology = json.loads((profile / 'ontology.json').read_text())
scenarios = json.loads((profile / 'scenarios.json').read_text())
receipt = validate_scenario_set(ontology, scenarios)
examples = compile_scenario_examples(ontology, scenarios)
print(receipt['scenarios'], receipt['steps'], receipt['uniquePrefixes'])
print(len(examples))
```

Expected: `7 20 11`, then `20`. `validate_scenario` checks one scenario; `evidence_counts` derives the count summary; `scenario_output_schema` creates the closed v1 state schema for a profile. All are in `notella.scenarios`. There is no new scenario HTTP submission route or live scenario-memory server.

Export is **full-prefix reconstruction**: each input contains only the visible evidence, scope, policy reference and cutoff. It never includes authored prior or future target states. The model would reconstruct and interpret that prefix. Autoregressive rollout from the model's own previous state is a separate, unimplemented evaluation mode.

The ontology instruction supplies the proposed policy through the existing compiler. A future learner must infer supported state and assessment changes; the current rule baseline is a comparator, not the intended proof that an AI understands morphology.

## 7. See what validation rejects

The tests deliberately introduce future references, false match counts, duplicate observation nodes, unsupported temporal order, cross-asset links, active retracted support, disappearing history, and shared prefixes relabelled across splits. These fail structural/integrity checks.

A schema-valid but wrong criticality label can still pass the generic contract. The rule baseline, interpretation review and later model evaluation must check domain meaning separately. Current software tests include this distinction explicitly. A complete target graph does not establish neural reasoning or field correctness.

## 8. Admission and the next training gate

All source fixtures have `trainingAllowed=false`. The tutorial intentionally attempts compilation and verifies refusal. Source permission/admission is not inferred from passing validators. No optimizer job or model evaluation is started.

Before training, review the ontology/policy and prefix targets, preserve corrections and reviewer identity, freeze separately authored evaluation families, and explicitly admit intended training material. Keep every branch and prefix from one original family in one split; new names or timestamps do not establish independence. Exact shared-prefix checking helps detect relabelling but cannot certify source-family independence or detect every semantic duplicate.

Next compare the explicit rule baseline, an unadapted model and an ontology-guided model on reviewed scenarios. Measure supported/false links, assessment revision, escalation/de-escalation, uncertainty, correction handling and evidence/rationale consistency. Retain the prior 0.6B results as static-task evidence, not evidence of this new behavior.


## Compatibility and preserved evidence

New public APIs and records use `notella.scenarios`, `notella.scenario.v1`, `notella.scenario-prefix.v1` and `scenarioId`. The existing `notella.episodes` validator is retained as an internal compatibility backend and remains callable. The scenario API accepts legacy episode-format records without mutating their content or stored identities; newly exported prefixes use scenario terminology and therefore have new input identities.

The scenario profile is a new version with a new ontology identity, policy name and source references. It delegates the unchanged reference policy behavior to the retained legacy profile. The tutorial records both facade/reference and compatibility-backend source hashes. Original `profiles/network_episodes` files and historical experiment receipts are preserved. No old training/evaluation result is relabelled as a new run, and no semantic improvement follows from this naming change.

See [Tutorial 13: Rolling windows and semantic deltas](rolling-windows.md) for the ten-second window advancing every second. This runtime design is separate from the full-prefix training comparison.

---

[Previous: Tutorial 10 — Use a local teacher without admitting its answers](teachers.md) · [Next: Tutorial 12 — Score changing scenario states](scenario-scoring.md)
