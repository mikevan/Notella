[Tutorial index](index.md) · [Tutorial 0: environment setup](setup.md)

# Meaning is more than a query

## The PRS purpose

PRS aims to help people recognize escalating danger in time to make informed decisions, including people displaced by conflict or facing unreliable communications. Local observation, preserved evidence, and understandable findings support that purpose. The relationship-and-time model is the foundation; the new trained-AI and phone implementation is a distinct validation task.

## The argument

Semantic technology should be judged by the meaning a system can preserve and use. Mapping a business term to a metric, SQL expression or storage structure is useful. It does not, by itself, establish that an AI can interpret changing evidence, distinguish current support from historical presence, or revise a protective warning when its justification changes.

For our use case, the decisive question is: **What changed in the situation, what does that change mean, and does it warrant a different action now?**

An ontology represents the semantic model: the domain's concepts, instances, typed relationships and constraints. Semantic Ontology Morphology is our working term for changes in the evidence-backed instantiation of that model over time. The intended AI capability is to interpret those changes. The software maintains evidence identity, provenance, time and retained history; the model learns how those facts bear on hypotheses and decisions.

The PRS model treats semantic relationships as the basis for context-specific ontologies, measures their evolution over time and aims to make that interpretation actionable at the edge. The new learning, distillation and phone implementation must be validated separately; current Notella trials do not demonstrate reliable real-time warnings.

## A defensible market contrast

The statement that all vendors equate semantics with SQL and ontologies with schemas is not supported by the sources inspected. The critique should target a reduction of scope, not misrepresent competitors.

| Source-backed example | What its documentation emphasizes | What we can fairly conclude |
| --- | --- | --- |
| Snowflake Semantic Views | Database-managed business definitions, entity relationships and metrics, used by analytics and AI-assisted queries. | A clear example of an analytics-oriented semantic abstraction. Its documentation does not justify claiming the vendor considers all semantics equivalent to SQL. [S1] |
| dbt semantic models | A graph of model metadata connected through entities, with definitions supporting metric calculation and querying. | Another query/metrics-centered design. It is more than column renaming, and it serves a legitimate problem. [S2] |
| Palantir Ontology | Connected objects and relationships combined with decision logic, actions, AI and operational systems. | A counterexample to the universal claim. Operational ontologies already exist; our argument must acknowledge that overlap. [S3] |
| W3C OWL 2 | Domain vocabularies with formal meaning, including classes, properties and instances. | The established concept of ontology is broader than a storage schema. We are applying and extending a modeling approach, not inventing ontology itself. [S4] |

These are selected examples, checked November 13, 2026, not an exhaustive capability audit or a claim about each vendor's entire platform.

## The distinction we propose

A query-oriented semantic layer helps preserve definitions while retrieving or aggregating data. An operational semantic model can also represent the situation whose meaning must be interpreted. Our proposal makes **temporal evidence revision a training target** and **small-device warning behavior an acceptance requirement**.

| Design question | Query-oriented example | Proposed Semantic Ontology Morphology requirement |
| --- | --- | --- |
| Meaning | Which definition and aggregation should a query use? | What does this observation imply within the defined domain and current context? |
| Ontology | Which entities and relationships organize the data? | Which concept instances, assertions and relationships currently support or contradict a hypothesis? |
| Time | Which period or time grouping should be queried? | What changed in support, validity, ordering or scope between states? |
| Provenance | Where did the record come from? | Do reports share an originating event, and does a correction invalidate all dependent support? |
| Learning | Use semantic context to improve access to data. | Teach an AI to interpret evidence-backed state changes and revise its assessment. |
| Output | A governed answer, metric or query result. | A compact, evidence-supported assessment and policy-appropriate warning. |
| Acceptance | Correctness and consistency of the requested result. | Missed warnings, incorrect clearances, false alarms, evidence support and measured end-to-end device behavior. |

This compares requirements and example design centers. It is not a statement that SQL systems cannot implement time, provenance, inference or alerts. Those capabilities can be implemented with SQL and other technologies. Their implementation still has to be demonstrated; the words “semantic layer” alone do not establish them.

## Why temporal meaning changes the problem

Consider an illustrative camp scenario under an already threatening context:

1. A reviewed Wi-Fi disruption indicator appears. Preserve the observation and context.
2. Another report repeats the same originating event. Record volume grows; independent corroboration does not.
3. A credible, independent drone-signature observation is associated with the same place and time. A reviewed domain policy may warrant focused precautionary assessment and a protective warning.
4. A trusted correction withdraws the Wi-Fi indicator. Preserve the history and remove its current support, including the repost. Reassess the remaining drone evidence and background threat; do not automatically declare all clear.

