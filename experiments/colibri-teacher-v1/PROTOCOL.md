# Colibri teacher v1: connection and feasibility protocol

## Objective

Establish whether a larger, untuned local teacher can draft usable ontology-scoped material on the current workstation. This is a prerequisite to the student-size experiment, not evidence that distillation improves a phone model.

## Frozen starting point

Notella source baseline: 567c6c3052b40bc71261d4f08e5ee1304646b0e6. Existing typed 4B adapter remains unchanged. Its ten synthetic development controls are 10/10 decision matches versus 5/10 for its matched base. Those controls are already inspected development evidence, not an independent acceptance set.

Teacher: Qwen3.6-35B-A3B, preconverted int4-gs64 container Kreuzzelg/qwen36-35b-a3b-colibri-i4-gs64, pinned revision c619aa594ad1e70af82168fb6b4878427896e21c. Verify downloaded bytes against the pinned listing before inference. Record the engine binary digest and source/provider hashes with the run. This is pretrained teacher inference, not teacher fine-tuning.

Hardware observed: Intel i7-9700K, about 31.9 GiB RAM, NVIDIA RTX 2070 8 GB. Colibri's prebuilt CUDA engine requires compute capability 8.0+, so this compute-7.5 card uses Vulkan. Other applications remain running. Bound initial context and memory use; do not kill other apps or assume all RAM/VRAM is available.

## Run order

1. Complete and verify the teacher intake.
2. Start one loopback-only server on port 8877 with explicit model ID and bounded memory/context. Capture its startup log and serving settings.
3. Run examples/teacher_tutorial.py against that server. Preserve the exact pending candidate, finish reason, latency and request/result hashes. Check for incomplete or malformed output before interpretation review.
4. Inspect the candidate for policy fidelity, source-lineage distinctions, causal overclaiming and internal contradictions. Record an agent review explicitly as agent-authored and not independent field verification. No automatic admission.
5. Use the existing ten controls for a compatibility diagnostic through experiments/notella-pilot/compare_teacher.py in the Colibri source tree. Record JSON/schema compliance, decision-field agreement, evidence-guard checks, errors and elapsed request time separately. Invalid/rejected replies are not successes.
6. Stop the temporary teacher server after the bounded diagnostic unless more work immediately requires it.

## Next gate: smaller student experiment

Before admitting a teacher corpus, freeze a separately reviewed prospective evaluation set outside teacher-generation inputs. Separate scenario families and preserve rejected drafts. A credible independent evaluation requires another reviewer or source; examples authored and checked by the same agent are not independent.

Compare the same small student with direct ontology-guided teaching versus additional reviewed teacher-generated material, using matched training settings. Preserve source permissions, provenance and example lineage. Report each critical miss and false alarm, not only aggregate matches. Record total teacher generation, review and training time. Existing 4B results are a reference, not a matched architectural control.

Quantization and actual phone latency/memory/sustained thermal/battery measurements follow only for promising students. Logit-level distillation, structural pruning, teacher training and Android Colibri support are outside v1. No deployment, release qualification, speedup or smaller-model success is implied by a working teacher connection.
