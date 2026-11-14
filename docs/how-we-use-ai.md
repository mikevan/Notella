[Tutorial index](index.md) · [Tutorial 0: environment setup](setup.md)

# How we use and train AI

Notella develops a reusable way to teach models the meaning of evidence and how that meaning changes over time. Vixen is the first field-analysis application: its intended role is to help people understand a developing situation using locally preserved observations.

**Begin with [Tutorial 0: environment setup](setup.md) before following the [tutorial sequence](index.md).** Read the [iteration history](ai-iteration-history.md) for improvements, regressions, and the evidence behind our decisions.

## Where AI belongs

The intended field workflow keeps capture and immediate triage procedural. Hunter records observations; Vixen preserves relevant evidence; T-Ultra supplies an independent record for comparison. A rolling ten-second capture window can identify an interesting change and retain the surrounding slices. The model is then asked to interpret relevant evidence, rather than process every update continuously.

The application is responsible for identities, time, duplicates, retained evidence, exact comparisons, and validated warning state. The model's research role is interpreting evidence relationships and their evolution. An attack signature is a hypothesis to evaluate, not permission to invent its expected stages. A missing observation must stay missing.

This is the intended division of work. [Vixen's current implementation status](https://github.com/mikevan/Vixen/blob/field/ecosystem-evidence-parity/docs/ai-development/CURRENT-AI-STATUS.md) records what is integrated and what remains unproven. Notella's reference components do not establish normal phone warning delivery.

## How we teach it

1. **Define the meaning.** Specify concepts, relationships, evidence requirements, time assumptions, and the proposed interpretation policy. The ontology represents that semantic model. See [the method](semantic-ontology-morphology.md).
2. **Author and review examples.** Include partial sequences, benign alternatives, withdrawn support, and contradictory evidence. Preserve source rights, provenance, review decisions, and family boundaries. See [Tutorial 3](curricula.md).
3. **Keep evaluation separate.** Freeze the evaluation role and criteria before looking at predictions. Inspected cases become known development evidence; they must not be renamed independent validation. See [scenario scoring](scenario-scoring.md).
4. **Adapt an existing model.** The current local backend uses LoRA/QLoRA rather than training a language model from scratch. Explicitly configured local weights and a compatible CUDA environment are required. A plan does not start a job; starting a job is a deliberate API action. See [Tutorial 4](training.md).
5. **Measure actual work.** Retain applied and skipped updates, source/data hashes, package settings, saved-weight checks, and exact generated answers. Loss and finite weights establish numerical properties, not understanding.
6. **Compare meaning, not just format.** Compare base and adapted models under matched settings. Score decisions, evidence, timing, and complete state separately. Retain incomplete or wrong answers unchanged and record reviewer provenance. See [Tutorial 5](semantic-reviews.md) and [Tutorial 7](decision-scoring.md).
7. **Qualify integration separately.** A successful synthetic task does not establish RF detection, phone performance, a useful warning, or field reliability. Device and end-to-end qualification remain distinct gates.

## What teachers and smaller students contribute

An optional locally served teacher can propose candidates. Its answers are not automatically true or admitted to training. The ontology and review policy remain authoritative. The first 0.6B comparison favored direct training over adding six reviewed teacher decisions on the selected controls; it did not establish that teacher augmentation helps. See [Tutorial 10](teachers.md) and [the comparison](../experiments/student-v1-teacher-augmentation/RESULTS.md).

## What has and has not worked

Typed-observation training improved a compact three-field task on ten authored development controls. Full evolving-state experiments still confuse historical evidence with current support and can repeat until their output budget is exhausted. Neither result justifies a field-readiness claim. The [iteration history](ai-iteration-history.md) links both outcomes and their limits.

[Tutorial index](index.md) · [Start with environment setup](setup.md)
