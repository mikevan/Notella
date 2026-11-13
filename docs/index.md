# Learn Notella

Notella turns explicit concepts, relationships and reviewed teaching examples into versioned training curricula. Its first implementation adapts local language models through LoRA. These guides explain both the intended meaning and the actual behavior of version 0.1.

## Intended method: Semantic Ontology Morphology

**The ontology represents the semantic model; morphology is its change over time; the AI interprets those changes. The trainer defines the model and its ontology representation first.** Start with [the method and node-edge reasoning](semantic-ontology-morphology.md), then [how Colibri will propose new scenarios](scenario-authoring.md). Both guides distinguish implemented tooling from planned scenario/state capabilities. [Tutorial 11: scenario contracts and teaching branches](scenarios.md) now runs the first seven provisional branches without a model.

## A suggested learning path

1. [Understand the method](concepts.md): ontology, semantics, LoRA, provenance and the difference between completion and success.
2. [Complete the first tutorial](tutorial.md): create a small ontology, compile examples, plan training and inspect a fixture evaluation without a GPU.
3. [Use the HTTP API](http-tutorial.md): run a server and repeat the workflow from another application.
4. [Run real training](training.md): configure local weights, submit a job, read numeric evidence and handle interruptions.
5. [Design curricula and evaluations](curricula.md): keep meaningful contrasts, split families and document source rights.
6. [Consult the API reference](api-reference.md): fields, routes, responses and failure examples.
7. [Record interpretation reviews](semantic-reviews.md): bind reviewer judgments to exact outputs and criteria.
8. [Understand implementation and limits](architecture.md): storage, job lifecycle, package boundaries and extension points.
9. [Troubleshoot](troubleshooting.md): common errors and the evidence to inspect.

For the first application, start with the [LayerTime ontology walkthrough](layertime-ontology.md), then read [temporal evidence](temporal-evidence.md), [development results](results.md) and the profile files in `examples/layertime.*.json`. The [project README](../README.md) supplies a compact start and route summary.

## What you need

Core tutorials: Python 3.11 or later, a writable local folder, and the Notella source. No GPU, model downloads or network access are required. Training tutorials additionally require a compatible CUDA setup, installed training dependencies and locally present model weights that you are permitted to use.

Run all commands from `C:\workspace\Notella` unless a guide explicitly says otherwise. Shell examples use PowerShell. Python examples use the public API rather than private helper functions.

## How to read results

A tutorial can prove that an interface works without proving that a model understands anything. A saved adapter can prove that training updated weights without proving that those updates improved behavior. A correct JSON response can still make a false claim. Each guide names exactly what its checks establish.

Examples, proposed warning policies, benchmark fixtures and observations from the field are different kinds of evidence. Keep their labels and provenance intact when building on this project.

## Portable profile packs

[Tutorial 6: package a reproducible profile](portable-profiles.md) shows how to pin ontology files, examples and training settings by hash, recreate artifact IDs on another installation, and detect changed or escaping input files. Preparation never launches training.

## Decision agreement and output compliance

[Tutorial 7: score declared decision fields](decision-scoring.md) keeps formatting, decision agreement and interpretation review separate, with examples of malformed JSON and correct decisions that violate a length limit.

## Measured temporal features

[Tutorial 8: derive time relations](temporal-features.md) shows the LayerTime adapter, shared-clock assumptions, provenance receipts and the separate no-training inference diagnostic.

## Trusted decision-task contracts

[Tutorial 9: input boundaries and output consistency](input-output-contracts.md) covers explicit source lineage, payload exclusion, allowed output states, review deferrals and honest evaluation after normalization. The latest [typed-training results](../experiments/warning-v6-typed-training/RESULTS.md) separate new controls from known-template regressions.

## Local teacher candidates

[Tutorial 10: draft and preserve local teacher candidates](teachers.md) covers the optional Python provider, restart behavior, review boundaries and teacher/student evaluation gates.

The [first smaller-student comparison](../experiments/student-v1-teacher-augmentation/RESULTS.md) records the direct 0.6B development candidate and negative teacher-augmentation result, with exact outputs and limits.

- [Tutorial 13: Rolling windows and semantic deltas](rolling-windows.md)
- [Tutorial 14: Focused monitoring and connected replay](focused-monitoring.md)
- [Tutorial 15: Diagnose semantic training failures](semantic-failure-diagnosis.md)
- [Completed 4B morphology comparison and correction plan](../experiments/scenario-model-v3/RESULTS.md)

- [Tutorial 16: Warning continuity and configurable output budgets](warning-continuity.md)

- [Curriculum-only rerun results and exact evidence](../experiments/scenario-model-v4/RESULTS.md)
- [Interpretation of the repaired curriculum and next target](../experiments/scenario-model-v4/INTERPRETATION.md)

- [Consolidated semantic morphology failure report](morphology-failure-report.md)
- [Five root-cause hypotheses and planned tests](../experiments/retraction-diagnosis-v1/HYPOTHESES.md)
- [Large-teacher/small-student evolution roadmap](teacher-student-roadmap.md)
- [Latest retraction/repetition comparison](../experiments/scenario-model-v5/RESULTS.md)
- [Complete runtime-document checkpoint archive](../archive/morphology-v1/README.md)

- [Scrollable infographic: from evidence to evolving meaning](infographics/semantic-morphology-evolution.html)
