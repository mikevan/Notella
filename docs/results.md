[Tutorial index](index.md) · [Tutorial 0: environment setup](setup.md)

# Development results — November 12, 2026

## Actual LayerTime training

A fresh Qwen3-4B-Instruct-2507 adapter completed two passes through 371 training examples: 742 applied optimizer updates, zero skipped. All 144 saved adapter tensors were finite. Recorded training time was 992.96 seconds (about 16.5 minutes), excluding setup. Training loss was 0.8319 and validation loss 1.3693; these are optimization diagnostics, not accuracy measures.

The corpus combines 341 previously admitted development examples with 30 newly authored civilian-warning variants from ten synthetic families. Fifteen validation and fifteen test examples are separate from training. Of these, two validation and three test examples belong to the new warning profile. Existing frozen acceptance prompts remain excluded. These synthetic contrasts are closely related teaching material, not independent field validation.

The original run is preserved in `runtime/initial-layertime-run/runs/fresh-base-v1`. Its corpus and trainer source snapshots are retained alongside numeric diagnostics. Earlier rejected corpus builds and the first failed interface attempt are preserved with their labels. The adapter was not installed on the phone.

## Reusable Notella API

The core and HTTP API compile domain-neutral ontology curricula, preserve source permissions and admission, create allowlisted model training plans, launch local jobs and record structural evaluation results. The LayerTime example demonstrates the integration. The public API exposes concepts and directed relationships without importing LayerTime application code.

Automated tests cover family and prompt separation, training-source admission, output contracts, exclusion hashes, integrity tampering, path validation, HTTP authentication, client roundtrips, job execution/locking and uncertain temporal order. The final test count is recorded in `runtime/unit-tests.txt`.

A separate real HTTP-to-GPU integration probe completed two applied updates with zero skips and 144 finite tensors. This probe checks integration only; it does not establish a useful model. Exact job state, package/source manifests and results are retained in `runtime/backend-verification-result.json` and its referenced job directory. The initial failed probe remains separately recorded in its job folder.

## Qualification status

No semantic accuracy, causal discovery, calibrated threat probability, improvement over the base model, broad acceptance improvement or field qualification follows from these checks. The warning policy and example time window are project proposals. Generated held-out warning outputs and any interpretation review are stored separately in `runtime/warning-evaluation-v1`.

All candidates remain development-only. Neither the phone nor the LayerTime repository was modified during the Notella extraction. Notella has not been initialized as a Git repository or pushed to GitHub.

## First held-out warning answers

All three generated answers passed the compact JSON/reference checks. The critical case nevertheless failed: the model stated that the combined trigger was not established even though the supplied credible local sequence met the proposed policy. Its missing-clock answer maintained high concern but did not explain the timestamp limitation. Its benign-operations answer recognized scheduled maintenance but introduced an unsupported statement that neither disruption nor drone identity was independently corroborated.

These are agent-authored interpretation observations of three selected synthetic outputs, not independent expert scores or a field accuracy estimate. Generation took approximately 27.1, 20.4 and 14.3 seconds on the desktop GPU. No matched fresh-base comparison or full frozen acceptance reevaluation was performed for this adapter. No improvement claim is supported. The failure is preserved rather than hidden behind the three schema passes.

[Tutorial index](index.md) · [Start with environment setup](setup.md)
