# Tutorial 13: Rolling intercept windows and semantic deltas

Continuous observation must retain meaningful changes without repeatedly treating old evidence as new support. This procedural foundation preserves the slices needed to investigate developing danger before deciding whether AI analysis is warranted.

Run from the Notella project directory:

```powershell
python -m examples.window_tutorial
```

Expected result: ten active intercepts, nine retained, `intercept-11` added, `intercept-1` expired, one updated semantic node, and `modelCalled=false`.

## The operational design

Keep a ten-second capture window and advance it by one second. At second 10 the interval is (0, 10]; at second 11 it is (1, 11]. All received intercept records within that interval participate in the domain projection. The overlapping nine seconds are retained evidence, not nine seconds of new independent support. Continue monitoring; when a meaningful pattern appears, preserve the incident evidence and assessment outside this short-lived buffer.

The ontology defines the semantic model. Domain projection maps intercept attributes and provenance into concept instances and typed edges. Semantic Ontology Morphology is the change in that model over time. The AI interprets those changes using the ontology, relevant current context, and retained incident history. A delta alone may be ambiguous: an added edge needs its endpoint meanings and provenance. Counts are not causal probabilities.

`RollingInterceptWindow` implements the clocked buffer. Ingest records with stable `id`, `observedAtMs`, and `availableAtMs`, optionally with a JSON payload. Both clocks must already be normalized to a common monotonic clock. Call `advance` at exactly the configured stride; receipt time prevents future or delayed reports from appearing prematurely. Identical retries are ignored; conflicting IDs and backdated receipt insertion are rejected. Reports older than the active interval are reported rather than revived as fresh evidence. Expiration also works when no new records arrive.

Defaults bound retained records to 100,000 and their serialized JSON to 64 MiB. Capacity rejection is explicit in ingestion results and frame counters. This is not an exact process-memory bound or proof of all-intercept throughput. Production ingestion must surface loss and preserve necessary evidence elsewhere. Raw waveform capture, clock synchronization, source authentication and classification remain application responsibilities.

## Send changes, retain context

`semantic_delta(before, after)` compares caller-validated complete semantic states with stable node and edge IDs. It returns added, removed and updated records, assessment changes, and state hashes. It does not infer which changes are important or whether an assessment is correct. Raw evidence leaving the ten-second buffer does not itself clear an incident or disprove a hypothesis. Incident retention and explicit resolution policy belong in the application.

`LatestWindowWork` bounds inference scheduling to one active request and one latest pending snapshot. Offer complete semantic snapshots internally. When work begins, it computes a delta against the last accepted input state. Replacing a pending snapshot therefore preserves surviving changes from intermediate ticks; replacing individual raw deltas could lose them. Transient events that disappear between snapshots require separate incident/event retention.

A result generated against an older revision is stale. `finish(revision, accepted=True)` will not accept it automatically. The application must validate its claims against current evidence before asserting `revalidated_revision=<latest revision>`. This argument records a caller assertion; the queue does not perform revalidation. The next delta still starts from the accepted request's input snapshot, so intervening changes remain visible.

## What is implemented and what remains

These reusable primitives and their tests run without a model. They do not yet connect interception, domain projection, salience detection, incident storage or a phone runtime. The current scenario training comparison reconstructs full prefix states as a diagnostic baseline; it is not a delta-trained deployment model. The scenario training contract also does not yet cover expiry-only steps.

A one-second window cadence does not establish one-second LLM inference. Benchmark model latency, throughput, memory, thermal behavior and missed-event handling on the target phone before setting its inference cadence. Keep collection and deterministic semantic updates running independently of slower inference.

See [Tutorial 14: Focused monitoring](focused-monitoring.md) for the explicit transition when something interesting appears, retained evidence and resolution.
