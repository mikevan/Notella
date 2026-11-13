# Architecture and extension guide

## Boundaries

```text
PRS application / command line / HTTP client
                  |
          notella.core.Notella
           /      |       \
     Ontology  Curriculum  Evaluation
                  |
             Training plan
                  |
             notella.jobs.Jobs
                  |
       Job dataset + source snapshots
                  |
          Local LoRA engine process
                  |
         Adapter + numeric diagnostics
```

The core has no LayerTime imports, GPU dependencies or network requests. A profile supplies domain definitions and examples. The HTTP layer translates requests into the same core calls. Client is a small transport convenience. Jobs owns local subprocess execution and the model allowlist. Correlation provides independent timestamp interval arithmetic.

## Source map

| Location | Responsibility |
|---|---|
| notella/core.py | Contracts, provenance admission, content-addressed storage, curriculum compilation, plans and structural evaluation |
| notella/http.py | Loopback HTTP server, bearer authentication, JSON limits and route handling |
| notella/client.py | Reusable HTTP client |
| notella/jobs.py | Training export, source snapshots, exclusive store lock, subprocess and completion monitoring |
| notella/training_profile.py | Verify Notella exports at the retained engine boundary |
| notella/correlation.py | Time-order/window interval calculation |
| notella/openapi.py | Machine-readable route description |
| notella/__main__.py | CLI serve/demo commands |
| training_engine/ | Retained local training implementation and supporting modules |
| examples/ | Runnable tutorials and the first LayerTime profile |
| tests/ | Core, HTTP, job-boundary and temporal checks |
| runtime/ | Local training/evaluation evidence; excluded from future source-control staging by default |

The engine is a compatibility boundary inherited from LayerTime's development tools. Its current train_lora.py selects CPU-resident frozen output logits for the --cpu-frozen-layers path, and completion_loss.py uses bounded token chunks; per-job source snapshots preserve earlier implementations. The Notella-specific manifest verifier replaces domain_training_profile.py, and the prompt adapter recognizes Notella's domain-neutral curriculum version. Historical helper names remain inside the engine; they are not public API concepts. Its original source includes additional utilities not yet split into independent packages.

## Artifact lifecycle

Ontology registration produces an immutable hash identity. Compilation resolves that exact ontology and produces immutable messages and provenance. Plans refer to a curriculum by identity. Jobs export a snapshot and verify hashes before running. Training output retains corpus, arguments, environment and source evidence. Evaluation records refer back to the exact curriculum.

Core JSON artifacts use complete-write temporary files and atomic hard-link publication. Job state is updated with temporary-file replacement under an in-process lock. One API process per store is supported. This is a local filesystem architecture, not a transactional distributed database or concurrent-worker scheduler.

## Job lifecycle and source capture

The server acquires gpu.lock with exclusive file creation before exporting data. Each job receives a unique folder. Engine and Notella module files are copied into the folder, hashed, and executed from those copies. stdout and stderr are persisted. The parent monitors the child, updates status and releases the lock in its normal completion path.

If the server crashes, automatic reconciliation is absent. The child may remain active and the lock intentionally remains. See the recovery procedure in [training](training.md). A production scheduler should add durable worker ownership, heartbeats, PID/start-time checks, cancellation and audited recovery rather than infer success from a directory name.

## Add another domain

Create an ontology and examples using the documented public fields; register and compile them through the existing API. Keep the base model and domain separate. A domain can change without changing the training transport. Use concept/relationship definitions and contrasting targets appropriate to the task, rather than renaming LayerTime's warning labels.

To demonstrate that a new domain remains independent, the temperature tutorial imports only Notella's public API. Its core workflow requires no LayerTime Android code or application-specific validator.

## Add another training backend

Jobs is the current local implementation, not a formal plugin registry. A future backend should accept immutable plans and curricula, own its model/executable configuration, preserve source/data/environment receipts, enforce split separation and distinguish applied updates from requested steps. It should return a durable job identity and preserve failures.

The HTTP server accepts an injected jobs object with start(plan_id) and get(job_id) methods. This is the current extension seam. Backends must not accept arbitrary shell commands from untrusted requests. In-process core users can choose another orchestration layer without changing ontology compilation.

## Deliberate limits

Version 0.1 does not implement model serving, remote training, cancellation, queues, multi-user authorization, formal ontology reasoning, automatic source licensing checks, semantic judging or product-release approval. The documentation identifies these so integrators can rely on actual behavior rather than infer features from the project name.

Before broader adoption, prioritize independent curriculum review, more domain-neutral engine packaging, durable job recovery, a formal backend interface and independently validated semantic evaluation. Changes to these boundaries should include examples and compatibility notes, not only code.


## Intended scenario reasoning architecture

The ontology represents the semantic model; an scenario supplies changing observations, scoped concept instances, typed relationships and hypotheses. The trainer defines the model and representation. The application will maintain versioned scenario state and the model will interpret its changes, propose supported revisions and assess criticality under a named policy. Application validators must check evidence references, identity scope, time, provenance and permitted transitions.

The first Python scenario contract, explicit validation, full-prefix export and rule fixtures are implemented in `notella/scenarios.py` and the source-checkout `profiles/network_scenarios` profile. A live scenario-memory service, trained scenario interpreter and rollout evaluation remain intended extensions. Runtime evidence changes the scenario state/context; ordinary inference does not update neural weights. LoRA training adapts behavior from reviewed examples without proving a literal internal ontology graph.

```text
Trainer's semantic model -> versioned ontology + assessment policy
                                  |
                    Colibri scenario candidates
                                  |
             structural/domain review -> explicit admission
                                  |
                 scenario-prefix curriculum -> LoRA training

New evidence -> versioned semantic state -> model interpretation
                      ^                        |
                      +--- validated revisions + assessment
```

Nodes represent scoped semantic elements. Edges carry relationship type, evidence, temporal conditions and uncertainty. Counts support association only under a defined matching unit and query/scenario scope; causal or criticality judgments require additional semantics. See [the method](semantic-ontology-morphology.md) and [scenario workflow](scenario-authoring.md).

Current optional modules `notella/teachers.py` and `notella/teacher_reviews.py` provide local candidate generation and exact-output reviews. They do not themselves implement a live scenario-state service, complete scenario validation, neural introspection or automatic admission. The separate scenario module provides bounded structural/evidence validation; [Tutorial 11](scenarios.md) states its limits. Notella's domain-neutral core remains independent of LayerTime and Colibri.

## Scenario contract v1

`notella/scenarios.py` provides the closed graph-state schema, explicit evidence/clock/provenance checks, family/shared-prefix guards and full-prefix teaching export. It imports no application profile or model dependencies. `profiles/network_scenarios/reference.py` supplies a proposed domain ontology, transparent rule comparator and fixture-authoring helper. Frozen ontology/scenario JSON files support review. Source-checkout profiles are not packaged runtime services.

An scenario reference target is not authoritative because it passed the generic contract. Domain review, rule/model comparisons and independently authored scenario families are separate requirements. All current scenario fixtures are unadmitted. The no-model [tutorial](scenarios.md) verifies that the compiler refuses to train on them.


## Scenario naming compatibility

The public `notella.scenarios` interface delegates graph validation to the preserved `notella.episodes` implementation. New profile/record names use scenario terminology; the retained episode module, profile JSON and historical receipts remain valid. The new profile wrapper preserves policy behavior and exposes the terminology/version change explicitly. See [scenario compatibility](scenarios.md#compatibility-and-preserved-evidence).
