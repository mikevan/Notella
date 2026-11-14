# Learn Notella

Notella makes domain meaning, evidence, and evaluation explicit so models can be taught and tested against inspectable claims. Begin with **[Tutorial 0: set up your environment](setup.md)**. Choose [Windows](setup-windows.md) or [macOS/Linux](setup-macos-linux.md); no existing workspace is assumed.

## Before you run anything

[How we use and train AI](how-we-use-ai.md) explains where procedural work ends and learned interpretation begins. [Our iteration history](ai-iteration-history.md) links the successes, mistakes, regressions, and decisions behind the current research.

The [method](semantic-ontology-morphology.md) explains the intended Semantic Ontology Morphology approach: define the semantic model and its ontology representation, preserve evidence-backed changes, and evaluate interpretation over time. Reference components and synthetic fixtures do not establish a qualified field-warning system.

## Tutorial sequence

Follow the numbered sequence or choose a topic after completing Tutorial 0. Each tutorial links back here at the top and to its neighbours at the bottom. Tutorial 16 is the current end of the sequence.

| Tutorial | Topic | Environment and work performed |
| --- | --- | --- |
| 0 | [Set up your environment](setup.md) | Choose Windows or Mac/Linux; no GPU |
| 1 | [Your first semantic curriculum](tutorial.md) | Core environment; no GPU required for the documented fixture/report exercise |
| 2 | [Use the HTTP API](http-tutorial.md) | Core environment; no GPU required for the documented fixture/report exercise |
| 3 | [Design a useful curriculum](curricula.md) | Core environment; no GPU required for the documented fixture/report exercise |
| 4 | [Run and inspect real training](training.md) | Compatible CUDA environment and local model weights; starts training only when requested |
| 5 | [Record interpretation reviews](semantic-reviews.md) | Core environment; no GPU required for the documented fixture/report exercise |
| 6 | [Package a reproducible profile](portable-profiles.md) | Core environment; no GPU required for the documented fixture/report exercise |
| 7 | [Score decisions separately from formatting](decision-scoring.md) | Core environment; no GPU required for the documented fixture/report exercise |
| 8 | [Supply measured temporal facts](temporal-features.md) | Core environment; no GPU required for the documented fixture/report exercise |
| 9 | [Bind trusted input and output contracts](input-output-contracts.md) | Core environment; no GPU required for the documented fixture/report exercise |
| 10 | [Use a local teacher without admitting its answers](teachers.md) | Optional local teacher server; no student training |
| 11 | [Represent an evolving scenario](scenarios.md) | Core environment; no GPU required for the documented fixture/report exercise |
| 12 | [Score changing scenario states](scenario-scoring.md) | Core environment; no GPU required for the documented fixture/report exercise |
| 13 | [Preserve rolling windows and semantic deltas](rolling-windows.md) | Core environment; no GPU required for the documented fixture/report exercise |
| 14 | [Focus while broad monitoring continues](focused-monitoring.md) | Core environment; no GPU required for the documented fixture/report exercise |
| 15 | [Diagnose semantic training failures](semantic-failure-diagnosis.md) | Core environment; no GPU required for the documented fixture/report exercise |
| 16 | [Preserve warnings through incomplete output](warning-continuity.md) | Core environment; no GPU required for the documented fixture/report exercise |

Run commands from the project root you chose during setup. Whenever a guide says `python`, use your project interpreter from Tutorial 0. Most shell examples use PowerShell; the Mac/Linux setup explains the shell differences. Python snippets are portable unless a guide states an additional dependency. Training uses a separate compatible environment; do not install GPU packages merely to complete the core exercises.

When sharing a Notella tutorial outside the source code, include [Tutorial 0: environment setup](https://github.com/mikevan/Notella/blob/main/docs/setup.md) beside the tutorial link so readers have a clear starting point.

## Concepts and supporting guides

- [Concepts](concepts.md), [LayerTime ontology walkthrough](layertime-ontology.md), and [temporal evidence](temporal-evidence.md).
- [Scenario authoring](scenario-authoring.md) and [the large-teacher/small-student roadmap](teacher-student-roadmap.md).
- [API reference](api-reference.md), [architecture](architecture.md), and [troubleshooting](troubleshooting.md).
- [Project overview](../README.md) and [semantic positioning](semantic-morphology-positioning.md).

## Results you can inspect

- [Initial development results](results.md) and [typed-observation v6 results](../experiments/warning-v6-typed-training/RESULTS.md).
- [First smaller-student comparison, including negative teacher augmentation](../experiments/student-v1-teacher-augmentation/RESULTS.md).
- [Full-state v3 comparison](../experiments/scenario-model-v3/RESULTS.md), [v4 curriculum-only rerun](../experiments/scenario-model-v4/RESULTS.md), and [its interpretation](../experiments/scenario-model-v4/INTERPRETATION.md).
- [Latest v5 retraction/repetition comparison](../experiments/scenario-model-v5/RESULTS.md), [consolidated failure report](morphology-failure-report.md), and [root-cause hypotheses](../experiments/retraction-diagnosis-v1/HYPOTHESES.md).
- [Checkpoint archive](../archive/morphology-v1/README.md) and [the illustrated development story](infographics/semantic-morphology-evolution.html).

A tutorial can verify an interface without proving model understanding. Applied updates, finite weights, valid JSON, correct evidence interpretation, and operational warning delivery are distinct results. Each record keeps its own task, cohort, review provenance, and limits.
