[Tutorial index](index.md) · [Tutorial 0: environment setup](setup.md)

# AI iteration history

We keep successful experiments and failed approaches visible so the next change responds to evidence. This is a reading guide to preserved records, not a new evaluation or a claim that all scores measure the same task.

[How we use and train AI](how-we-use-ai.md) explains the workflow. For runnable exercises, begin with [Tutorial 0: environment setup](setup.md) and the [tutorial index](index.md).

## What we changed and what happened

| Iteration | Result and mistake exposed | Decision and source record |
| --- | --- | --- |
| Initial Notella training and API integration | A fresh 4B adapter applied 742 updates with no skips and finite tensors. The selected critical warning example still failed interpretation despite valid structure. The initial failed integration attempt was retained. | Treat numerical completion and a working API as integration evidence, not model success. [Initial results](results.md). |
| Typed-observation decision training v6 | On ten new authored development controls, base decision agreement was 5/10 and the adapter's was 10/10. Its 19/19 historical regressions included 18 normalized inputs identical to training inputs. | Keep the narrow success and disclose overlap. Do not call the regression score generalization or field accuracy. [v6 results](../experiments/warning-v6-typed-training/RESULTS.md). |
| First 0.6B student and teacher augmentation | Direct training matched 8/8 new numeric-variation controls and 10/10 historical controls; adding six reviewed teacher decisions matched 6/8 and 8/10. Both completed 90 updates. | Prefer the direct candidate for further diagnostics. Teacher benefit was not demonstrated; one run does not establish a general causal effect. [Student comparison](../experiments/student-v1-teacher-augmentation/RESULTS.md). |
| Full evolving-state v3 | Schema validity improved from 3/10 to 8/10, while criticality agreement stayed 3/10. Complete state agreement was only 1/10 for the adapter. | Valid JSON and familiar graph shapes did not demonstrate semantic interpretation. [v3 results](../experiments/scenario-model-v3/RESULTS.md). |
| Curriculum correction v4 | Known-case criticality improved from the prior adapter's 3/10 to 6/10, but capped outputs worsened from 2/10 to 4/10. Fresh-case decisions matched 5/8 versus the base's 4/8; complete state matched only 2/8. | Retain both improvement and regression. Historical presence was still confused with active support. [v4 interpretation](../experiments/scenario-model-v4/INTERPRETATION.md). |
| Retraction-focused v5 | On 18 known cases, criticality improved from the previous adapter's 11/18 to 13/18, but complete state fell from 4/18 to 1/18. On six fresh cases, base criticality was 6/6 versus adapter 5/6; adapter complete state was 2/6. | Reduced repetition was not a semantic fix. Keep exact answers and investigate active versus withdrawn support. [v5 results](../experiments/scenario-model-v5/RESULTS.md). |
| Diagnosis and warning continuity | We tried curriculum corrections before checking generation on exact training examples. The consolidated review identifies that process gap; proposed root causes remain hypotheses. Runtime components preserve validated warnings through incomplete generation, using a simulated backend. | Test competing explanations before another training run. Warning containment is not a learning fix or proven phone delivery. [Failure report](morphology-failure-report.md), [hypotheses](../experiments/retraction-diagnosis-v1/HYPOTHESES.md), [continuity tutorial](warning-continuity.md). |

The compact decision task and full-state task have different inputs, outputs, and evaluation roles. Do not combine their scores into one accuracy figure. Cases called fresh were frozen before the relevant run but remain same-author synthetic development controls, not independent field incidents.

## Where the evidence lives

Each linked experiment preserves its protocol and detailed results. Where available, follow those records to exact generated outputs, per-case judgements, hashes, and training receipts. The [checkpoint archive](../archive/morphology-v1/README.md) indexes retained runtime documents and source snapshots. Private captures, model weights, and local runtime paths are not promised as public downloads.

[Vixen's iteration record](https://github.com/mikevan/Vixen/blob/field/ecosystem-evidence-parity/docs/ai-development/iteration-history.md) separately tracks phone-model failures, controlled component successes, and the gap to ordinary field operation. An experiment in one repository does not imply deployment in the other.

## How we record the next iteration

Before running it, state the question, dataset and split identities, base/adapter identities, changed variables, comparison conditions, and acceptance criteria. Afterward, record requested versus applied work, exact outputs, errors, semantic review, uncertainty, and the resulting decision. Preserve the prior result; use a new experiment identity for changed data, representation, or decoding settings.

Known evaluation answers and generated acceptance outputs stay out of optimizer input. A failed answer remains a failed answer even if an external checker rejects it. Promotion requires evidence for the intended workflow, not a favorable subset of examples.

[Tutorial index](index.md) · [Start with environment setup](setup.md)
