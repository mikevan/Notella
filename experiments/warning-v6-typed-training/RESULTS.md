# Typed semantic decision training v6 — results

The newly trained adapter meets all three declared output fields on all ten new development controls, compared with five for the matched base. All generated adapter answers also pass the declared output/evidence checks. This is a small synthetic development result, not independent field accuracy.

| Evaluation role | Base correct | New adapter correct |
|---|---:|---:|
| New development controls; exact input overlap with training = 0 | 5/10 | 10/10 |
| Historical known-template regressions | 12/19 | 19/19 |

Two additional specimens (unknown source lineage and uncertainty straddling the window boundary) are deferred before generation in both conditions. They are not model passes or negative threat findings.

## What changed

The model is now trained and evaluated on the same typed decision view. Irrelevant captured text and raw free-form context are retained in original artifacts but excluded from this task. Context comes from trusted owner configuration. Source aliases resolve through explicit authored provenance roots rather than label wording. Time relations are calculated with uncertainty and the supplied clock assumption. Ten allowed output states bind evidence class, trigger and posture. Necessary evidence checks reject contradictory answers without repair.

This is a pipeline containing learned and deterministic parts. The model does not discover source authentication, verify sensors or calculate an attack probability. For simple fully structured policy rules, code can compute/validate decisions directly; the SLM must not be the sole authority for those rules.

## Data and training

The 45 optimizer rows comprise 30 authored source variants and 15 explicit replays, balanced across the three posture labels. They normalize to 24 distinct model inputs. The new ten development controls vary timing/window values, clock alignment, source cardinality and lineage topology. Exact cross-split overlap is zero, but they share underlying synthetic pattern templates and are not independently reviewed incidents.

Training completed 90 applied updates, zero skips, two passes and 144 finite saved adapter tensors. Recorded optimizer training time was 150.07 seconds; setup, generation and other checks are separate. The base and adapter receive identical prompts and decoding settings. The adapter is fresh from the same pinned base; no inspected test outputs or old validation labels enter optimizer input.

## Why old regressions are not validation

Normalization removes clock-origin and source-alias differences. 18 of the 19 historical model inputs exactly equal normalized training inputs. Their 19/19 outcome is useful for detecting breakage and boundary invariance, not a generalization score. The narrowed-window case remains a prior inspected development probe, not a fresh acceptance test.

Clean uncertain-signal input and the two new captured-payload variants have identical rendered prompts and outputs in this condition. This is input isolation, not learned immunity to arbitrary adversarial text. Alias equivalence also comes from the supplied registry; do not attribute it solely to weight learning.

## Output checks and remaining limits

On this selected cohort, checks reject observed wrong base outputs without accepting a wrong answer, and do not reject a correct adapter answer. This does not prove the checker will catch every future wrong answer. Rejection never changes a generated value or supplies a replacement posture. The included registry is a synthetic assertion set, not an authentication system; a production caller must bind trusted collector identities to reviewed provenance.

The adapter produces compact decision slots, not independently grounded free-text explanations. Unknown kinds/areas and unsupported evidence states require review. A broader independent evaluation, domain review, operational policy calibration, job lifecycle hardening and device qualification remain unfinished. No model is installed on the phone and releaseEligible remains false.

## Reproduction

profile.json pins the ontology and typed example files. sampling-audit.json records raw/replay/projected counts and overlap. projection-receipts.json and source-registry.json preserve the normalization evidence. prepare.py rebuilds the pack only before launch; launched experiments must be preserved. run.py performs training plus the matched new-control comparison. run_regressions.py separately labels the historical fixtures and deferrals. Runtime results remain local under runtime/warning-v6-typed-training and runtime/warning-v6-typed-regressions.
