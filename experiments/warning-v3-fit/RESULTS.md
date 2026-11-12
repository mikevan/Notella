# Balanced decision diagnostic v3 — results

A narrow positive result: the adapted model matches the required decision fields on both development cases; the same base model matches one. Both produce schema-valid outputs on both cases.

| Case | Base | Adapted | Expected |
|---|---|---|---|
| Corroborated local sequence | critical / met | critical / met | critical / met |
| Unidentified RF signature | critical / met | high / unconfirmed | high / unconfirmed |

The base model labels the uncertain RF evidence unidentified_signal but still sets critical/met. The adapter instead returns high/unconfirmed for that evidence and preserves critical/met for the corroborated sequence.

Training completed 60 applied updates, zero skips, ten passes over six synthetic variants from two families. All 144 saved adapter tensors are finite. Recorded training time was about 7.7 minutes. The native prompt, base-model intake and evaluator source match between base and adapted conditions. Training/inference prompt rendering parity was separately verified.

The experiment narrows the curriculum, balances the two patterns, changes the instruction and learning rate, and removes free-text explanations from the supervised output. It does not isolate which change caused the difference from v2. The new output is only a structured decision; it demonstrates no grounded free-text explanation or learned causal reasoning.

Two synthetic development families are too small and too closely related to establish general threat-detection accuracy. These validation cases have been used during development, and there is no untouched independent test in this experiment. This is a useful fit-stage result, not an acceptance or deployment result.

The ontology, examples and plan are reproducible from the portable profile.json pack. Exact generated outputs, model/adapter/evaluator hashes, data snapshots and numerical diagnostics remain under runtime/warning-v3-fit. The adapter is not installed on the phone and remains releaseEligible=false.


## Fit verification

All six training variants produce the required schema-valid decision fields (6/6). This resolves the selected training-fit failure observed in v2 within the new, restricted output task. The two development cases also pass (2/2), compared with 1/2 for the matched base condition. These are separate results: training fit is not held-out performance, and the development cases are not independent field evaluation.
