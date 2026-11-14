[Tutorial index](index.md) · [Tutorial 0: environment setup](setup.md)

# Tutorial 12: test interpretation of changing scenario states

Warnings must be judged against the evidence available at each moment. Score evolving scenarios without rewarding hindsight or unsupported certainty, and retain the failures that show where the approach needs work.

**Outcome:** distinguish a correct decision label from a valid, reference-consistent semantic state, without treating a plausible explanation as proof of understanding.

The ontology represents the semantic model. A scenario supplies evolving evidence; the model is expected to reconstruct supported nodes, typed relationships and assessment changes. This guide describes the first practical model comparison, not a separate non-LLM AI implementation or a broader formal research program.

## Run a no-model check

From C:\workspace\Notella:

```powershell
python -m examples.scenario_scoring_tutorial
```

Expected: fixtureOnly=true, modelLoaded=false, referenceStateMatches=true, correctLabelWithFutureEvidenceRejected=true, semanticAccuracyMeasured=false. The example uses an authored target, then replaces its assessment support with future evidence. The latter retains the expected criticality label but fails the evidence contract. This tests scoring plumbing, not model performance.

## The reusable Python API

```python
from notella.scenario_scoring import score_scenario_output
result = score_scenario_output(ontology, scenario, as_of_ms, exact_generated_text)
```

The scenario must contain an authored target at that cutoff. Preserve the exact generated text separately; this API never repairs it. Pass token_limit_reached=True when an incomplete generation exhausted its budget. JSON with duplicate keys is rejected.

| Check | What it establishes |
|---|---|
| jsonValid / schemaValid | Parseability and the declared output shape |
| contractValid | Explicit evidence visibility, count, scope, graph and temporal checks for this prefix; change references must include newly available evidence |
| criticalityMatch / assessmentStatusMatch | Agreement with the authored policy reference on two discrete fields |
| assessmentEvidenceMatch | Exact reference-set agreement for assessment citations |
| nodesMatch / edgesMatch | Reference-record agreement on concepts, scope, states, relationships, citations and counts, ignoring arbitrary node/edge names |
| contractAndDecisionMatch | Contract-valid matching criticality/status without a known token-limit truncation; not a claim of complete semantic correctness |
| fullStateMatch | All above reference-state components match; prose meaning is not automatically judged |

Extra/missing edge-record counts expose structural differences. These are exact reference conventions, not proof that every different representation is semantically wrong. A separate whole-scenario contract check tests consistent retained identities across generated prefix outputs. Full-prefix reconstruction does not measure rollout from the model's own previous state.

## Current practical comparison

The frozen [scenario-model-v1 protocol](../experiments/scenario-model-v1/PROTOCOL.md), continued by the [memory-bounded retry](../experiments/scenario-model-v3/PROTOCOL.md), compares the explicit proposed rule reference, the local unadapted 4B model, and a fresh scenario-trained adapter on that same base. New development families exercise a scoped benign explanation alongside independent compromise evidence, and correction of reposted compromise evidence amid unrelated-asset observations.

The rule reference defines these initial policy targets, so its agreement is a consistency baseline, not independently measured detector accuracy. Development scenarios have different authored trajectories but the same agent author and proposed policy; independent field accuracy is not claimed. Per-prefix model outputs, graph failures, decisions and actual assessment revisions must be inspected rather than reduced to a format score.

Questions to review after generation include whether a new observation really supports escalation, whether benign evidence improperly erased separate compromise, whether a correction withdrew every duplicate, and whether an unrelated asset acquired a false link. Keep exact explanations for agent/domain review and record review identity truthfully.

This stage establishes whether the working implementation follows the semantic model as its evidence changes. Broader proof of representational advantage, independent studies, phone measurements and alternative architectures are outside this milestone unless requested.

---

[Previous: Tutorial 11 — Represent an evolving scenario](scenarios.md) · [Next: Tutorial 13 — Preserve rolling windows and semantic deltas](rolling-windows.md)
