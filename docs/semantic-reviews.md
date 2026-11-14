# Tutorial 5: record interpretation reviews against exact outputs

Trust requires a visible distinction between a proposed interpretation and one supported by reviewed evidence. Review records make that distinction inspectable while preserving disagreement and uncertainty.

**Outcome:** preserve who judged a generated answer, the criteria they applied, their reasons and the exact output text. This records a review; it does not turn a judgment into independent proof of model accuracy.

## Why structure checks are insufficient

The initial warning model returned valid JSON while missing the supplied critical-warning trigger. A JSON schema can require a posture field, but it cannot establish that critical or high is justified by the observations. Exact answer matching is also insufficient: correct paraphrases can differ, and repeated generic text can preserve the wrong interpretation.

Interpretation reviews therefore need a separate record tied to the exact prompt, output and criteria. Notella now provides this in the Python API and authenticated HTTP API.

## Run the demonstration

From C:\workspace\Notella:

```powershell
python -m examples.review_tutorial --store runtime/review-tutorial
```

Expect a review ID, output hash, allCriteriaPassed=true, fixtureOnly=true and automaticallyMeasuredSemanticAccuracy=false. The demonstration uses the authored temperature reference as an explicit fixture. It does not load a model and is not a measurement of model quality.

## Review a real output

Obtain the exact decoded model text without normalizing whitespace or editing its explanation. Keep the example ID and held-out split. Write criteria before reading the answers where possible, then record a judgment and rationale for every criterion:

```python
from notella.semantic_reviews import record_review

review = record_review(
    api,
    curriculum_id,
    example_id,
    exact_generated_text,
    reviewer={'name': 'Actual reviewer name', 'kind': 'human', 'independent': False},
    criteria=[
        {'id': 'policy-comparison', 'description': 'Correctly applies the supplied warning policy.'},
        {'id': 'causal-limit', 'description': 'Separates warning urgency from causal certainty.'},
    ],
    judgments=[
        {'criterionId': 'policy-comparison', 'status': 'fail', 'rationale': 'Describe the specific contradiction in this output.'},
        {'criterionId': 'causal-limit', 'status': 'pass', 'rationale': 'Identify the exact supported limit stated by the answer.'},
    ],
    split='validation',
)
```

Replace the illustrative judgments with an actual review. Reviewer kind is human or agent; independent is a recorded assertion, not something the API can verify. Do not mark a reviewer independent merely because the output was evaluated in a separate process.

## Interpret the record

The stored evaluation has formatVersion=notella.interpretation-review.v1. It includes curriculum/example IDs, the compiled prompt hash, exact output and its SHA-256, criterion definitions and their hash, reviewer metadata, judgments, structural validity and limitations. allCriteriaPassed is true only when every explicit judgment is pass. not_assessed is distinct from pass or fail.

Changing even output whitespace creates a different output hash and review artifact. Changing a criterion or rationale creates a different review artifact. This helps preserve the chain of evidence, although it does not prove the review is correct or signed by the named person.

Missing criterion judgments, duplicate or unknown criteria, wrong-split example IDs and attempts to review training examples are rejected. Invalid JSON output can still be reviewed and preserved, with schemaValid=false; failed generations should not disappear from the record.

## Use the HTTP client

```python
review = client.record_review(
    curriculum_id, example_id, exact_generated_text,
    reviewer, criteria, judgments, split='validation',
)
stored = client.get('interpretation-reviews', review['id'])
```

POST /v1/interpretation-reviews accepts curriculumId, exampleId, output (the original text string), reviewer, criteria, judgments and optional split (default validation). GET /v1/interpretation-reviews/{id} retrieves only this review type. The same artifact is also retrievable from evaluations/{id}. Both routes require the normal bearer token. The generated OpenAPI description includes the request structure.

## What the record does not establish

It does not automatically determine semantic truth, verify reviewer expertise/identity, certify independence, estimate field accuracy or authorize release. A single reviewer can be wrong. Selected synthetic cases cannot establish population performance. Use independent review and prospectively designed evaluations for stronger claims.
