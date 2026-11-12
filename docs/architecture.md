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

The engine is a compatibility boundary inherited from LayerTime's development tools. Its train_lora.py remains unchanged. The Notella-specific manifest verifier replaces domain_training_profile.py, and the prompt adapter recognizes Notella's domain-neutral curriculum version. Historical helper names remain inside the engine; they are not public API concepts. Its original source includes additional utilities not yet split into independent packages.

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
