# Tutorial 14: Monitor broadly until something warrants focus

Signs of developing danger need to remain available after the original capture window expires. Preserve the evidence that warrants attention while ordinary collection continues; this tutorial demonstrates that procedural boundary before model integration.

Run from the Notella project directory:

```powershell
python -m examples.focus_tutorial
```

Expected: `afterExpiry.mode` remains `focused`, `priorityIncidentIds` contains `incident-A`, and `broadMonitoring` stays true. After explicit resolution the mode is `broad`. The triggering `report-1` is still retained. No model is called.

## The transition that matters

Use the ten-second rolling window for broad monitoring until a validated semantic change warrants attention. Then open a focused incident and preserve its triggering evidence before window expiry. Continue collecting broadly while prioritizing changes related to that incident. Track its entities, typed relationships, temporal sequence, supporting evidence and counterevidence across successive windows. The semantic model defines their meaning; morphology describes how their support and relationships change.

`notella.focus.FocusMonitor` implements an explicit incident lifecycle:

1. `focus(incident_id, revision, reason, entity_keys, evidence)` opens or extends a focused incident. Supply stable evidence IDs and the actual evidence records, not just references into an expiring buffer.
2. `plan(changed_entity_keys)` returns active incidents, those affected by related changes, and `broadMonitoring=true`. The application chooses which semantic entity keys a change concerns. This is exact-key matching, not learned semantic relevance or an inference executor.
3. `resolve(incident_id, revision, reason, basis)` closes an incident only through an explicit `evidence_review` or `timeout_policy` decision. A timeout reason must identify the application's policy; the component neither measures inactivity nor invents a timeout. Resolution is a workflow state, not proof that no threat exists.
4. `snapshot()` returns a detached copy for inspection or application-controlled persistence.

Capture expiry never invokes resolution. Multiple incidents remain focused independently. Corrections append new evidence with a new ID; they must not overwrite retained originals. The application interprets the correction and revises semantic support and posture. A resolved incident is retained; renewed activity uses a new incident ID so its history stays distinct.

## Integration boundary and failure behavior

The component accepts an explicit, validated focus decision. It does not yet detect an interesting pattern, validate a model's claims, calculate threat posture, expand entity relationships automatically, schedule inference, or wire these decisions into phone interception. The tutorial uses a synthetic caller decision. The ongoing full-prefix model comparison remains separate and unchanged.

Default limits are 100 retained incidents and 64 MiB of serialized retained evidence. Limits include resolved incidents; reaching capacity raises an error rather than silently dropping the trigger. Conflicting evidence IDs, backdated revisions, missing reasons, and reopening resolved IDs are rejected. Failed focus updates leave stored state unchanged. Incident metadata and Python overhead are outside the evidence-byte limit; this is not an exact memory bound.

The store is in memory and is not thread-safe. Persist incident snapshots and provenance in the application before relying on retention across restarts. An application-controlled archive/recovery path is still required; there is no automatic eviction, durable audit log or restore API here. Callers must serialize updates and enforce admission, source authenticity, privacy and retention policies.

Use this with [Tutorial 13: Rolling windows](rolling-windows.md). Keep broad collection and deterministic semantic updates independent of slower AI inference. Prioritization must not stop collection or erase transient events while the model is busy.

## Connected replay: a pattern changes what we monitor

Run the composed reference flow:

```powershell
python -m examples.monitoring_replay
```

The synthetic timeline is:

| Time | Evidence / change | Expected behavior |
| --- | --- | --- |
| 1 s | Wi-Fi disruption at camp A | Broad monitoring |
| 5 s | Drone signature at camp A | Create a temporal edge and open focused tracking; retain both reports |
| 7 s | Additional signal report at camp A | Prioritize the incident and retain the related report |
| 11 s | Original Wi-Fi report expires; unrelated signal arrives at site B | Keep the incident and its evidence; keep monitoring site B broadly |
| 15 s | Original drone report expires | Reconsider the changed active graph without automatically closing the incident |
| 16 s | Triggering pair is outside the active window | Focus and retained history remain available |

This replay connects the real rolling-window, semantic-delta and focus APIs. Its small `project` function is an illustrative ontology projection, not the generic scenario graph schema. The example rule recognizes already-classified Wi-Fi-disruption and drone-signature records at the same site in strict temporal order within ten seconds. It opens precautionary focus; it does not infer an imminent attack, authenticate signatures, calculate criticality or establish causation. In a threatened camp the application may assign a high precautionary posture using a separately reviewed context policy. That decision is not silently embedded in this generic tool.

An overlapping pair produces one new edge and one trigger, rather than a new trigger every second. New reports at a focused site are retained. Related entity selection is deliberately explicit: cross-site links, shared sources, corrected reports, uncertain clocks and independent-support analysis need domain policy beyond this demonstration. Existing scenario validators remain separate and unchanged.

The replay emits every tick and retained incident as JSON. It is synthetic software verification, not model inference, training data admission or evidence of field performance. Its synchronous orchestration illustrates integration; durable incident storage, asynchronous AI scheduling, trigger validation and phone ingestion are still application work. In particular, the frozen training evaluation continues to measure full-prefix reconstruction and does not yet test this delta-input runtime.
