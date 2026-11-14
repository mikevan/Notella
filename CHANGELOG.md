# Change log

For tutorials, begin with [Tutorial 0: environment setup](docs/setup.md) and [the tutorial index](docs/index.md). [The AI iteration history](docs/ai-iteration-history.md) connects the changes to measured outcomes and preserved failures.

## Unreleased

- Added a typed decision-task boundary, explicit caller-supplied source-lineage summaries and output-state/evidence consistency checks. Captured payloads remain in source artifacts but are excluded from this task's model view; rejected answers are not repaired.
- Preserved the negative v5 compatibility diagnostic: the previous adapter did not automatically transfer to the new representation.
- Completed v6 training: 90 applied updates, ten of ten new synthetic development controls versus five for the matched base, and 19/19 known-template regressions (18 normalize to training inputs). Two unsupported input specimens are deferred, not counted as model successes. Field qualification remains false.
- Added Tutorial 9 and its runnable no-model example; 75 software tests pass.

- Added exact-output interpretation review records, with Python/HTTP interfaces, reviewer metadata, criterion hashes and a runnable tutorial.
- Added portable, hash-verified profile packs that reproduce ontology, curriculum and plan IDs without starting training.
- Added independent JSON/schema and decision-field scoring, including rejection of ambiguous duplicate JSON keys.
- Preserved the selected PRS-style brain/weave logo with Vixen-style amber and green diagonal wordmark accents.
- Preserved the failed warning-v2 experiment and its training-fit diagnosis.
- Completed warning-v3-fit: 60 applied updates, 6/6 selected training variants and 2/2 development decisions, versus 1/2 for the matched base. This is a small synthetic diagnostic, not field qualification.
- Completed warning-v4-expanded: 90 applied updates, 7/10 full primary-case matches versus 1/10 for the matched base. Raw robustness is 3/6 for both.
- Added a tested LayerTime temporal-facts adapter. Without further training, the same candidate reached 9/10 primary and 4/6 robustness matches with the extra measured facts; captured-text and provenance failures remain.
- Core/profile tests now total 52 passing checks. These synthetic development results do not qualify a phone installation or product release.

All post-baseline work remains owner-controlled for check-in. Model weights and runtime folders stay local by default. No new candidate has been installed on the phone.

## 0.1 foundation � baseline ceb5916

Initial standalone Notella core, local HTTP API, ontology/curriculum contracts, training job backend, tutorials and the selected evidence checkpoint. The owner executed the check-in; the assistant did not stage, commit or push.

## Local teacher integration in development

- Added an optional loopback-only teacher Python provider and hash-bound, pending-review candidate receipts. Completed requests can be reused; uncertain calls require explicit retry directories. No automatic curriculum admission or training.
- Added Tutorial 10 and a bounded Colibri teacher feasibility protocol. Larger-teacher improvements and student-size benefits remain unproven. Core/provider tests: 81 passing.
- Completed the first local 35B teacher diagnostic: 5/10 decisions, 10/10 schema compliance, all five wrong decisions rejected by evidence checks; first free-form draft rejected. Preserved exact outputs, intake hashes, review and timing. No data admitted or new student trained.

## Teacher review and smaller-student diagnostics

- Added hash-bound pending-teacher reviews with explicit criterion coverage, reviewer assertions, and separate review versus training-permission states. All 84 software tests pass.
- Completed three constrained teacher contrasts: six correct decision labels, reviewed by an agent and explicitly admitted only to a documented development experiment.
- Trained two fresh 0.6B adapters: 90 applied updates each, no skipped updates, 112 finite tensors each. Direct training matched 8/8 new known-pattern controls and 10/10 historical controls; teacher augmentation matched 6/8 and 8/10. Preserved the negative augmentation result, exact outputs, data/source receipts and added-example/sampling limitations. No model was exported to or installed on a phone.

## Semantic Ontology Morphology direction

- Documented the ontology as the representation of the semantic model, with the trainer responsible for defining that model and its ontology before generating teaching examples.
- Defined intended node-edge reasoning, evidence/match units, typed and supported relationships, and morphology as episode-state/support/interpretation change over time.
- Added the intended Colibri workflow for proposing controlled scenario episodes and branches, with prospective criteria, reviews, explicit admission and episode-family evaluation boundaries.
- Updated the main tutorial, concepts, curriculum guidance, architecture and learning path. Episode-level training/state validation remains planned; historical experiments are preserved as single-observation development evidence.

## Episode foundation

- Implemented the first reusable Python episode/state contract with arrival-time visibility, origin/report counts, typed edges, interval-aware precedence, retained/retracted graph history and explicit correction links.
- Added family/shared-prefix checks and full-prefix curriculum export that excludes authored prior/future targets from inputs. Export grants no admission.
- Added a proposed network semantic model, explicit rule comparator, seven unadmitted teaching branches, 20 reference states and 11 distinct visible prefixes in one original family.
- Added Tutorial 11 and updated implementation-status guidance. All 104 software tests pass. No episode model has been trained or evaluated, and no phone deployment changed.

## Scenario terminology

- Adopted scenario, scenario instance, scenario family, branch and step as the public vocabulary, with the intended simulation/training meaning documented alongside HELM's broader evaluation usage.
- Added notella.scenarios, scenario-format records and the scenario tutorial/profile while retaining legacy episode APIs, fixtures and historical identities. New ontology version 0.1.2-development records the naming change; reference-policy behavior is unchanged.
- Verified compatibility, unchanged trajectories, future-evidence rejection and read-only treatment of original records. All 108 software tests pass; the scenario tutorial still refuses unreviewed training admission.

## Retraction and repetition investigation checkpoint

- Completed the same-settings v5 rerun: known criticality agreement 13/18 versus prior 11/18, repetition 1/18 versus prior 5/18, but full-state agreement regressed from 4/18 to 1/18. Fresh agreement is 5/6 versus base 6/6. The candidate remains development-only.
- Recorded unresolved root causes, five discriminating hypotheses, the completed saved-interface audit, and the large-teacher/small-student roadmap.
- Preserved runtime documents, training data/records, exact outputs, logs and source snapshots in a hash-verified deduplicated checkpoint archive. Weight/optimizer binaries stay local with a hash inventory.
- Verified 154 core tests and four optional training-loss tests. No phone deployment or notification-delivery qualification occurred.

- Added a self-contained scrollable infographic and static PNG exports documenting the initial approach, Semantic Ontology Morphology direction, failed results, unresolved causes and proposed teacher/student architecture. Desktop/narrow layout and four illustrative interaction states were checked; no new capability is claimed.
