# Retraction and repetition curriculum: completed comparison

The local 4B base, immutable ontology, engine/package hashes, actual training arguments, fresh adapter initialization, 80-update budget and twenty training rows are held fixed. The intervention is a retraction-focused curriculum with short fact-specific rationales and separate change summaries. Full-prefix input, full-state output, greedy generation and the 1536-token output cap remain unchanged.

## Known cases

| Measure | base | previousAdapter | retractionAdapter |
| --- | ---: | ---: | ---: |
| jsonValid | 13/18 | 13/18 | 17/18 |
| schemaValid | 8/18 | 11/18 | 14/18 |
| contractValid | 0/18 | 4/18 | 2/18 |
| criticalityMatch | 7/18 | 11/18 | 13/18 |
| assessmentEvidenceMatch | 8/18 | 10/18 | 7/18 |
| nodesMatch | 0/18 | 7/18 | 5/18 |
| edgesMatch | 0/18 | 5/18 | 2/18 |
| fullStateMatch | 0/18 | 4/18 | 1/18 |
| tokenLimitReached | 5/18 | 5/18 | 1/18 |
| repetitive narrative heuristic | 0/18 | 5/18 | 1/18 |

## Fresh cases

| Measure | base | retractionAdapter |
| --- | ---: | ---: |
| jsonValid | 6/6 | 6/6 |
| schemaValid | 4/6 | 5/6 |
| contractValid | 0/6 | 2/6 |
| criticalityMatch | 6/6 | 5/6 |
| assessmentEvidenceMatch | 3/6 | 3/6 |
| nodesMatch | 0/6 | 2/6 |
| edgesMatch | 0/6 | 2/6 |
| fullStateMatch | 0/6 | 2/6 |
| tokenLimitReached | 0/6 | 0/6 |
| repetitive narrative heuristic | 0/6 | 0/6 |

## Criticality detail

| Group / condition | Critical correct | Critical downgraded | Critical unreadable | Contextual falsely critical |
| --- | ---: | ---: | ---: | ---: |
| known / base | 4 | 4 | 2 | 2 |
| known / previousAdapter | 8 | 0 | 2 | 2 |
| known / retractionAdapter | 9 | 1 | 0 | 3 |
| fresh / base | 4 | 0 | 0 | 0 |
| fresh / retractionAdapter | 4 | 0 | 0 | 1 |

## Interpretation boundaries

All eighteen v4 evaluation prefixes are now inspected, known diagnostics. Six fresh prefixes were frozen before training but share the same author and proposed rule reference; neither group is independent field validation. Known base outputs were reused only after exact prompt and score checks; six fresh base outputs and all twenty-four candidate outputs were generated. No previous-adapter generation was run on the new fresh cases.

Repetition is a fixed diagnostic on rationale/summary prose, including incomplete quoted prose: at least 36 words, a repeated 12-word window appearing at least three times, and duplicate-window fraction at least 0.25. It excludes repeated graph fields and is not a semantic correctness measure. Thresholds were fixed before candidate generation. Exact outputs, heuristic details and per-case scores are preserved.

No generated output was repaired, dropped or admitted to training. Incomplete output remains unreadable, never clearance. More output tokens and warning-continuity retries were not introduced into this matched comparison. Runtime safeguards remain separate, and no phone deployment or alert-delivery guarantee is demonstrated.

See PROTOCOL.md and review.json for curriculum, scope and provenance. The generic ontology currently declares correction edges for compromise evidence only; credential-retraction authoring drafts failed validation and were revised before admission, without changing the ontology.
