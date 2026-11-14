[Tutorial index](index.md) · [Tutorial 0: environment setup](setup.md)

# Tutorial 10: use a local teacher without admitting its answers

A teaching model can propose useful material, but it cannot certify its own truth. Reviewable proposals and explicit admission decisions protect the learning process from unsupported claims entering the corpus.

The trainer defines the semantic model and represents it as an ontology first. Colibri's intended role is to host a model that proposes new scenarios and branches demonstrating how that model changes over time. See [the scenario-authoring plan](scenario-authoring.md) and [Semantic Ontology Morphology](semantic-ontology-morphology.md). This runnable tutorial covers the current candidate/review plumbing; multi-step scenario generation and validation are not implemented by it.

This optional Python API connects to a local Colibri/OpenAI-compatible server. It drafts candidate material, not a curriculum or a training job. It adds no package dependencies. No HTTP routes have been added to Notella's server.

## Start with a known server and model

Use a running teacher on loopback and obtain its exact model ID from its `/v1/models` endpoint. This example expects an unauthenticated local server on port 8000. For an authenticated server pass `token=` when constructing `LocalTeacher`; the bearer token is never included in saved requests. Do not place secrets in prompt text: prompts and responses are saved locally.

```powershell
$python = 'C:\workspace\TUltra-Project\LayerTime\tools\ai-training\.venv\Scripts\python.exe'
Invoke-RestMethod http://127.0.0.1:8000/v1/models
& $python C:\workspace\Notella\examples\teacher_tutorial.py --model YOUR_SERVED_MODEL_ID --output C:\workspace\Notella\runtime\teacher-draft-001
```

The LayerTime example hashes its actual ontology file, selects named concepts and asks for two contrasting synthetic scenarios. It does not read evaluation examples or expected evaluation answers. The ontology includes the proposed policy, which is a teaching specification, not an independently validated threat model.

Expected summary: `reviewStatus` is `pending` and `admittedForTraining` is `false`. Read `request.json` and `result.json` in the output directory. The latter preserves the exact response body, parsed content, server-reported model ID, finish reason and elapsed request time. A length-limited answer can be incomplete: inspect `finishReason` before review.

## Reusable Python interface

```python
from notella.teachers import LocalTeacher, teaching_candidate
provider = LocalTeacher('YOUR_SERVED_MODEL_ID', timeout=300)
result = teaching_candidate(
    provider,
    ontology_id='YOUR_VERIFIED_ONTOLOGY_ID',
    concept_refs=['YOUR_CONCEPT_ID'],
    messages=[{'role':'user','content':'YOUR_ONTOLOGY_SCOPED_TASK'}],
    directory='runtime/my-teaching-request',
    max_tokens=384,
)
```

The generic interface records caller-supplied ontology/concept references. It does not resolve them or verify their meaning. The tutorial explicitly resolves the selected concepts from the ontology. Model names and server replies are identity assertions, not cryptographic weight receipts; add verified model-file hashes to the experiment intake before claiming reproducibility.

## Restarts and failures

Rerunning an identical completed request returns the saved result without calling the model. A different request in the same directory is refused. A timeout, interrupted call or incomplete directory is refused on restart: inspect the files and use a new directory for an explicit retry. This avoids silently repeating uncertain execution; it is not an exactly-once guarantee. A failed call records error type/message where possible. Keep the local error text private if it contains sensitive diagnostics. Redirects and environment proxies are disabled; remote endpoints are refused. The local server itself must also be configured not to forward prompts elsewhere.

## Review before training

Review physical plausibility, ontology coverage, counterevidence, provenance assumptions, contradictions and ambiguous cases. Record who reviewed a candidate and preserve rejected outputs. Admission through the existing curriculum workflow remains a separate action; this API never sets source permissions or starts training. Teacher-generated material and its review do not establish independent field truth.

## Experimental gates

1. Preserve baseline and a separately reviewed evaluation set before new teacher material is admitted.
2. Compare the same student architecture/settings with and without reviewed teacher material.
3. Track missed critical warnings, false alarms and deferrals separately; measure total teacher/review/student time.
4. Quantize and measure promising candidates on an actual phone, including latency, memory, sustained heat and battery use.

No improved accuracy, faster training, smaller phone model or teacher weight-training support has been demonstrated by this connection. Probability-distribution distillation and structural pruning are not implemented.

The first local teacher feasibility [protocol](../experiments/colibri-teacher-v1/PROTOCOL.md) records model intake, hardware, bounded inference and the gate before a smaller-student experiment.

Each new request also records the teacher provider source SHA-256. A provider-source change produces a different request identity. Saved results have an integrity hash checked before reuse; this detects accidental edits but is not a digital signature.

## Reproduce this workstation run

After completing and verifying the public model intake, `C:\workspace\colibri\Start-NotellaTeacher.ps1` starts the bounded local server. It requires the verified receipt and engine hash, and records serve-settings.json. The --vram launcher flag is CUDA-only on this engine; the script uses Vulkan-specific caps instead. The prebuilt engine is recorded by hash and is not claimed to be built from the extracted fork source.

```powershell
& $python C:\workspace\Notella\examples\teacher_tutorial.py --model notella-teacher-qwen36 --base-url http://127.0.0.1:8877/v1 --output C:\workspace\Notella\runtime\teacher-draft-NEW
```

This run is described in the experiment results. Keep the exact draft and its separate review, including rejected answers. Use a new directory for a new or explicitly retried request.

## Record a reusable review of a pending candidate

The separate Python API `notella.teacher_reviews.record_teacher_review` stores a content-addressed review in a Notella artifact store. It verifies the candidate/result hash and exact output hash, requires one reasoned judgment per criterion, and records the reviewer's kind and asserted independence.

```python
import json
from pathlib import Path
from notella import Notella
from notella.teacher_reviews import record_teacher_review
candidate = json.loads(Path('runtime/teacher-draft-001/result.json').read_text())
review = record_teacher_review(
    Notella('runtime/review-store'), candidate,
    reviewer={'name': 'Your reviewer', 'kind': 'human', 'independent': False},
    criteria=[{'id': 'policy', 'requirement': 'Decision follows the supplied policy'}],
    judgments=[{'criterion': 'policy', 'status': 'fail',
                'rationale': 'The draft assigned a critical trigger despite unresolved outage cause.'}],
)
print(review['id'], review['artifact']['disposition'])
```

The example records a supplied reviewer assertion; use the actual reviewer identity and truthful independence status. Statuses are `pass`, `fail`, or `uncertain`. Dispositions are `review_passed`, `rejected`, or `needs_review`. Even an all-pass review has `trainingPermissionGranted=false`: curriculum admission remains a separate explicit action with source permissions and experiment scope. There is no new HTTP submission route for this review API.

See the constrained teacher v2 results for a completed six-case diagnostic and the separate student augmentation experiment for its explicitly reviewed admission. Their agent reviews are not independent validation.

## Smaller-student experiment

The [constrained teaching diagnostic](../experiments/colibri-teacher-v2-constrained/RESULTS.md) and [0.6B student comparison](../experiments/student-v1-teacher-augmentation/RESULTS.md) show the full path from preserved candidate to agent review, explicit scoped admission, sequential training and exact-output evaluation. The direct student performed better in this diagnostic; teacher generation is not automatically useful. Both cohorts are related synthetic development cases, and no phone performance claim follows from them.

---

[Previous: Tutorial 9 — Bind trusted input and output contracts](input-output-contracts.md) · [Next: Tutorial 11 — Represent an evolving scenario](scenarios.md)
