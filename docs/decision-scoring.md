[Tutorial index](index.md) · [Tutorial 0: environment setup](setup.md)

# Tutorial 7: separate decision agreement from formatting

A plausible answer is not enough when someone may act on a warning. Separate semantic correctness from formatting so failures remain visible and improvements reflect understanding rather than cleaner JSON.

**Outcome:** score an exact generated JSON answer against declared decision fields without hiding a correct decision behind a formatting failure—or mistaking valid JSON for a correct decision.

The warning-v2 comparator required schema validity before checking decision fields. Its original results remain preserved, but that combined score could not show whether a verbose answer had selected the right posture. This helper makes the two checks explicit for future analysis.

## 1. Declare the contract and the fields before scoring

```python
from notella.scoring import score_output

schema = {
    'type': 'object',
    'properties': {
        'posture': {'type': 'string', 'enum': ['critical', 'high']},
        'reason': {'type': 'string', 'maxLength': 20},
    },
    'required': ['posture', 'reason'],
    'additionalProperties': False,
}
target = {'posture': 'critical', 'reason': 'Supplied trigger met'}
fields = ['posture']
```

The target must satisfy its own schema. Fields must be a nonempty, unique list of keys present in the target. Unknown or duplicate field names are rejected rather than silently omitted.

## 2. Score a correct decision with an overlong explanation

```python
output = '{"posture":"critical","reason":"This explanation is longer than twenty characters."}'
result = score_output(output, target, schema, fields)
print(result)
```

Expect jsonValid=true, schemaValid=false, decisionFieldsMatch=true and schemaAndDecisionMatch=false. The posture agrees, but the output is not contract-compliant. Do not discard either finding or relax the length limit after seeing the answer.

## 3. Score a well-formed but wrong decision

```python
output = '{"posture":"high","reason":"Uncertain"}'
result = score_output(output, target, schema, fields)
```

Expect schemaValid=true and decisionFieldsMatch=false. The answer can be consumed by an application, but it does not match the declared decision target.

## 4. Handle malformed output

```python
result = score_output('not JSON', target, schema, fields)
```

Expect jsonValid=false, with no decision pass. Duplicate JSON keys are rejected as ambiguous rather than selecting the first or last favorable value. Nonfinite JSON numeric values are also rejected.

The original output string is not edited or repaired. Retain it and its hash in the generation receipt, including failed outputs. An evaluator should never quietly rewrite an answer into passing form.

## 5. Interpret the result

| Field | What it establishes |
|---|---|
| jsonValid | The text parses as unambiguous supported JSON |
| schemaValid | The parsed output satisfies the declared structural contract |
| fieldMatches | Exact canonical value agreement for each declared field |
| decisionFieldsMatch | All declared decision fields agree |
| schemaAndDecisionMatch | Both schema and declared decision checks pass |
| semanticAccuracyMeasured | Always false; this is not a general semantic judge |

Field agreement is useful when the target is a reviewed policy label. It is not proof that the policy itself is valid or that a model's explanation is grounded. Use the separate [interpretation-review record](semantic-reviews.md) for justified judgments about exact outputs.

In the expanded warning experiment, posture, combinedTrigger and evidenceClass are all scored. The proposed policy, synthetic labels, family relationships and replay counts remain explicit. Development agreement must not be reported as independent field accuracy.

---

[Previous: Tutorial 6 — Package a reproducible profile](portable-profiles.md) · [Next: Tutorial 8 — Supply measured temporal facts](temporal-features.md)
