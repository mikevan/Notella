# Post-hoc temporal-facts diagnostic

After the raw expanded comparison, three primary failures concern temporal interpretation. This diagnostic changes inference context only; it performs no training and changes no output labels, schemas, model weights or decoding settings. It evaluates both the base and the same adapter on all ten primary cases and all six probes.

A LayerTime-specific adapter supplies the existing interval calculator's order, delay bounds, window inclusion and configured window. It derives these from capture_summary only and never reads target labels. Unknown alignment is not numerically subtracted. Missing/overlapping times remain unknown/uncertain; they are not converted into negative evidence. No source identity, source independence, posture, trigger decision or attack probability is computed.

Model-visible additions contain only the measured relation and window. Full input hashes, algorithm provenance and the scope of the shared-clock assumption are retained in receipts. The model receives no extra instruction and no target answer. Existing evidence, including instruction-like captured text, is retained.

This is a separate post-hoc development condition, not a fresh test or evidence of further weight learning. Any improvement can support a hybrid numeric-facts-plus-language approach; it cannot be claimed as independent field accuracy or prove the cause of the raw model's errors.
