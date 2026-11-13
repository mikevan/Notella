# Scenario comparison memory-bounded retry

Continue the same practical comparison defined in ../scenario-model-v1/PROTOCOL.md, with exactly the same ontology, admitted curriculum, plan, evaluation cases and decoding. The first attempt stopped at 19 applied updates with no saved final adapter after no optimizer progress on long-target work near the GPU memory limit. Memory pressure is suspected; no OOM exception was reported. Preserve the original job and its numerical records.

The engine loss now computes mathematically equivalent token-mean cross entropy in checkpointed chunks, avoiding retained full FP32 vocabulary buffers. CPU tests compare FP32/FP16 loss values and gradients, prompt masking/target shift, empty targets and chunk bounds. New source snapshots record this implementation. A two-update check of the longest training example must pass before the new full 80-update job. All adapters start fresh; discarded partial updates are not combined with a completed run.

No semantic labels, scenario inputs, assessment policy or evaluation references are changed. No new non-LLM reasoning architecture or broader research program is in scope.
