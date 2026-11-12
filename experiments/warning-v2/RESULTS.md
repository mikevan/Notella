# Warning experiment v2: results

This is a two-case development comparison, not independent test accuracy or field qualification.

| Case | Expected | Base decision | Trained decision |
|---|---|---|---|
| Corroborated local sequence | critical/met | critical/met | high/unconfirmed |
| Unidentified RF signal | high/unconfirmed | critical/met | high/unconfirmed |

Both conditions matched the decision fields on one of two development cases when inspected independently of formatting. The trained model obeyed the output contract on both cases; the base violated length limits on both. The original schema-gated comparator reports base 0/2 and adapted 1/2, and is retained unchanged. This is not evidence of an overall decision-quality improvement.

The trained critical answer falsely stated there was only one visual observer, despite the supplied independent acoustic sensor. The base over-escalated the unknown RF case by treating it as independently corroborated drone presence. The candidate is not accepted or installed.

Training completed 120 applied updates with zero skips and 144 finite tensors. The native prompt hashes, base intake and evaluator source match across conditions. Responses were about 56.9/47.0 seconds for the base and 10.6/14.8 seconds for the adapter; the adapter generated substantially shorter answers, so this does not establish a general runtime speedup.

Review judgments are agent-authored, not independent expert validation. The causation field is constrained to not_established by this task contract; satisfying that invariant alone does not demonstrate learned causal reasoning.

The subsequent training-fit check is diagnostic only and is not part of the frozen development comparison.


## Training-fit diagnostic

The adapter produced exactly the same outputs, byte for byte, on the selected training critical sequence and uncertain-signal example as on their development counterparts. It still invented a single observer on the training critical case. This demonstrates a fit failure on that selected training example, not merely a failure to generalize to its held-out counterpart. It does not identify the cause. More updates alone are not yet justified; the next controlled work should audit target balance, repeated boilerplate versus discriminative labels, and source-count representation before another long run.
