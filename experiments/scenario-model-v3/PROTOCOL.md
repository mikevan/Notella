# CPU-logit memory retry

Use the same immutable scenario ontology, curriculum, 80-update plan, frozen development scenarios and generation settings as scenario-model-v1. No labels or semantic inputs change. Preserve v1 (19 applied updates, no final adapter) and v2's zero-update longest-target check. Neither partial attempt counts as a trained candidate.

When --cpu-frozen-layers is selected, frozen output logits now stay on CPU; token-mean CE runs in checkpointed chunks on that device and its scalar loss returns to CUDA for the normal mixed-precision/optimizer path. The default offload helper remains compatible for callers that do not request CPU logits. Tests cover FP32/FP16 loss and gradient agreement, masking and shifted targets, invalid chunk/empty target handling, and differentiable CPU-logit to GPU-scalar transfer. Trace logs distinguish backbone, output projection and loss stages in the two-update hardware check. The full adapter starts fresh only after that check succeeds.

This is a practical implementation test of LLM interpretation of changing node-edge states, not a new non-LLM AI system or a formal research program.

## Monitoring progress without altering generation

Run `python experiments/scenario-model-v3/summarize.py` from the project directory. It reads the incremental journals, separates completed output counts from finalized conditions, reports contract/decision/graph measures and criticality confusion, and verifies prompt hashes for every available matched pair. Once both conditions finalize, it also compares evaluation, evaluator, scorer and curriculum identities. It does not modify prompts, targets, scores, model state or the running job. A snapshot can become stale as generation proceeds; rerun to obtain current progress. Partial baseline outputs do not establish a training benefit. The current evaluation reconstructs full prefixes and does not test the later rolling-window/delta design.
