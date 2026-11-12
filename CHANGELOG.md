# Change log

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

## 0.1 foundation — baseline ceb5916

Initial standalone Notella core, local HTTP API, ontology/curriculum contracts, training job backend, tutorials and the selected evidence checkpoint. The owner executed the check-in; the assistant did not stage, commit or push.