The retained record count increases at step four while support for the combined pattern decreases. A semantic model must represent that difference, and an interpreting AI must respect it. Node size or co-occurrence counts alone are not confidence, independent evidence or proof of causation.

The example does not establish an impending assault. Protective action, including evacuation guidance, needs validated local policy and relevant context. The model's job is not to turn an unverified correlation into certainty.

## The PRS model and its AI extension

**Stable ontology → current semantic state → meaningful state changes → learned interpretation → validated warning.**

- **Ontology:** domain concepts, relationship types, scope and constraints, versioned separately from live observations.
- **State:** concept instances and assertions grounded in available evidence, with active/retracted status, event and receipt times, provenance and uncertainty.
- **Morphology:** added, revised, withdrawn and newly connected support, interpreted with retained incident history. The graph can change without changing its vocabulary or the model's weights.
- **AI interpretation:** identify issues, revise criticality, cite support and express uncertainty under the domain policy.
- **Warning path:** validate the proposal, surface a compact protective message promptly, and keep optional explanation generation separate.

A node-edge graph here is the system's semantic representation. We do not claim it is a literal diagram of the language model's neurons. Likewise, the architecture does not require an LLM to invent identities, recompute every count or serialize an entire graph before an existing validated warning can be shown.

### Training center

Establish a large teacher that reliably performs the semantic task. Review its decisions and supporting evidence. Distill demonstrated capabilities into smaller students, and measure what survives the transfer. Larger models are not automatically correct; earlier Colibri drafting experiments did not establish a reliable specialized teacher.

### Phone

Deliver a finished local inference model. The application updates a ten-second rolling window every second and maintains the semantic state. It sends meaningful deltas and relevant context for interpretation. When something warrants focus, retain the incident and prioritize related changes while broad monitoring continues. A one-second collection cadence is not a claim of one-second model inference.

Observations must come from authorized, available device sensors or supported receivers. This proposal does not establish that every phone can detect a Wi-Fi attack or a drone signature. Source verification and detection capability are distinct from interpretation by an LLM.

Refugees do not train models in camps. Centrally reviewed failures inform versioned teacher/student releases; field observations update application state rather than silently retraining weights.

## Evidence and promise

We have defined a testable path and implemented reference components for ontology/scenario validation, training, scoring, rolling windows, focused incidents and warning continuity. In the latest controlled 4B rerun, known criticality agreement improved from 11/18 to 13/18 and flagged repetitive narratives fell from 5/18 to 1/18. Full-state agreement regressed from 4/18 to 1/18. On fresh controls the adapter matched 5/6 decisions, versus 6/6 for the base.

Those trials address the new SLM implementation; they do not establish that the underlying relationship-and-time model is wrong. They show some teachable behavior and unresolved failures, rather than reliable semantic reasoning, successful distillation or operational assault detection. Root cause is not isolated. Phone latency, sustained operation and notification delivery remain unqualified.

Our proposed contribution is the combination to test: ontology-guided semantic training, explicit time-dependent evidence state, learned interpretation of its morphology, reviewed teacher-to-student transfer, and compact local warning behavior. We have not established a world-first claim, exclusivity, or superiority over every operational-ontology platform.

## Positioning statement

**Semantics should govern how an AI interprets a changing situation. An ontology should express the model of that situation. Our proposal trains AI to interpret the model's evolution, then transfers demonstrated capability into a small, local warning system.**

SQL, schemas and governed metrics remain useful infrastructure. The additional claim must be earned in behavior: the system must know which evidence still matters, revise its judgment correctly, and deliver a timely, supportable warning.

## Sources

- [S1 — Snowflake: Overview of semantic views](https://docs.snowflake.com/en/user-guide/views-semantic/overview)
- [S2 — dbt: Semantic models](https://docs.getdbt.com/docs/build/semantic-models)
- [S3 — Palantir: The Ontology system](https://www.palantir.com/docs/foundry/architecture-center/ontology-system)
- [S4 — W3C: OWL 2 document overview](https://www.w3.org/TR/owl2-overview/)

Project evidence: `experiments/scenario-model-v5/RESULTS.md`, `docs/morphology-failure-report.md`, `docs/teacher-student-roadmap.md` and `docs/warning-continuity.md`. Research, example illustrations, implemented code and validated product behavior are distinct claims.

[Tutorial index](index.md) · [Start with environment setup](setup.md)
