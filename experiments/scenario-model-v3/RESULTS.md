# Scenario model comparison: completed results

## Outcome

The fresh 4B adapter completed 80 applied updates, zero skipped updates, and finite weights. These numerical checks do not establish correct semantic interpretation. The matched development comparison is complete; all ten prompt hashes match between conditions, and evaluator/scorer/curriculum/evaluation identities match.

| Measure | Base | Trained |
| --- | ---: | ---: |
| jsonValid | 6/10 | 8/10 |
| schemaValid | 3/10 | 8/10 |
| contractValid | 0/10 | 2/10 |
| criticalityMatch | 3/10 | 3/10 |
| assessmentEvidenceMatch | 4/10 | 5/10 |
| nodesMatch | 0/10 | 2/10 |
| edgesMatch | 0/10 | 2/10 |
| fullStateMatch | 0/10 | 1/10 |
| tokenLimitReached | 4/10 | 2/10 |

Generation totals: base 1229.6 s; trained 999.2 s. Output lengths differ, so this is not an inference-engine speed benchmark or phone estimate.

A criticality match is measured independently of graph validity. A full state match includes contract, decision, evidence and node/edge agreement; prose truth is not automatically judged. A label in a truncated/unparseable response is not extracted or repaired. The explicit rule reference authored the targets: its self-agreement is not an independent accuracy measurement.

## Morphology: decision revisions

| Measure | Base | Trained |
| --- | ---: | ---: |
| directionMatches | 3/8 | 3/8 |
| endpointMatches | 1/8 | 1/8 |

These are adjacent independently prompted prefix outputs, not rollout using earlier generated state. Direction can match while severity stays consistently wrong. See evidence/revisions.json for every transition.

## Why criticality is being downgraded

Observed: standalone compromise in S-Q71-step-1 is labeled contextual, with an explanation that the evidence does not establish compromise. Step 2 also demands an association with authentication activity. Step 3 becomes critical once all three concepts appear. Step 4 becomes contextual after a scoped benign explanation even while its rationale says the compromise is not negated. Step 5 incorrectly keeps critical after the underlying compromise claim is retracted. S-Q92-step-3 assigns high despite reviewed compromise evidence. These are semantic policy failures as well as graph-contract failures. The last two trained responses repeat their rationale until the token cap, leaving incomplete JSON; they are retained as failures without extracting a provisional label. Training loss was 0.2201 and validation loss 0.2150, illustrating that low token loss did not establish correct decisions.

Verified curriculum gap: 20 training rows contain only 11 normalized distinct visible prefixes from one authored family. Labels are contextual 10, high 7, critical 3. All seven one-observation rows are contextual. All three critical rows contain reconnaissance, credential activity and compromise together. There is no standalone-compromise critical example, no critical compromise that survives an explanation limited to scan/authentication, and no reposted-compromise correction trajectory in training. The ontology instruction does state the correct override and scoped-explanation rules.

Inference, not a proven causal finding: the adapter appears to learn scenario/template shortcuts more strongly than rule precedence. The observed sequence sensitivity and rationale/decision contradictions fit that explanation. Low training loss on repeated structured targets is compatible with memorization and does not resolve it. This run does not isolate data coverage, learning rate, adapter capacity, seed effects or token-loss weighting. Successful updates alone cannot rule every training implementation defect out.

## Changes to make next

1. Keep this adapter as a failed semantic diagnostic, not a deployment candidate. Preserve the current development fixtures and outputs unchanged. Do not turn inspected evaluation answers into targets.
2. Author and review new training families with contrastive controls: compromise alone; compromise before or without scan/authentication; a scoped benign explanation that leaves compromise active; actual source correction that removes compromise; duplicate/repost roots; unrelated assets; occurrence versus receipt order. Change identifiers, assets, order and irrelevant context across families so row length and fixed sequences cannot predict severity.
3. Deduplicate normalized prefixes or explicitly weight their family contribution. Measure coverage of rule precedence and criticality transitions before admission. Mere class balancing cannot fix missing semantics.
4. First rerun with a corrected curriculum while holding base model, rank, learning rate and update budget fixed. This makes the curriculum change assessable. Keep the existing development set as a known diagnostic, and freeze newly authored untouched evaluation families before the next run; do not call reused cases independent evidence.
5. Enforce structural and policy-consistency checks before applying proposed changes at runtime. Reject unsupported downgrades and claims retaining retracted compromise; retain the previous validated incident and mark the new proposal for review. Do not force critical indiscriminately: a valid correction must permit de-escalation.
6. Then test compact delta inputs with relevant baseline context, ontology meanings, provenance and retained incident evidence. Keep full-state checks for audit. Do not mix a new delta representation into the first curriculum-only comparison or claim this run has tested delta inference.

Full-state serialization dominates the target, while severity occupies few tokens. Decision-focused targets or explicit loss weighting are later ablations if curriculum repair is insufficient, not established fixes from this run. More epochs on the same narrow examples is not the first remedy.

## Evidence and limits

Exact outputs and per-prefix scores are preserved under evidence/, with SHA-256 identities in evidence/manifest.json. See BASELINE-REVIEW.md for baseline prose errors and PROTOCOL.md for preserved memory failures/retry. Training uses fresh QLoRA rank 16 on the local Qwen3-4B-Instruct-2507 base. The earlier partial runs are not added to its 80 updates.

Same-author synthetic development, two evaluation families and one training family; no independent field validation, calibrated attack probability, delta-trained inference, phone deployment, thermal/battery qualification or Colibri teacher contribution in this comparison. All artifacts remain releaseEligible=false.
