[Tutorial index](index.md) · [Tutorial 0: environment setup](setup.md)

# Tutorial 16: Output limits must not silently discard warnings

A long or incomplete explanation must not erase an already validated warning. Preserve the evidence and current warning state independently so output limits cannot silently undermine a person's ability to respond.

Run from Notella:

```powershell
python -m examples.warning_continuity_tutorial
```

Expected: `incident` stays active, the last validated critical assessment and its evidence remain available, and `requiresAttention=true`. The incomplete new assessment is explicitly not current. A retry plan grows the output allowance from 1536 to 2396 tokens with a 1700-token input inside a 4096-token context. No model, phone alert or network message is invoked.

## Keep warning continuity separate from explanation generation

Broad collection, validated semantic triggers and retained incident evidence must continue even if an AI response fails. The application should expose its compact validated warning state immediately; a long narrative or full graph serialization must not be a prerequisite for presenting an already validated warning. An incomplete assessment never means all clear. Conversely, exhaustion does not itself prove a critical threat; when there is no validated assessment, return that explicit gap and require attention rather than fabricate a severity.

`AssessmentContinuity(validator)` holds the last validated assessment and revision. The required callback checks domain policy and current evidence and returns exactly True for acceptance. Schema validity alone is insufficient. `finish(assessment, revision, latest_revision, finish_reason)` accepts complete current validated results. Token-limited, stale, generation-error and invalid-assessment results preserve history, return `assessment_incomplete`, and require attention. Ordinary pending work returns `assessment_pending`; it does not itself invent a threat alert. Active focused incidents still require attention while work is pending. Previously validated history is marked not current after failure; it must not be passed off as a new assessment. Latest revisions cannot move backwards, even when the latest generation failed.

`warning_state(focus_monitor, outcome)` returns the active incident IDs and retained assessment immediately, without invoking a model. It neither creates a threat classification nor delivers an alert. Assessment acceptance does not resolve an incident: explicit evidence review or the application's timeout policy must call the focused-monitoring lifecycle. Validated de-escalation remains possible; there is no permanent critical latch.

The callback in this tutorial compares against synthetic prevalidated policy outcomes. It illustrates an interface, not a production semantic validator or source-authentication mechanism. State is in memory, is not thread-safe and needs application persistence. UI delivery, notification reliability and phone background execution remain unimplemented integrations.

## Give useful answers room, within a measured budget

`OutputBudget` makes output capacity configurable rather than hiding a universal allowance inside a caller. It accounts for both input length and output capacity. Default initial output is 1536, maximum output 4096, context 4096, with one retry. These are configurable reference defaults, not a measured phone configuration or the base model's inherent limits.

After token exhaustion, `after_limit(input_tokens, attempt)` plans one larger attempt when space permits. If no larger attempt fits, or retries are exhausted, it returns an explicit review result. It does not execute inference, truncate input, expand device context without authorization, or loop indefinitely. The caller must preserve incomplete raw outputs and retry provenance, check the finish reason, retain incident continuity, and apply validation to the new result. A retry's added context must come from a device profile whose memory and latency have been measured. Input that consumes the whole context is an explicit error, never silent truncation of evidence.

If an initial allowance cannot fit because of input size, `allowance` returns the remaining output capacity. The caller must inspect that value; substantial evidence/context should be selected or compacted through a documented semantic policy, not blindly dropped. Exhaustion and insufficient context are attention conditions. More output tokens can worsen repetition and latency; they cannot repair an incorrect decision already generated. Consider compact assessment outputs and separate optional explanations in a separately measured experiment.

## Preserve comparisons

The active curriculum-only v4 comparison retains the previous 1536-token cap and 4096 combined bound. Changing it mid-run would change the measurement. These new primitives do not alter its frozen evaluator or training snapshots. In that experiment all reference answers fit in at most 857 output tokens, so the observed capped responses have space to be correct; they spend it repeating instead. The guarded runner connects these primitives to a caller-provided backend; it is not yet wired to a real model provider, phone runtime or notification channel. The active comparison does not use it.

## Guarded generation runner

`run_guarded_generation(generate, continuity, focus_monitor, budget, input_tokens, revision, latest_revision, on_state)` exposes warning state through `on_state` before invoking the backend. The tutorial uses a simulated backend to demonstrate a length stop followed by a successful larger attempt: limits 1536 and 2396, retained warning present before either attempt, two exact raw outputs retained, and a validated final assessment. No real model is called.

The backend callback receives the allowed output tokens and must return exact `text` and a trustworthy `finishReason` (`complete` or `token_limit`). It must honor the measured context and token budget. The caller captures the prompt and evidence snapshot corresponding to `revision`. The `latest_revision()` callback is checked again after generation; stale evidence is not retried as if current. The `on_state` callback connects to the application's immediate warning view. Its invocation is not proof of delivery to a person; notification reliability must be separately implemented and tested.

Length failures alone may retry with more space. Invalid JSON, duplicate keys, unsupported assessments and backend exceptions do not trigger unlimited repair loops. Successful retries clear the pending retry plan. Every model attempt returns its exact text and hash, or an error type, for durable caller audit storage. No partial JSON label is accepted. Application code must persist those receipts and handle errors in its validation, revision and delivery callbacks. The component preserves active focused incidents; it does not authenticate observations, discover attacks, create calibrated threat levels or send an alert by itself.


### Keep useful results usable while windows advance

One-second window updates can outpace model inference. The runner accepts optional `revalidate(assessment, input_revision, current_revision)` to explicitly check a completed older proposal against live evidence. It must return exactly True after a real domain check; a revision number or generic True stub is not revalidation. The normal assessment validator then runs against the current revision as well. The attempt receipt retains its original input revision and records the revision at which it was revalidated. If evidence changes again during the check, the result remains stale. Without this callback, stale results are rejected and must not replace accepted assessments.

This is assessment validation, not rewriting the model's input history. If combining it with `LatestWindowWork`, retain the original request snapshot as its delta baseline so intervening semantic changes are not lost. Serialize evidence updates, revalidation and acceptance in application code; these in-memory components do not provide cross-thread transactions.


The runner is synchronous. Call it from an inference worker, separately from collection, window advancement and the UI event loop. The state callback must dispatch promptly to the application's warning path. Token bounds do not enforce a wall-clock deadline or guarantee display, background execution, cancellation or delivery; the real backend needs measured deadlines/cancellation and a supervised worker. These integrations remain required before operational use.

---

[Previous: Tutorial 15 — Diagnose semantic training failures](semantic-failure-diagnosis.md) · [Next: tutorial index — end of the current sequence](index.md)
