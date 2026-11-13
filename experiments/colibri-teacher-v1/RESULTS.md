# First live local teacher result

The larger teacher connection ran successfully on this workstation. That establishes local inference feasibility, not training benefit.

The first free-form draft took 158.5 seconds, with 465 prompt tokens and 691 completion tokens, finish reason stop. It was rejected for training admission. Its first scenario explicitly assigned an unresolved outage cause yet called the combined trigger critical/met/corroborated_drone, contrary to the supplied policy. It also counted source origins across the two different event types rather than demonstrating distinct origins for the drone reports. The second scenario changed both lineage and time uncertainty, and proposed multiple evidence classes instead of an isolated contrast.

The response did correctly distinguish correlation and precautionary posture from proven causation and attack probability. Correct caveats did not rescue its incorrect classification.

See first-draft-review.json for the exact raw response, its hash and the separate agent review against prospectively recorded criteria. The review is agent-authored and not independent field verification. No draft entered a curriculum and no student was trained from it.

## Runtime and intake

All 45 model files matched the pinned public revision in teacher-intake.json. The downloaded prebuilt engine, not a locally compiled modified fork, was used. serve-settings.json records loopback serving on port 8877, context 2048, RAM plan 12 GB, Vulkan device cap 3072 MiB, requested expert tier 1 GiB, host pool 4 GiB and four CPU threads. Actual startup selected only two device-resident experts because the dense chain consumed most of the bounded device memory. Much expert computation remained on the CPU. These limits are chosen experiment settings, not a hardware speed ceiling.

The initial CLI --vram setting was rejected as CUDA-only. The successful launch used Vulkan-specific settings. An automatic host-pool startup was stopped before inference and replaced with an explicit 4 GiB pool. Startup also reported runtime dense int8 conversion and fp16 KV caching. Logs and the exact engine binary hash are retained in the local Colibri runtime intake folder. Do not infer performance of other precision/settings from this single configuration.

The ten-case structured compatibility diagnostic is recorded separately after completion. The existing controls are synthetic development cases, already inspected, not a new independent acceptance set. This is a different model and serving stack from the 4B adapter, not a matched engine benchmark.

## Completed structured diagnostic

| Measure | Configured 35B teacher |
|---|---:|
| Exact three-field decision matches | 5/10 |
| JSON/schema compliant | 10/10 |
| Evidence guard passes | 5/10 |
| Transport/runtime errors | 0 |
| Median end-to-end request time | 49.7 seconds |
| Total time for ten requests | 503.0 seconds |

Four incorrect replies asserted an unsupported critical combined trigger: unidentified RF, unresolved outage cause, different location and dependent reports. The fifth used outside_window instead of reversed_sequence. All five were rejected by evidence checks, without repair. Rejections are not counted as correct answers.

The unchanged trained 4B adapter previously matched 10/10 on the same case IDs (verified against the saved report). This is a reference comparison across different model/training/runtime conditions, not proof that Colibri itself causes worse accuracy or that all larger models perform worse.

Exact responses, checks and timings are in structured-control-results.json. Per-case request/result receipts preserve raw server replies and provider hashes under control-receipts/. The evaluator source snapshot and original scoring references are retained. These evaluation answers must not become teaching targets.

## Decision and next gate

The reusable connection and local feasibility are established. This untuned teacher stack is not approved as an automatic label source: its first authored draft failed review, and half of the structured development decisions were wrong. No teaching examples were admitted, no new student was trained, and the phone installation is unchanged.

The temporary teacher server was stopped after the diagnostic. Downloads and receipts remain local for reuse. All new source changes remain uncommitted.

Before scaling teacher generation, test a more constrained candidate format and review process, or use the already specialized 4B adapter as a candidate teacher. A matched small-student experiment still requires reviewed teaching material and a separately reviewed prospective evaluation set. Neither compression nor training speed improvements have been demonstrated.
