# Retraction/repetition investigation: root cause not established

## First recorded appearances in this scenario series

- Before LoRA, v3's matched base already makes wrong decisions and incomplete responses. The later fixed narrative-repetition heuristic flags none of its ten outputs. These are distinct observations: hitting a token bound is not proof of repetition.
- After the first completed fresh 4B scenario training (v3), S-Q71-step-1 labels standalone reviewed compromise contextual, despite a contract-valid output. S-Q71-step-5 retains critical after explicit withdrawal. The first flagged trained-model loop is S-Q92-step-4 (duplicate-report prefix), followed by step-5.
- v4's revised curriculum improves some labels, but the first flagged loop moves earlier to S-Q71-step-5; five of eighteen narratives are flagged. A completed fresh response, V-834-step-3, cites a correction while claiming current compromise. Thus wrong retraction meaning can occur without looping.
- Current v5's S-Q71-step-5 again begins with an incorrect critical label, acknowledges retired r17, misuses credential/benign reports as access/retired support, and repeats until the unchanged cap. This raw incomplete output is preserved, not accepted as a valid decision.

This is the earliest documented occurrence in the inspected scenario comparison artifacts, not a claim about every earlier static-task model or teacher experiment.

## Model conditions

Same local Qwen3-4B-Instruct-2507, NF4 QLoRA, fresh rank-16/alpha-32 q_proj/v_proj adapter, learning rate 0.0001, seed 42, batch/accumulation 1, eighty applied updates, zero skipped updates, finite weights. Full visible-prefix history is input; the model must reconstruct current/retired evidence, apply scope and temporal policy, assess severity and serialize a complete graph with counts/citations. Greedy generation uses the same 1536-output allowance within a 4096 combined bound. The original twenty training rows had eleven normalized distinct prefixes from one authored family. All original critical rows contained scan/authentication/compromise together.

## What was established, and what was inferred

Established: missing coverage and duplicated prefixes; exact semantic contradictions; graph/citation errors; adapter-specific flagged repetition on this fixed suite; valid reference answers fit below 857 tokens. Numerical stability and optimizer completion were checked. None of these alone identifies the underlying learning/generation cause.

Hypothesis: scenario-template shortcuts are dominating rule precedence. Curriculum changes are controlled tests of that hypothesis, with some observed gains. They have not established why the model loops, fails to withdraw support, or confuses evidence roles. Tiny data, generalization, optimization/objective effects and the combined reconstruction/interpretation/serialization task remain unresolved possibilities. An eighty-step completed run is not proof of adequate learning.

Process gap: a training-example generation readback and a separated evidence-state input test should have preceded another curriculum-only repair. Low teacher-forced loss was not sufficient evidence to move past that question.

## Interface checks now completed

`audit_interface.py` reconstructs actual saved v3/v4/v5 training prefixes using each job's saved rendering helper and compares them with evaluation rendering. All sixty training and fifty-two validation records match, and reconstructed lengths match actual training logs. Tokenizer EOS 151645 is recognized by generation's [151645, 151643] stop configuration. All logged sequences fit their context bound. See interface-audit.json.

This narrows evidence for prompt/template, stop-token or truncation mismatch. It audits saved code/configuration and logged lengths, not a dump of live tensor labels or all optimizer gradients. It does not rule out every training implementation, quantization or learning-dynamics issue.

## Corrections versus containment

Curriculum edits attempted learning corrections, not a proven root-cause fix. v4 improved some decisions and worsened some structural/repetition measures. v5 is still being evaluated; failures are retained.

Warning continuity, explicit incomplete status, retained evidence and bounded retries are failure containment. They do not establish model understanding or fix wrong reasoning. The output cap stops generation; it does not explain wrong labels already present before exhaustion. Raising it alone is not a semantic correction.

## Next discriminating checks, before any additional retraining

1. Generate exact trained examples with the saved adapter, especially a simple withdrawal and a benign/compromise/withdrawal combination. Compare with the base on the identical prompts. If the adapter fails its own examples, a pure out-of-sample coverage explanation is insufficient. If it fits those but fails the existing diagnostics, generalization becomes a stronger suspect.
2. Hold weights/decoding fixed and supply mechanically derived active/retired state for selected failed inputs, without supplying severity or target explanations. This tests the burden of reconstructing evidence state separately from interpreting it. The application was already intended to own provenance, time, duplicate identities and incident facts.
3. Separate compact assessed-warning output from optional long explanation/full-graph serialization in a later explicit experiment. This changes the task and must not be presented as the same matched full-state comparison.

These are proposed discriminating tests, not established fixes. Generated readbacks are training-fit diagnostics, never held-out accuracy evidence or new training targets. All future tests must preserve prompts, outputs and failures and keep model/training controls unchanged unless an explicit ablation says otherwise.
