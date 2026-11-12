# Notella project working rules

Notella is a Project Revive Solutions project for ontology-guided semantic LoRA training. The reusable core must remain independent of the LayerTime profile.

## Owner-controlled check-ins

The owner inspects and executes all staging, commit and push scripts. Do not stage files, create commits, create remote repositories, or push on the owner's behalf. Read-only Git inspection is allowed. Local implementation, tests and authorized training are allowed. Prepare explicit, reviewable scripts for repository mutations; never use force-push or broad git add . in those scripts.

The first baseline is commit ceb5916. Check-In.ps1 and checkpoint/baseline-manifest.json describe that frozen baseline, not subsequent changes. Do not reuse or silently expand its manifest to stage later work. Prepare a separately reviewed checkpoint for later changes.

## Scientific and operational reporting

Keep requested iterations distinct from applied optimizer updates. Preserve source, corpus, model intake, exact generated outputs and failures. Valid JSON, finite tensors, loss and completed training do not prove semantic correctness or field qualification.

Use development validation to select experiments. Do not convert previously inspected frozen-test answers or generated acceptance outputs into training targets. Label synthetic variants and reviewer independence accurately. A critical precautionary posture is distinct from proven causation or a calibrated attack probability.

## Local development

Core tests: python -m unittest discover -s tests -v. Training uses a separately configured compatible CUDA environment and already present licensed model weights. Keep model weights, private captures and runtime job state out of source-control check-ins by default. Snapshot active jobs; do not edit their data or code during execution. Keep one local training server per store and inspect a held GPU lock before recovery.

## Documentation and identity

Document new public capabilities with runnable examples, expected outputs, failure cases and explicit limits. PRS visual language is angular amber #F2AB21 and vivid green #69D100 on black. Selected Notella logo direction: loose information strands becoming an ordered weave inside an angular brain. Preserve concept originals; version refinements.
