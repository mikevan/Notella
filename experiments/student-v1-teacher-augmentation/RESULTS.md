# First 0.6B student diagnostic results

Two fresh local Qwen3-0.6B LoRA adapters were trained and evaluated sequentially. Neither the existing 4B adapter nor the phone model was changed.

| Condition | Training rows (unique inputs) | Applied / skipped updates | New numeric-variation controls | Existing v6 controls |
|---|---:|---:|---:|---:|
| Direct ontology-guided | 45 (24) | 90 / 0 | 8/8 | 10/10 |
| Plus six reviewed teacher decisions | 51 (30) | 90 / 0 | 6/8 | 8/10 |

Both adapters have 112 finite tensors. Both returned schema-valid JSON for every case in both cohorts. The augmented model confused dependent reports with unidentified signal, and outside-window timing with reversed order. Evidence checks rejected its incorrect explanations; rejection is not a correct model decision. No answer was repaired.

The eight numeric-variation controls were frozen before teacher admission, with no exact input overlap against v6 examples or the six added teacher cases. They share known synthetic policy patterns and authorship. The ten historical controls were already inspected development evidence. Neither cohort establishes independent generalization. The direct 0.6B model matches the prior trained 4B adapter's 10/10 on the historical case IDs; this does not establish equal general capability, field accuracy or phone suitability.

## What this establishes

We have a trained smaller development candidate for the scoped three-field policy task. The direct condition is preferred for further diagnostics. Teacher augmentation did not improve this run and reduced observed decision agreement. This is not a causal demonstration that teacher material is harmful: adding rows changed quantity and sampling, and only one seed/update budget was tested. The teacher predictions matched already authored reference labels, so they did not supply new ground truth.

Training used the same local base, seed 42, rank 16, alpha 32, learning rate 0.0001, completion-only QLoRA path and 90 requested updates. Both applied all 90 without overflow skips. Exact source/data snapshots, gradients and adapters remain in the per-job runtime folders; checks and model-file receipts are preserved here. Total job wall times include loading/checkpointing and are not a matched training-speed benchmark against the 4B model.

The selected direct adapter is in runtime/student-v1-teacher-augmentation/store/jobs/8f724cbea6e543c49a2ca5df0ecde5af/adapter and has SHA-256 c7399ebba35040a6b350eafa1802d02b90e2c4ae2715acad37f3f9fa81354c99. Its 9,189,904-byte adapter requires the original base model; it is not a standalone phone model. No quantized phone export, thermal/battery benchmark, structural pruning or deployment was performed.

## Reproduce and inspect

The frozen experiment scripts refuse to overwrite prepared/completed runs. Inspect PROTOCOL.md, controls.json, explicit-admission.json, teacher-reviews.json and both exact-output evaluation reports. To repeat, create a separately named experiment/runtime location rather than weakening preservation checks. The reusable Notella teacher/review/training APIs are documented in docs/teachers.md and docs/training.md; these experiment files are evidence snapshots, not a generic batch service.

The next useful gate is broader separately reviewed scenarios and quantized export/device measurement of the direct 0.6B candidate. More teacher generation is not justified by these results alone. No release qualification is claimed. All changes remain owner-controlled for check-in.
