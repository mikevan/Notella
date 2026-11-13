# Semantic Ontology Morphology: the training method

**The ontology represents the semantic model. Our intended AI captures changes in that model over time (morphology) and interprets them. The trainer's first job is to define the semantic model and how it should be represented as an ontology.**

This is Notella's intended direction: adapt an existing language model to interpret a system through an explicit semantic model and its evolution. We use existing model capabilities and teach the domain's concepts, evidence relationships and assessment discipline. We do not assume that naming concepts or presenting a graph makes the model internally reason through that exact structure.

## 1. The trainer defines meaning before generating examples

Begin with the system we need the AI to understand. Define:

1. **Entities and scope:** devices, networks, accounts, sensors, observations, assets and scenarios. Specify what establishes identity and which observations can legitimately be combined.
2. **Concepts:** what each observation can mean, its required evidence, and what it does not establish. An outage, deliberate disruption and an attributed attack are different concepts.
3. **Attributes:** units, permitted ranges, physics-derived values, measurement uncertainty and provenance. Identify which values are observations, calculations, caller assertions or policy settings.
4. **Relationships:** their meanings, direction, temporal conditions and evidential requirements. Distinguish observed association, temporal order, support, contradiction and a causal hypothesis.
5. **Morphology:** what evidence permits a node or relationship to emerge, gain support, weaken, expire or be retracted. Define how contradictions and corrections change the interpretation.
6. **Assessment policy:** how the developing model informs criticality given asset importance, potential consequences, evidence quality and unresolved alternatives. Criticality, confidence, and probability of attack are different quantities.
7. **Representation:** the ontology definitions and the concrete scenario/state representation, including identities, timestamps, evidence references and version history.
8. **Teaching and evaluation:** scenarios and contrasts that demonstrate correct interpretation and revision, including cases where escalation is unwarranted.

The ontology is the explicit representation of this semantic model, not a bag of keywords attached after examples have been written. Its structure must follow the system's meaning rather than the convenience of a model prompt.

## 2. Distinguish model definition from an evolving scenario

The ontology defines concepts and allowed relationships. Each scenario supplies scoped instances, observations, relationship assertions and hypotheses under that ontology.

An scenario evolves as new evidence arrives. For example, the support for a coordinated-activity hypothesis may increase after corroboration and decrease after a source correction. That does not require redefining the meaning of corroboration each time an event arrives. Changes to concept definitions or policy require a reviewed ontology version; changes to the scenario produce a new scenario-state version.

Thus morphology includes changing support and relationship structure, even when the vocabulary remains stable. It is not simply a larger count of suspicious events.

## 3. Nodes and edges describe the intended reasoning behavior

The node-edge concept is an explanation of how we expect the AI to reason; it does not require a particular visual display.

**A node represents a meaningful, scoped element of the semantic model.** Depending on the domain this can be an attribute range, an observation, a concept instance, an asset or a hypothesis. Examples include a measured radio attribute within a specified range, scanning of host H7, or a hypothesis of coordinated activity in scenario E12. Identical concept names in unrelated assets do not automatically constitute one incident.

**An edge represents a specified relationship between nodes.** It must carry its type, direction where relevant, scope, timing conditions, supporting evidence and uncertainty. Useful relation types include:

| Relationship | What it supports |
|---|---|
| observed_with | Joint occurrence under a defined matching rule; no causal claim |
| precedes | A supported temporal order, accounting for timestamp uncertainty |
| same_asset_as / refers_to | An identity or scope relationship with a stated basis |
| supports | Evidence contributes to a concept or hypothesis |
| contradicts | Evidence conflicts with a claim or interpretation |
| explained_by | A proposed or verified alternative explanation, labelled accordingly |

A relation name is not sufficient evidence that the relation holds. Each claim must be traceable to the observations and matching/inference rule that supports it.

### The ELINT counting analogy

In the original attribute-selection pattern:

- A query selects observations based on measured or physics-derived attributes.
- A node's match count is the number of selected units satisfying its attribute/range definition.
- An edge's joint-match count is the number of those same units satisfying both definitions.
- A display can use one pixel of edge width per match. That pixel rule is a display convention, not the reasoning algorithm.

For matching sets A and B in a selected population Q:

```text
nodeMatches(A) = count(distinct matching units in Q that satisfy A)
edgeMatches(A,B) = count(distinct matching units in Q that satisfy both A and B)
```

Define the unit explicitly: one radar, one observation, one independently asserted provenance root, or one event pair in an scenario. These are different measurements. A temporal edge between different events needs a documented join over eligible event pairs, asset scope, ordering and window conditions; it is not a same-row attribute count.

Preserve raw matches, deduplicated matches and provenance-root counts separately. Report duplication must not silently amplify independent support. Even distinct asserted roots do not establish statistical independence. If the selection query already requires A and B, a dense A-B edge is partly imposed by that query and is not independent evidence of association.

### Expected interpretation of node/edge changes

The AI should use increased support, new relationships, contradictions and changes in scope to revise its interpretation. Raw frequency alone must not become importance, confidence, causation or criticality. One well-supported severe event can matter more than many duplicate weak reports.

Record counts, provenance, recency, match conditions and uncertainty as distinct attributes. Any learned weighting or calibration must be specified and evaluated; there is no established universal count-to-confidence formula in the current implementation.

