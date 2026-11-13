# Constrained teacher v2 results

Three prospectively frozen single-factor contrasts completed: six of six decisions matched the author-specified references, all three outer JSON formats passed, all six decisions passed evidence guards, and all responses ended with stop rather than truncation. Pair times were 98.203, 88.235 and 88.359 seconds (274.797 seconds total).

The conditions covered disruption identity, drone-report source lineage and signal identity. The exact candidates and requests are retained under receipts/. They were reviewed against the earlier prospectively recorded v1 criteria; agent-reviews.json stores the exact hash-bound reviews, with kind=agent and independent=false. Case-2 wording about unconfirmed independence is limited to the trigger's asserted source topology, not statistical certification. Review is not independently verified field truth.

The narrower instruction and output shape changed alongside the case set, so this is not a matched demonstration that prompting alone fixed the earlier failures. These are known synthetic policy patterns with new numeric inputs; zero exact overlap with the v6 examples does not establish independent generalization. The original ten-case diagnostic has not been rerun under this prompt.

After explicit agent review, six decision labels were admitted solely to the bounded 0.6B augmentation diagnostic. Review records themselves grant no training permission. The separate admission is recorded in runtime/student-v1-teacher-augmentation/explicit-admission.json and preserves candidate/review references. Rationales were not used as student optimizer targets. No previously generated acceptance output or v6 validation reference was used as a teacher training label.

Colibri was stopped before student training. No teacher weights were updated, no pruning was performed, and no phone model was changed. See ../student-v1-teacher-augmentation/PROTOCOL.md for the small-student comparison and its added-example/sampling confounds.
