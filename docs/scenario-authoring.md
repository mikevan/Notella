# Colibri scenario authoring for Semantic Ontology Morphology

**Purpose:** use a local model served by Colibri to propose new scenarios that teach an existing semantic model and its change over time. The trainer defines the semantic model and represents it as an ontology before scenario generation begins.

This guide describes the intended scenario workflow. The current runnable teacher API generates and preserves candidate text. A separate [scenario contract and tutorial](scenarios.md) now validate selected graph/evidence transitions and supply provisional rule-authored fixtures. The teacher API does not automatically generate, validate or admit multi-step scenario curricula.

## 1. Write the trainer's scenario specification

Before prompting a model, supply:

| Specification | Required decision by the trainer |
|---|---|
| Semantic model | What system is represented, its entities, identities, concepts and relationships |
| Ontology | Exact version/content identity and domain definitions |
| Morphology objective | Which node/edge changes and interpretation revisions the scenario should teach |
| Measurement rules | Units, ranges, uncertainty, clock assumptions and any externally validated physics formulas |
| Evidence rules | Sources, provenance roots, permitted identity claims and deduplication/matching units |
| Criticality policy | Asset/consequence context, required evidence, allowed assessments and deferral conditions |
| Scenario constraints | Length, available evidence at each step, supported transitions and prohibited contradictions |
| Contrast plan | Which factor changes in each branch and what stays fixed |
| Review criteria | Prospective checks for meaning, plausibility, consistency and evidence traceability |

The model may suggest additions to this specification, but those suggestions require separate review/versioning. They must not silently redefine the ontology in the generated scenario.

## 2. Ask for controlled candidate scenarios

An example authoring prompt, to adapt with the actual ontology and policy:

```text
Draft synthetic candidate training scenarios for human or agent review.
Use only the supplied ontology definitions, measurement rules and policy.
The ontology represents the semantic model; the teaching objective is how
that model changes as evidence arrives and how those changes are interpreted.

Create one original network scenario and three explicitly labelled branches:
1. Additional evidence supports a developing compromise hypothesis.
2. Reports share one source and must not count as independent corroboration.
3. A supported benign explanation changes the interpretation of the early events.

Keep the common prefix identical. Identify the changed factor in each branch.
For every step provide:
- evidence IDs, times, uncertainty, asset/account scope and source roots;
- only the evidence visible at that step;
- proposed node and typed-edge changes, with supporting evidence references;
- hypotheses supported, weakened or contradicted;
- a proposed assessment under the supplied policy and a short rationale;
- unresolved questions and conditions requiring review or deferral.

Do not invent a successful compromise from failed logins or a drone identity
from unidentified RF. Do not turn co-occurrence counts into causal proof.
Do not report a numerical attack probability without a supplied calibrated method.
Mark every scenario and assessment as a synthetic candidate pending review.
```

This is a proposed prompt template, not a command that runs a new scenario pipeline. Keep operational exploit instructions out of these interpretation-focused scenarios; event summaries and evidence transitions are the teaching material.

If the task requires numerical physics, calculate/check the values with the specified formula and units outside the authoring model. A plausible-looking model-generated number is not a validated measurement or physical simulation.

## 3. Preserve the candidate before review

Use the existing [teacher tutorial](teachers.md) to call `LocalTeacher` and `teaching_candidate`. Preserve exact messages, response body, output hash, finish reason, model identity and verified intake/configuration receipts. Keep the ontology and specification hashes with the experiment. A truncated or failed reply must remain a visible failed candidate; use a new directory for an explicit retry.

The current teacher provider is a reusable Python interface for a loopback server. No new `/scenarios` or `/scenarios` HTTP endpoint is implemented by this documentation.

For a first single-step runnable candidate, from `C:\workspace\Notella`, with the verified bounded local teacher server already running:

```powershell
$python = 'C:\workspace\TUltra-Project\LayerTime\tools\ai-training\.venv\Scripts\python.exe'
& $python .\examples\teacher_tutorial.py --model notella-teacher-qwen36 --base-url http://127.0.0.1:8877/v1 --output .\runtime\teacher-scenario-seed-001
```

Expected: a saved request and candidate, `reviewStatus=pending` and `admittedForTraining=false`. This existing example drafts a short source-lineage contrast. It does not implement the multi-step scenario template above. No training starts from this command.

## 4. Review structure and meaning separately

Structural checks should establish identifiers, valid types/units, evidence references, timeline consistency, prefix visibility and branch differences. The current scenario validators implement explicit reference/visibility, provenance-count, typed-edge, retained-history and temporal-order checks; they do not perform full physical/domain validation or prove correct criticality. Call them explicitly before admission. More comprehensive transition policies remain additional work.

Semantic review must ask:

- Do concepts and relationships mean what the ontology defines?
- Does each node/edge change have supporting evidence, with counterevidence preserved?
- Are identities, time windows and provenance roots used consistently?
- Are repeated reports distinguished from independent observations?
- Do the proposed assessment and rationale follow the trainer's policy?
- Does a correction revise affected hypotheses without rewriting history?
- Does each contrast isolate the intended distinction?
- Is uncertainty retained where the available evidence is insufficient?

The existing `record_teacher_review` API binds judgments to an exact candidate output and records reviewer kind and asserted independence. A review pass grants no training permission. Agent review is agent review, not independent domain certification. A teacher evaluating its own draft is not an independent reference answer.

## 5. Admit reviewed teaching material explicitly

After review, author/admit curriculum examples with source permissions, candidate/review references, ontology version and original scenario family. Preserve reviewer corrections separately from the original response; never silently repair a failed response and report it as a teacher success.

For scenario training, all prefixes and branches derived from one original scenario belong in one split. Keep evaluation families and expected answers out of teacher-generation inputs. Deduplicate by underlying source/family and semantic content where possible, not only by exact text or invented family names. Do not promote already inspected acceptance answers into training material.

## 6. Test what the teacher adds

Compare a direct authored baseline with reviewed teacher-generated scenario material on the same student architecture and declared training budget. Include a matched-count authored augmentation control to distinguish teacher value from merely adding examples. Record family counts, replay/sampling, seeds and total generation/review/training cost. Keep synthetic and field evidence separate.

Evaluate interpretation at each scenario prefix: supported links, false links, missed escalation, false escalation, correct de-escalation, retained uncertainty, proper response to source correction and rationale/evidence consistency. Final-label agreement alone does not establish correct morphology interpretation. Use separately reviewed prospective scenario families before claiming generalization.

The existing local experiments establish plumbing and expose limits: the first free-form teacher draft failed review; constrained single-factor tasks produced six correct labels; adding those labels to a 0.6B student reduced observed agreement in a one-seed fixed-budget diagnostic. These do not establish a benefit from teacher-generated scenarios, which have not yet been implemented or evaluated. [Recorded results](../experiments/student-v1-teacher-augmentation/RESULTS.md).

## 7. First scenario milestone

The first versioned representation, validators, explicit rule comparator and provisional scenario fixtures are available in [Tutorial 11](scenarios.md). They have not received independent domain review or training admission. The next milestone is to review the semantic model/policy and targets, author separate evaluation families, then compare the rule baseline, an unadapted model and a trained model, with reviewed Colibri branches where useful. Maintain a trace from each assessment back to observations and ontology rules. Keep phone conversion and device/field qualification as separate later gates.
