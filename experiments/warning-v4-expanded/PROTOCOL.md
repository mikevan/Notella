# Expanded compact warning experiment v4

Frozen before generating this run's outputs. This broadens v3's three-field decision task to the ten previously authored warning patterns. It retains all 30 original training variants, adds 15 explicit replays to balance critical/high/contextual at 15 rows each, and uses 10 development cases. The replays are not new incidents; the development views share underlying synthetic pattern templates and are not independent field evidence. Previously inspected test cases and generated test answers are not loaded.

A fresh 4B adapter receives 90 requested updates (two passes over 45 rows), rank 16 and learning rate 0.0001. The task excludes free-text explanations. Causal understanding, attack probabilities, actual RF classification and deployment qualification are not measured.

Prospective decision criteria: all three fields must match the authored proposed policy. The ten cases cover corroborated sequence, uncertain signal, unknown outage cause, reversed order, missing clock, different location, verified benign operations, dependent reports, outside-window delay and overlapping uncertainty. critical/met must remain correct for the corroborated anchor; high/unconfirmed for the unidentified-signal anchor. All other cases must preserve the stated missing or negating condition through evidenceClass.

Base and adapted generation use identical messages, tokenizer, greedy decoding and output budget. Preserve each exact output, prompt hash, adapter/base intake hashes and failed cases. Compare raw decision fields separately from schema validity. Both must pass for a compliant result. The two previous anchors are developmental regression checks, not untouched acceptance tests.

If broadening loses the critical anchor or invents a trigger, do not replace the v3 diagnostic or phone model. All artifacts remain releaseEligible=false. Runtime files are under runtime/warning-v4-expanded; profile.json pins the versioned input files and settings. Source code and the sampling audit document every replay.
