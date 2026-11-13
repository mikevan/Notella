# Provisional review of baseline reasoning

These notes inspect exact preserved development outputs, not independent validation. They do not change targets, scores or the running experiment. The adapted condition has not yet completed, so no training benefit is claimed.

- `S-Q71-step-2`: the model replaces the standalone reviewed-compromise criticality rule with an invented scan/compromise high-criticality rule. This is a substantive policy error, not merely malformed JSON.
- `S-Q71-step-3`: the prose contradicts the supplied times, at one point claiming the 10000 ms compromise precedes the 9000 ms scan. It also states that reviewed compromise warrants critical and nevertheless outputs high. Correctly naming concepts does not establish semantic understanding.
- `S-Q71-step-4`: the model recognizes that the benign explanation covers scan/credential activity but does not invalidate the standalone compromise. It still outputs high rather than the expected critical, and its change citations omit the newly available benign report. Recognition and decision consistency must be assessed separately.
- `S-Q71-step-5`: generation reaches the frozen 1536-token cap and ends inside JSON. Preserve this failure; do not repair the output or increase the cap mid-comparison.
- `S-Q92-step-2`: the decision correctly stays contextual when reconnaissance concerns another asset. The graph still fails endpoint validation. This is evidence for reporting decision and graph measures separately, not calling every graph failure a wrong criticality.

The source is `runtime/scenario-model-v3/base-generation.jsonl`. Exact output, hashes, cutoff, prompt hash, token counts and scores are preserved there. `summarize.py` reads aggregate progress; `audit_revisions.py` reports expected versus generated escalation/de-escalation across adjacent prefixes, including unreadable outputs. Direction agreement alone can hide consistently wrong severity, so endpoint agreement is also reported. These are independently prompted reconstructions, not sequential rollout from a model's earlier answer.
