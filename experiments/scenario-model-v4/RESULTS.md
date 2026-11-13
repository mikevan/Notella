# Curriculum repair: completed comparison

Same base model, ontology, engine, LoRA/optimizer settings, 80-update budget and 20 training rows. The curriculum and its repeated-prefix exposure changed; it now has 20 unique prefixes rather than 11. All exact known prompts match, and fresh-case prompts match between base and repaired adapter.

## Known diagnostics: inspected before curriculum repair

| Metric | Base | Previous adapter | Repaired adapter |
| --- | ---: | ---: | ---: |
| jsonValid | 6/10 | 8/10 | 6/10 |
| schemaValid | 3/10 | 8/10 | 5/10 |
| contractValid | 0/10 | 2/10 | 2/10 |
| criticalityMatch | 3/10 | 3/10 | 6/10 |
| assessmentEvidenceMatch | 4/10 | 5/10 | 5/10 |
| nodesMatch | 0/10 | 2/10 | 4/10 |
| edgesMatch | 0/10 | 2/10 | 3/10 |
| fullStateMatch | 0/10 | 1/10 | 2/10 |
| tokenLimitReached | 4/10 | 2/10 | 4/10 |

## Fresh synthetic evaluation: frozen before training

| Metric | Base | Repaired adapter |
| --- | ---: | ---: |
| jsonValid | 7/8 | 7/8 |
| schemaValid | 5/8 | 6/8 |
| contractValid | 0/8 | 2/8 |
| criticalityMatch | 4/8 | 5/8 |
| assessmentEvidenceMatch | 4/8 | 5/8 |
| nodesMatch | 0/8 | 3/8 |
| edgesMatch | 0/8 | 2/8 |
| fullStateMatch | 0/8 | 2/8 |
| tokenLimitReached | 1/8 | 1/8 |

Known cases are reused diagnostics, not independent evidence. Fresh cases share author, semantic motifs and rule reference with training, so are synthetic development controls, not field validation. No previous adapter generation was run on fresh cases. Schema/contract agreement and loss do not establish complete semantic correctness. Exact explanations still require inspection.

The untrained base outputs for the ten unchanged known cases were reused after exact prompt and score verification; eight fresh baseline cases were generated. The repaired adapter generated all eighteen responses. No generated evaluation output was repaired, admitted to training, or excluded. Token-capped incomplete responses remain failures.

See PROTOCOL.md, review.json and evidence/ for provenance. No Colibri, phone, delta-trained inference, independent expert validation or calibrated attack probability is demonstrated. No automatic field deployment follows from this experiment.

## Criticality failure detail

| Group / condition | Critical correct | Critical to contextual | Critical to high | Critical unreadable | Contextual to critical |
| --- | ---: | ---: | ---: | ---: | ---: |
| known / base | 1 | 0 | 3 | 2 | 0 |
| known / previousAdapter | 1 | 3 | 1 | 1 | 1 |
| known / repairedAdapter | 4 | 0 | 0 | 2 | 0 |
| fresh / base | 3 | 1 | 0 | 0 | 2 |
| fresh / repairedAdapter | 4 | 0 | 0 | 0 | 2 |

## Assessment revisions

| Group / condition | Correct direction | Correct endpoints |
| --- | ---: | ---: |
| known / base | 3/8 | 1/8 |
| known / adapted | 4/8 | 4/8 |
| fresh / base | 2/6 | 2/6 |
| fresh / adapted | 4/6 | 3/6 |

The previous adapter scored 3/8 direction and 1/8 endpoint matches on known diagnostics. These revisions are reconstructed from independently prompted prefixes, not rollout from prior generated state. Direction agreement alone can conceal wrong severity.

## Output limits and warning continuity

The 1536-token output limit remained unchanged throughout both conditions. A separate tokenizer check found all eighteen valid reference answers fit within 857 tokens; the two early capped repaired responses correspond to reference lengths 856 and 512. Observed repetitive/incomplete responses are not merely reference graphs exceeding the allowance. Capped output remains unreadable for scoring; a partial initial label is not accepted or silently repaired.

The owner requires that output budgets must not silently suppress operational warnings. Separate runtime tooling now provides configurable bounded retries, retained validated assessments and focused incidents, and a warning-state callback before generation. See [Tutorial 16](../../docs/warning-continuity.md). The frozen comparison does not use those new policies. Their simulated-backend tests are not phone deployment, notification delivery validation, or evidence that a model can reliably detect an assault.
