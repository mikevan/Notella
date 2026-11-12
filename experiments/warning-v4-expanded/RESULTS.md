# Expanded warning profile v4 — results

This is an authored synthetic development experiment, not independent field evaluation or deployment qualification. All three fields (posture, combinedTrigger, evidenceClass) must match for a case pass.

| Condition | Primary cases | Robustness probes |
|---|---:|---:|
| raw base | 1/10 | 3/6 |
| raw adapted | 7/10 | 3/6 |
| temporal-facts base | 1/10 | 3/6 |
| temporal-facts adapted | 9/10 | 4/6 |

## Primary cases, condition by condition

| Pattern | Required output | Raw adapter | Same adapter + measured time facts |
|---|---|---|
| v4-ontoforge-heldout-corrob-sequence-0 | critical / met / corroborated_drone | critical / met / corroborated_drone | critical / met / corroborated_drone |
| v4-ontoforge-heldout-unknown-signal-0 | high / unconfirmed / unidentified_signal | high / unconfirmed / unidentified_signal | high / unconfirmed / unidentified_signal |
| v4-development-outage-only | high / unconfirmed / cause_unresolved | high / unconfirmed / cause_unresolved | high / unconfirmed / cause_unresolved |
| v4-development-reversed-order | contextual / not_met / reversed_sequence | contextual / not_met / reversed_sequence | contextual / not_met / reversed_sequence |
| v4-development-missing-clock | high / unconfirmed / unknown_time | contextual / not_met / unknown_time | high / unconfirmed / unknown_time |
| v4-development-distant-location | contextual / not_met / different_location | contextual / not_met / different_location | contextual / not_met / different_location |
| v4-development-benign-operations | contextual / not_met / benign_explanation | contextual / not_met / benign_explanation | contextual / not_met / reversed_sequence |
| v4-development-duplicate-reports | high / unconfirmed / dependent_reports | high / unconfirmed / dependent_reports | high / unconfirmed / dependent_reports |
| v4-development-outside-window | contextual / not_met / outside_window | critical / met / corroborated_drone | contextual / not_met / outside_window |
| v4-development-overlapping-clock | high / unconfirmed / uncertain_order | critical / met / corroborated_drone | high / unconfirmed / uncertain_order |

## What improved

The raw adapter retained both earlier anchors and met all fields for seven patterns, compared with one for the base under the same new prompts. Its raw misses were missing time, outside-window delay and overlapping clock uncertainty.

A separate post-hoc inference condition added interval measurements derived only from capture_summary. It made no new weight updates, changed no target labels, kept the same output schema/decoding and supplied no warning decision. The same adapter then handled those three temporal cases, but regressed the benign evidenceClass to reversed_sequence despite a correct contextual/not_met decision. Consequently the full primary score is 9/10, not 10/10.

## Remaining failures

- Instruction-like captured text changes the uncertain-signal warning to critical/met. The evidenceClass still says unidentified_signal, so the output is internally inconsistent as well as wrong under the supplied policy. This failure remains with time facts.
- Two reports relaying one upstream source do not reliably produce dependent_reports. The raw adapter emits generic-rf (outside the schema); the time-fact condition emits unidentified_signal. Both preserve high/unconfirmed, but fail the declared evidence classification.
- The raw adapter ignores a narrowed linking window in the robustness probe. Measured time facts correct this selected case.
- The measured-time condition misclassifies the benign case reason as reversed_sequence. The warning level alone is insufficient to count the case as passing.

## Training and provenance

The fresh adapter completed 90 applied updates, zero skips, and 144 finite saved tensors. The 45 training rows contain 30 original authored variants and 15 declared replays, balanced across three posture labels. No replay is counted as an independent incident. The ten development cases share source templates; the six robustness probes were frozen before v4 outputs were inspected. No previously inspected frozen-test rows or answers entered training.

The raw base/adapted prompt hashes, base intake and evaluator source match within each pair. The time-fact pair also uses identical augmented prompts. The saved adapter hash is unchanged between raw and time-fact inference. The calculator assumes the shared-clock assertion supplied in the input; it does not independently verify alignment or establish causation.

## Limits and next work

The temporal-facts condition is post-hoc development analysis. It supports investigating a hybrid arithmetic-plus-language pipeline, not a claim that the weights learned accurate timestamp arithmetic. Repeated synthetic patterns, changed class sampling and an expanded output taxonomy prevent broad accuracy or isolated-cause claims. No phone installation or release is authorized by these results.

Next work should isolate structured observations from irrelevant captured instructions, represent source lineage explicitly, and enforce declared relationships between evidence states, trigger status and posture without silently repairing generated answers. New prospectively frozen cases are required after any repair. The profile also needs a declared state for uncertainty that straddles the timing-window boundary; it is not covered by these scored fixtures.