Counting words in a query is not this process. The question selects the assessment task; the evidence determines which semantic elements are supported. Our current corpus tags every training example with all nine concepts. Those broad tags cannot reveal useful differences in corpus co-occurrence. Future scenario curricula need selective, evidence-grounded annotations; do not invent informative edges from uniform tags.

## 4. The AI learns to interpret morphology

The intended inference cycle is:

```text
new observations
  -> normalize measurements, identities, time and provenance
  -> update the scenario's semantic state under the ontology
  -> assess supported relationships and competing hypotheses
  -> revise criticality and explain what changed, with evidence references
```

The application maintains the supplied semantic state and history. The language model interprets it and can propose changes or assessments; application-level checks must validate references, allowed transitions, units, identity scope and policy consistency. A fluent explanation must not make an unsupported relationship authoritative.

During training, LoRA adapts model weights using reviewed scenario examples. During ordinary inference, new evidence changes the scenario context/state, not the model's weights. The model's internal neural representation need not be a literal graph for us to teach and test this behavior.

## 5. Teach scenarios, not only final labels

A teaching scenario should include a sequence of prefixes and a reviewed interpretation at each step. At time t, the target may use only evidence available by t. Future facts must not leak into an earlier prompt or target.

| New evidence in a synthetic scenario | Desired reasoning behavior |
|---|---|
| An observed scan concerns host H7 | Represent the observation and scope; do not assert compromise from the scan alone. |
| Repeated authentication failures concern H7 and account A9 | Consider a relationship to the earlier activity, while retaining benign alternatives and source limitations. |
| A supplied, reviewed observation establishes unauthorized privileged access | Reassess the compromise hypothesis and criticality under the stated asset/consequence policy. |
| Later activity concerns another system | Link it only if supported identity, provenance and time conditions establish relevance. |
| A source corrects an earlier claim | Preserve the original claim and correction, revise affected support and explain the assessment change. |

Do not assign universal criticality values to this illustrative sequence. The trainer must define the policy, asset context and evidential requirements. A maintenance branch should share the early prefix and then introduce supported benign facts; it must not erase independently established compromise without a corresponding correction or explanation.

The curriculum must include single-factor contrasts, delayed/out-of-order evidence, missing clocks, duplicated reports, unrelated assets, contrary evidence, benign explanations and legitimate non-escalation. The target should explain why the semantic model changed, not merely repeat a warning paragraph.

## 6. Proposed scenario teaching contract

This describes the intended full scenario workflow. The first assessment-profile Python contract and validators are now implemented in `notella.scenarios`; [Tutorial 11](scenarios.md) covers their supported subset. They do not replace the historical three-field profile or supply a live scenario-memory server.

Each planned teaching item should identify the ontology version, scenario and family, evidence available so far, prior semantic state where appropriate, incoming observations, reviewed state changes, competing interpretations, criticality policy, expected assessment and rationale. Node/edge changes must refer to supported evidence IDs. Explicitly distinguish measured facts, inferred relations, hypotheses and reviewer assertions.

The current scenario validators check explicit evidence visibility/references, provenance-count consistency, retained graph identities, retractions, declared edge types, same-asset boundaries and supported temporal order. They do not establish source authenticity or correct domain criticality. Cross-asset bridge rules, expiry-only updates, calibrated confidence and model-generated state rollout remain additional work. The generic compiler still requires an explicit call to the scenario validator; it does not automatically apply profile checks to every JSON input.

All prefixes, branches and variants of one original scenario must remain in one split. Use separate scenario families and independent review when claiming generalization. Merely changing addresses or timestamps does not create a new independent family.

## 7. How Colibri fits

Colibri hosts a local model that proposes new scenario material from the trainer's semantic specification. It can help expand scenario diversity, propose alternative explanations and generate controlled branches that test an intended distinction. It does not determine what the semantic model means or certify correct criticality.

The trainer supplies concepts, relationships, transition rules, measurement constraints and assessment policy first. Candidate scenarios then undergo structural checks, domain review, provenance checks and explicit admission before entering a training curriculum. Keep rejected candidates and exact model/configuration receipts.

See [the scenario-authoring workflow](scenario-authoring.md) for a proposed scenario card, prompt example, review checklist and evaluation gates. The existing [teacher tutorial](teachers.md) provides runnable candidate generation and hash-bound reviews.

## 8. Implemented evidence and outstanding work

Implemented: ontology/curriculum APIs, local LoRA training, typed single-observation contracts, interval arithmetic, source-lineage summaries, local teacher candidates, separate hash-bound reviews and the [scenario contract/rule-baseline tutorial](scenarios.md). The first provisional set contains seven shared-family branches, 20 reference states and 11 distinct visible prefixes; training admission is false. Two 0.6B students have been trained on the current three-field classification task.

Not yet demonstrated by a trained model: interpreting a multi-step attack scenario, maintaining/revising semantic state across evidence updates, learning supported morphology transitions, or selecting criticality reliably across independently reviewed scenarios. There is no proof that the current models internally represent the ontology graph.

The [small-student diagnostic](../experiments/student-v1-teacher-augmentation/RESULTS.md) favored direct ontology-guided training over six extra teacher labels. It supports retaining a direct baseline and testing the value of teacher-generated scenario diversity, rather than assuming a larger teacher improves training. Phone performance and field qualification remain unestablished.
