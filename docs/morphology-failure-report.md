[Tutorial index](index.md) · [Tutorial 0: environment setup](setup.md)

# Semantic morphology failure report

The controlled 4B experiments did not produce a reliable deployable semantic-morphology model. Training completion and valid formatting were insufficient evidence of semantic correctness. No candidate was installed on a phone or qualified for operational warnings.

| Experiment | Decision agreement | Complete state agreement | Repetition / completion |
| --- | --- | --- | --- |
| v3 | Base 3/10; adapter 3/10 | Base 0/10; adapter 1/10 | Adapter two capped outputs |
| v4, known ten | Prior adapter 3/10; new adapter 6/10 | Prior 1/10; new 2/10 | Capped outputs worsen from 2/10 to 4/10 |
| v4, fresh eight | Base 4/8; adapter 5/8 | Base 0/8; adapter 2/8 | One capped response in each condition |
| v5, known eighteen | Prior adapter 11/18; new adapter 13/18 | Prior 4/18; new 1/18 | Repetitive narratives and capped outputs each fall from 5/18 to 1/18 |
| v5, fresh six | Base 6/6; adapter 5/6 | Base 0/6; adapter 2/6 | No flagged repetition or capped responses |

These are same-author synthetic development controls. Known cases were inspected and informed subsequent curriculum work; they are not independent generalization evidence. The previous adapter was not generated on each newly authored fresh set. Reference agreement follows proposed policy, not calibrated attack probabilities or field truth.

## Observed failure

Models confuse historical evidence with current support, use a source correction or credential activity as if it establishes current compromise, mix report IDs with graph-node IDs, and construct inconsistent counts/edges. Some contradictory narratives repeat until the output cap. Semantic mistakes also occur in complete responses, while some loops begin with the expected label: the two failure modes must be investigated separately.

The first documented trained-model loop in this scenario series is v3 S-Q92-step-4. Semantic errors appear earlier, including v3 S-Q71-step-1 (standalone reviewed compromise called contextual) and step-5 (withdrawn compromise still treated as critical). The base also makes semantic and completion errors, but the fixed narrative-repetition heuristic flags none of its inspected outputs.

v5 S-Q71-step-5 acknowledges retired r17, continues using it and credential activity as access support, and repeats until the cap. This is preserved as incomplete output, not accepted by extracting its initial label. Valid evaluation reference answers fit within 857 output tokens; the unchanged generation allowance is 1536. Raising that allowance alone is not a demonstrated semantic correction.

## Conditions and what was actually tested

Each run starts from the same pretrained Qwen3-4B-Instruct-2507 base and a fresh LoRA adapter, not the previous adapter. Rank 16/alpha 32, q_proj/v_proj modules, learning rate 0.0001, seed 42, batch/accumulation 1, NF4 QLoRA, CPU frozen-output training offload, eighty updates and twenty training rows were held fixed. Each completed candidate applied eighty updates, skipped zero, and had finite weights. Full-prefix input and full-state output were retained. No larger teacher or distillation was used in these three comparisons.

The v3 curriculum had only eleven distinct prefixes. v4/v5 had twenty unique prefixes, with more explicit semantic contrasts. v5 also shortened and diversified rationales and separated change summaries. Those are combined data interventions, not isolation of a single root cause.

## Root cause remains unresolved

Curriculum weaknesses are verified. Shortcut learning, reconstruction burden, supervision imbalance, inadequate effective learning and autoregressive feedback are hypotheses. We attempted curriculum corrections before checking generation on exact trained examples; that was a process gap. Warning preservation/retries are failure containment, not a learning fix.

Saved v3/v4/v5 prompt reconstruction checks match all sixty training and fifty-two validation records. Logged token lengths agree, no truncation is found, and tokenizer EOS is recognized by generation. This narrows interface-mismatch possibilities without proving correct live gradients, adequate learning or semantic truth.

Before additional retraining, run the discriminating tests in [the hypothesis plan](../experiments/retraction-diagnosis-v1/HYPOTHESES.md), starting with exact training-example readback. Then test explicit active/retracted state while holding weights fixed. Do not silently count a representation/output change as the same full-state experiment.

## Evidence and operational boundary

[Latest exact results](../experiments/scenario-model-v5/RESULTS.md), [root investigation](../experiments/retraction-diagnosis-v1/DIAGNOSIS.md), and [interface audit](../experiments/retraction-diagnosis-v1/interface-audit.json) preserve detailed evidence. The checkpoint archive preserves all collected runtime documents, training records and source snapshots byte-for-byte, with hashes and original paths. Model weights and optimizer binaries remain local with a separate hash inventory.

Broad ten-second monitoring, one-second advancement, focus retention and bounded warning-continuity components are implemented and tutorialized. Real-provider/phone integration and notification delivery remain untested. Incomplete generation must not clear an incident or silently suppress a validated warning. Ordinary pending monitoring must not invent a threat alert.

[Tutorial index](index.md) · [Start with environment setup](setup.md)
