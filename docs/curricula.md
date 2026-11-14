# Tutorial 3: design a useful curriculum

A curriculum serves people only if it teaches distinctions that matter to their decisions. For the LayerTime use case, that means recognizing developing danger while keeping uncertainty visible. Define the meaning and the evaluation before multiplying examples.

**Outcome:** understand what to supply, how to admit it and how to judge whether it teaches the desired distinctions.

## 1. Define the semantic model before adding examples

The ontology represents the semantic model. The trainer first defines the system's concepts, attributes, relationships, evidence requirements and assessment policy, then specifies how these are represented as an ontology. Examples teach the AI to interpret that model and, in the planned scenario workflow, its change over time. Teacher-generated scenarios must follow the specification rather than silently redefine it.

Use [the node-edge and morphology method](semantic-ontology-morphology.md) to specify supported relationship changes, and [the Colibri authoring workflow](scenario-authoring.md) to plan new scenario branches. The [scenario API](scenarios.md) now validates selected prefix-visibility and graph/evidence transitions when explicitly called. The generic compiler does not automatically invoke it; domain meaning and criticality still require separate review.

Write a concrete statement: “When two observations have different network-radio identities, the model must not treat them as one same-network sequence.” This is testable. “Understand wireless security” is too broad for a single teaching objective.

Define the concepts involved and their relationships. Give measurements units, distinguish measured values from policy parameters, and record the scope of identity claims. A radio address, a detected signal and a physical actor are different concepts.

## 2. Use explicit example records

```json
{
  "id": "different-network-001",
  "family": "different-network-original-scenario",
  "split": "train",
  "concepts": ["observation", "interpretation"],
  "source": {
    "id": "project-authored-v1",
    "kind": "synthetic",
    "reference": "Reviewed scenario card 001",
    "permission": "Project-authored; development training permitted",
    "labelAuthor": "Named reviewer or author",
    "trainingAllowed": true
  },
  "input": "Two observations have distinct network-radio identifiers.",
  "target": {"finding": "The same-network link is not established."}
}
```

This record must be paired with an ontology that defines observation and interpretation and a compatible outputSchema. It is a field example, not a standalone runnable curriculum. The temperature tutorial supplies a complete runnable set.

`source.kind` distinguishes synthetic, document and field material. Permission text records the actual basis for use; it is not a substitute for obtaining permission. Set trainingAllowed only after admission. Do not mark public availability as an automatic right to redistribute or train.

## 3. Build meaningful contrasts

For every intended positive interpretation, include cases where one decisive condition changes:

| Positive condition | Contrast | Desired lesson |
|---|---|---|
| Verified shared identity | Different identity | Similar appearance is not identity |
| A precedes B | B precedes A | Order matters |
| Known aligned times | Missing or overlapping times | Uncertainty can prevent linkage |
| Independent corroboration | Reposts of one report | Repetition is not independence |
| Verified drone presence | Generic RF | A signal is not a platform identity |
| Credible deliberate disruption | Unexplained outage | Symptoms do not establish intent |
| No supported benign explanation | Verified maintenance/aid operation | Counterevidence changes the finding |

The target should explain why the contrast matters. A generic caution paragraph repeated for every case can teach the model to ignore meaningful differences. The first new warning evaluation exposed exactly that failure in the critical trigger case.

## 4. Split original families, not rows

All variants of one original scenario belong in one split. Changing an address, location label or timestamp does not create an independent incident. Assign families before generating variants. The compiler blocks explicit family overlap and exact repeated input across splits, but it cannot discover all paraphrase or upstream-source leakage.

Use training to update weights. Use validation to select settings. Keep the frozen test/acceptance set out of optimization and tuning. If you inspect a held-out result and design new examples to repair it, treat later measurements as affected by that development history; preserve an untouched independent evaluation for stronger claims.

Supply excludedPromptHashes when protecting known evaluation prompts. Hashes protect exact canonical inputs or complete system/user lists. They do not detect paraphrases, aliases or related source recordings.

## 5. Review labels before training

Check each target against its observations and source. Verify measurements, units, chronology, entity roles, source independence and limitations. For a policy-driven judgment, make the policy visible and name its status. A proposed critical-warning threshold is not an empirical estimate of attack probability.

Record who authored and reviewed labels. Current source records carry a labelAuthor string; independent reviewer signatures and a formal approval workflow are not implemented in 0.1. Do not describe an AI-authored label as independently expert-validated.

## 6. Design evaluation around meaning

Schema validity asks whether the answer can be consumed. Exact target matching asks whether it equals the reference text. Neither fully measures justified meaning. A different correct paraphrase can fail exact matching; a fluent schema-valid answer can miss the decisive relationship.

Write criteria before reviewing outputs: correct identity comparison, correct temporal relation, correct posture under the supplied policy, acknowledgement of counterevidence, no fabricated actor/cause/outcome. Bind review decisions to exact generated output hashes and record reviewer scope. Field qualification needs representative, independently sourced evidence beyond these synthetic teaching cases.

## 7. Version changes

Change ontology.version when the meaning or intended contract changes. The content hash changes automatically even if a version label is accidentally reused. Keep a human change note explaining why the definition or label changed. A new hash supplies traceability, not proof that the new interpretation is better.
