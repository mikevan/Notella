# Interpretation of the curriculum-only rerun

The repaired curriculum improves some policy decisions, but the adapter is not operationally reliable. See RESULTS.md and exact evidence/ outputs. Same model/base intake, training engine/packages/arguments, rank, learning rate, seed, batch/accumulation, 80 applied updates and twenty training rows were verified. No initial adapter continuation occurred. The data intervention replaces repeated narrow prefixes with twenty unique contrasts and changes the class/exposure mix; this single run does not isolate which data feature caused each effect.

## What improved

Known-case criticality agreement increases from 3/10 for the previous adapter to 6/10. All four early S-Q71 compromise states now remain critical, including standalone compromise and the scoped benign explanation that does not invalidate compromise. The previous adapter falsely called three of those states contextual. The first repaired state fully matches the reference, rather than merely naming the right concept.

On the fresh cases, the repaired adapter matches all four expected-critical decisions, versus three for the untrained base. In particular V-947-step-3 retains critical despite an explanation covering only reconnaissance. V-947-step-1 and step-2 fully match their reference states; the baseline gets their labels right but fails their graph contracts. Fresh overall decision agreement is 5/8 versus base 4/8. The previous adapter was not evaluated on fresh cases.

## What remains wrong

The fresh contextual cases expose the remaining weakness: only one of four is correctly contextual. Two remain falsely critical after primary-asset support is withdrawn; one ends in incomplete JSON. V-834-step-3 cites the source correction u7 while claiming current primary-asset compromise remains. This is a meaning/provenance error, not a token limit. Full-prefix generation still confuses historical presence with current support, particularly when scope and correction interact.

There are five capped/incomplete repaired outputs across eighteen prefixes: four on known cases, one fresh. The known-group rate worsens from 2/10 in the prior adapter to 4/10. Several responses repeat generic compromise/explanation/correction sentences. Known schema validity also falls from 8/10 to 5/10. Do not hide these regressions behind the improved labels. Every reference answer fits within 857 tokens; increasing output capacity alone cannot establish correct semantics. Partial initial labels are not accepted as answers.

Criticality revisions improve on known cases from 3/8 direction and 1/8 endpoint matches to 4/8 and 4/8. Fresh direction/endpoint matches improve from base 2/6 and 2/6 to repaired 4/6 and 3/6. Stable wrong severity can give a correct direction, so both measures remain necessary. No sequential rollout or continuous phone inference was tested.

## Next implementation target

The results are consistent with learning the sufficient-compromise and scoped-explanation rules better, while retirement of support remains unreliable. They do not prove a particular neural reasoning mechanism or data-shortcut cause. Do not promote this adapter or respond by merely increasing epochs or unlimited output.

Keep the agreed division of responsibilities: the application maintains evidence identity, event/receipt time, duplicates, active/retracted support and incident history. Next test explicit current node/edge state and its semantic delta as model input, with a compact assessment/citation output. Teach interpretation of retired versus active support, with contrastive multi-asset correction cases authored separately from these now-inspected evaluations. Keep optional explanation generation separate from the warning record. That representation/output change is a new experiment; it was not silently introduced into this curriculum-only run.

The separate warning-continuity tooling preserves validated incident state and evidence, surfaces incomplete assessment explicitly, exposes warning state before calling the backend and permits bounded larger-output retries. It requires current-evidence validation and an application delivery path. Its simulated-backend tests do not establish real model-provider integration, phone notification delivery or attack-detection reliability. Output exhaustion must never be interpreted as clearance.

All data are same-author synthetic development controls, not independent field evidence. Artifacts remain releaseEligible=false. Exact model outputs are retained without repair, exclusion, or admission back into training.
