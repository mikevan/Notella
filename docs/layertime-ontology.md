[Tutorial index](index.md) · [Tutorial 0: environment setup](setup.md)

# Walkthrough: the LayerTime ontology

Interpreting a developing threat starts with stating what observations can and cannot support. This walkthrough makes those meanings inspectable in the LayerTime training profile before any model is trusted with them.

**Outcome:** understand the ontology used by the current 4B and 0.6B development experiments, inspect its real JSON artifact, and follow a worked temporal example without loading a model.

The artifact is [LayerTime typed-observation decision training, version 0.6.0-development](../experiments/warning-v6-typed-training/ontology.json). Its content-addressed ID is `de8b8fa925137177906f1422d92e9024f7253a4ff086f4ee10ef731ab4fa5092`.

This is a narrow development ontology for interpreting a disruption followed by possible drone activity under an ongoing threat. It is not a complete threat ontology, an RF classifier or a validated causal model.

The ontology represents the semantic model for this narrow task. The trainer chose the concepts, relationships and policy before creating examples. The planned extension teaches interpretation of changes in an scenario's semantic model over time; see [Semantic Ontology Morphology](semantic-ontology-morphology.md). The current three-field task does not demonstrate that full behavior.

## 1. Read the nine concepts

| Concept | Distinction being taught |
|---|---|
| Observation | An event has a source, location, time and uncertainty. |
| Disruption identity | A Wi-Fi outage alone does not establish deliberate denial of service. |
| Signal identity | Generic RF energy does not establish drone presence. |
| Source independence | Repeated reports can originate from one observation. Distinct asserted roots do not prove statistical independence. |
| Temporal precedence | One event precedes another only when their uncertainty intervals support that order. |
| Spatial overlap | Whether the observations concern overlapping locations within the supplied uncertainty. |
| Counterevidence | Benign explanations, reversed timing and missing corroboration constrain an interpretation. |
| Warning posture | Precautionary urgency under a stated policy; not a probability of attack. |
| Causal claim | Requires evidence beyond temporal association. Perpetrator attribution is a separate claim. |

The current spatial implementation is narrower than the concept definition: the typed profile compares declared `areaRef` values. It does not calculate geographic overlap from coordinates or location-error distributions.

## 2. Read the four explicit relationships

The JSON stores subject/predicate/object triples:

- `temporal_precedence qualifies observation`
- `source_independence qualifies observation`
- `counterevidence constrains warning_posture`
- `warning_posture distinctFrom causal_claim`

These are domain assertions that guide teaching and interpretation. Notella checks that referenced concepts exist; it does not prove these statements with an OWL reasoner or automatically establish ontology consistency.

## 3. Separate the ontology, policy and output contract

The JSON artifact packages all three together:

| Part | Its role |
|---|---|
| `concepts` and `relations` | Define the vocabulary and meaningful relationships. |
| `instruction` | Specify the proposed development decision policy. |
| `outputSchema` | Restrict the model to three fields and ten permitted combinations. |

Changing a precautionary policy is different from discovering a causal fact. A policy can require urgent action under uncertainty without claiming that an attack is certain.

The proposed critical combined trigger requires **all** of these supplied conditions: ongoing threat, reviewed deliberate disruption, corroborated drone identity, distinct reviewed origins for the drone reports, equal area references, drone activity afterward, and timing inside the configured linking window. Verified benign operations negate this particular combined trigger.

The model does not discover whether these inputs are authentic. Event classifications, registry review and standing-threat context are caller assertions. Their real-world verification requires other evidence and components.

## 4. Follow a worked example

Suppose a synthetic observation supplies:

- Reviewed deliberate disruption at 100,000 ms, with uncertainty of plus/minus 1,000 ms.
- Corroborated drone presence at 120,000 ms, with uncertainty of plus/minus 2,000 ms.
- The same area, ongoing threat, and two drone reports with different reviewed provenance roots.
- A shared time basis and a linking window of 120,000 ms.

The possible delay is **17,000 to 23,000 ms**. The drone observation is later and entirely inside the configured window. From `C:\workspace\Notella`, run:

```powershell
python -c "from notella.correlation import temporal_link; import json; print(json.dumps(temporal_link(100000,120000,1000,2000,120000),indent=2))"
```

Expect `order="after"`, `delayIntervalMs=[17000,23000]`, `withinWindow=true` and `causationEstablished=false`. This function performs interval arithmetic. The profile separately requires a supplied shared-clock assertion; neither the function nor the profile independently verifies clock alignment.

Given all the other stated conditions, the **authored policy reference**, not a model result from this command, is:

```json
{"posture":"critical","combinedTrigger":"met","evidenceClass":"corroborated_drone"}
```

This means the proposed precautionary trigger is met. It does not establish causation, a perpetrator or an attack probability.

## 5. Change one meaningful fact

| Change to the example | Policy reference: posture / trigger / evidence |
|---|---|
| Outage cause unresolved | high / unconfirmed / cause_unresolved |
| RF signature unidentified | high / unconfirmed / unidentified_signal |
| Drone reports relay one origin | high / unconfirmed / dependent_reports |
| Clock comparability unavailable | high / unconfirmed / unknown_time |
| Time uncertainty prevents ordering | high / unconfirmed / uncertain_order |
| Drone observation precedes disruption | contextual / not_met / reversed_sequence |
| Drone observation entirely beyond the window | contextual / not_met / outside_window |
| Different declared areas | contextual / not_met / different_location |
| Verified maintenance or humanitarian drone operation | contextual / not_met / benign_explanation |

Together with the critical example, these are the artifact's ten allowed output combinations. The table describes controlled single-factor contrasts, not a complete priority system for every possible combination of conflicting evidence. Unsupported input conditions, such as unknown source lineage or timing straddling the window boundary, require profile-level review deferral rather than an invented model answer.

`contextual` and `not_met` do not mean safe. They mean this particular combined trigger is not supported; a separate hazard or standing threat can remain.

## 6. See how this becomes semantic LoRA training

Notella's compiler places the policy instruction, concept definitions, relationships and output schema into the model-visible system message. Admitted examples pair a supplied observation with a reviewed target. The completion-only LoRA loss trains the target answer, while prompt tokens are masked out of that loss.

The desired semantic behavior is that changing a relevant relationship changes the interpretation for the correct reason. Naming a concept does not prove the model learned it. Evidence guards reject selected inconsistencies after generation; rejection is not a repaired or correct model answer.

For actual input projection and rejection behavior, run the no-model example in [Tutorial 9](input-output-contracts.md). For teacher-generated contrasts and review boundaries, use [Tutorial 10](teachers.md). The [0.6B student results](../experiments/student-v1-teacher-augmentation/RESULTS.md) show direct and teacher-augmented training on this same ontology, including the negative augmentation result.

## 7. Inspect the artifact yourself

```powershell
python -c "import json; from pathlib import Path; o=json.loads(Path('experiments/warning-v6-typed-training/ontology.json').read_text()); print(o['name'],o['version']); print(len(o['concepts']),len(o['relations']),len(o['outputSchema']['enum']))"
```

Expect the name and version above, followed by `9 4 10`. This verifies the artifact's declared structure, not its scientific validity. The current evaluations use related synthetic policy cases; they do not establish field accuracy, sensor classification capability or causation.

[Tutorial index](index.md) · [Start with environment setup](setup.md)
