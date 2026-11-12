# Balanced decision fit diagnostic v3

This deliberately narrow experiment selects three critical and three unresolved-signal training variants from the already authored development curriculum, with two separate development-validation families. It removes generated explanations and constant caution fields from the supervised output, retaining posture, combinedTrigger and evidenceClass. It starts a fresh adapter for 60 updates at learning rate 0.0001. Model/base prompts and decoding are matched as in v2.

The experiment changes data selection, output contract, instruction detail and learning rate together; it is a fit diagnostic, not an isolated causal comparison of curriculum weighting. Its purpose is to establish whether the model can reproduce the required source-identity distinction before expanding again. It does not test missing clocks, benign operations, unrelated locations or field generalization. No inspected test cases or model outputs are used as training targets.

Success criteria: critical/met/corroborated_drone for the supplied independently corroborated local sequence; high/unconfirmed/unidentified_signal for the generic RF case; same decisions on the corresponding two selected training examples. These are development/fit criteria only. Both base and adapted results, failures and exact prompt/output hashes must be preserved. A base/adapted tie establishes no training advantage. The schema contains no free-text explanation, so this run cannot demonstrate grounded prose or learned causal reasoning.

Versioned ontology.json and development-examples.json preserve the complete input material. Runtime plans, jobs and results are local under runtime/warning-v3-fit. The model is not eligible for installation or release regardless of this small diagnostic's outcome.

The post-training fit diagnostic will include all six training variants, not only one selected positive/negative pair. Report these separately from the two development-validation cases.
