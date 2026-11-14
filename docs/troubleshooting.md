# Troubleshooting by symptom

A failed development component must remain distinguishable from a successful assessment. Use these checks to diagnose the workflow without erasing evidence or interpreting missing output as safety.

## “No module named notella”

Run from C:\workspace\Notella, or install the core into the intended environment with `python -m pip install -e C:\workspace\Notella`. Check which Python executable your application is using. The API interpreter and training interpreter can differ; configure --python explicitly for training.

## The server rejects its token or will not start

Set NOTELLA_API_TOKEN to a nonempty secret of at least 24 characters in the server environment. The client must use exactly the same value in `Authorization: Bearer ...`. A token generated in one terminal is not automatically available in another. GET /health working does not verify authentication because health is deliberately public.

## “Family crosses splits” or “Input crosses splits”

Inspect the original scenario/source family, not only the row IDs. Keep variants together. Do not repair a meaningful leakage failure merely by changing IDs or adding irrelevant characters to the input. Redesign the split or collect an independent scenario. The prototype's rejected dataset builds are preserved as evidence of earlier exact-overlap detection.

## “Source not admitted for training”

Verify source.reference, permission, labelAuthor and trainingAllowed. A permission string should state the actual authority, not just “public.” Review external licences and private-data permissions before admission. If material is held out for evaluation, keep it held out instead of changing its admission solely to satisfy the compiler.

## “Unsupported output schema”

The validator supports a bounded subset, not every JSON Schema feature. Remove unsupported constructs only if the resulting contract still expresses your intent; otherwise extend the validator with tests or supply an appropriate alternative backend. Do not silently drop an important condition. See [supported keywords](api-reference.md).

## “Artifact integrity failed”

Content-addressed files are immutable. Editing one in place changes its hash. Preserve the corrupted file for investigation, restore it from a verified copy if available, or register the corrected content as a new artifact. Renaming a changed file to its old ID does not make it valid.

## Training backend or model is not configured

Creating a plan is allowed before a model is configured. Starting a job requires --engine, a compatible --python and a matching --model alias=directory mapping on the server. The API body supplies only the alias. Check that the directory exists and contains complete local weights and tokenizer files.

## The GPU lock is held

Check store/jobs/gpu.lock and the referenced job's state, process and logs. Another server or application may also be using the GPU independently. Keep one server per store. After a crash, the child can still be running; the lock is not automatically stale. Only recover manually after establishing whether the exact training process remains active and preserving its evidence.

## CUDA unavailable or out of memory

Check the training interpreter's torch installation and CUDA availability. The tested environment has an 8-GiB RTX 2070 and uses the CPU-frozen-layer option to reduce GPU demand. Other GPUs, drivers or model architectures can behave differently. Preserve the failure log. Do not run another model on the same GPU while diagnosing memory pressure.

The API currently exposes steps, rank and learning rate, but not every memory-related engine argument. A different backend/configuration may be needed for larger contexts or architectures. There is no automatic CPU-training fallback.

## An example exceeds the context budget

The engine intentionally fails instead of truncating answers. Shorten evidence pages while preserving meaningful relationships and provenance, or explicitly change the validated backend configuration. Do not delete uncertainty or counterevidence merely to fit a token limit. Changing prompt representation creates a new experiment and requires evaluation.

## Training completed but the answer is wrong

Inspect the exact prompt and output, not just loss or JSON validity. Compare the failed case with training contrasts. Look for conflicting instructions, repeated generic answers, insufficient positive examples, hidden metadata shortcuts, prompt mismatch and inadequate base-model capacity. Preserve failed answers and use development data to select a repair experiment.

The initial camp run provides a concrete example: the model returned valid JSON but declined the critical combined warning even though the supplied observations met the proposed policy. That is a behavioral failure, not a transport failure. Do not redefine success as valid JSON or quietly weaken the intended trigger.

## The evaluation reports zero exact matches for sensible answers

ExactTargetMatch compares canonical JSON values, including text strings. Correct paraphrases can differ. Review them against predeclared semantic criteria. Conversely, a schema pass can accompany a false interpretation. The public evaluator intentionally reports semanticAccuracyMeasured=false.

## Where to collect an issue report

Include the Notella version, artifact IDs, ontology and curriculum versions, job ID, relevant logs, runtime/package manifest, applied-update and weight-integrity summaries, and exact generated output hashes. Remove tokens, private observations and model weights from a public report. Describe the observed failure and expected interpretation with a minimal reproducible example.
