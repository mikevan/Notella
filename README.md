# Notella

**Weave knowledge into understanding.** A Project Revive Solutions technology.

Notella provides a reusable Python API and a versioned local HTTP API for ontology-guided semantic LoRA training. LayerTime is its first profile, not a dependency of the core API. Version 0.1 is a working developer foundation, not a hosted service or qualified threat-detection product.

**Start with the [guided documentation and tutorials](docs/index.md).** The [first tutorial](docs/tutorial.md) runs without a GPU; the [training tutorial](docs/training.md) explains exactly when real training starts. Other applications can use `from notella import Client` or the authenticated OpenAPI description at `/v1/openapi.json`.

## Quick start

Python 3.11 or later runs the core and HTTP API without third-party dependencies. From this folder:

```powershell
python -m unittest discover -s tests -v
python -m notella demo --store data
$env:NOTELLA_API_TOKEN = python -c "import secrets; print(secrets.token_urlsafe(32))"
python -m notella serve --store data
```

The server binds to `127.0.0.1:8765`. Keep the token in your environment; authenticated endpoints require `Authorization: Bearer <token>`. `GET /health` is public. Request bodies are limited to 4 MiB. This release supports local use only; TLS, remote hosting, multiple workers, user accounts, cancellation and distributed GPU scheduling are future work.

## Python API

```python
import json
from pathlib import Path
from notella import Notella

api = Notella('data')
ontology = api.register_ontology(json.loads(Path('examples/layertime.ontology.json').read_text()))
curriculum = api.compile(ontology['id'], json.loads(Path('examples/layertime.examples.json').read_text()))
plan = api.plan(curriculum['id'], 'qwen3-4b', steps=70)
```

Concepts, directed relations, task instructions and an output contract are explicit. Teaching examples carry concepts, original family, split, source reference, permission, label author and training admission. Artifacts have immutable SHA-256 identities and are verified on retrieval. Version changes produce new artifacts. An ontology is serialized into training prompts; references alone are not claimed to teach its meaning.

The compiler rejects unknown concepts, unadmitted training sources, family/input overlap across splits and explicitly excluded evaluation prompt hashes. Exclusion hashes must use Notella's canonical JSON fingerprint of either the input string or system/user message list. Near-duplicate detection and independent source-family review still require human work. Label validity and redistribution permission are recorded assertions, not independently certified facts.

Output contracts support a documented subset of JSON Schema: type, properties, required, additionalProperties=false, items, enum, const, length/item bounds, uniqueItems, numeric bounds and description. Complex JSON Schema features such as `$ref`, oneOf and pattern are unsupported. This is not an OWL/RDF reasoner or a general JSON Schema implementation.

## HTTP API v1

| Method | Endpoint | JSON request |
|---|---|---|
| POST | `/v1/ontologies` | Ontology object; see example |
| POST | `/v1/curricula` | `ontologyId`, `examples`, optional `excludedPromptHashes` |
| POST | `/v1/plans` | `curriculumId`, `baseModel`, optional `steps`, `rank`, `learningRate` |
| POST | `/v1/jobs` | `planId`; requires a configured training backend |
| GET | `/v1/jobs/{id}` | Job state and local process/result information |
| POST | `/v1/evaluations` | `curriculumId`, `predictions` mapping example IDs to JSON objects, optional `split` |
| GET | `/v1/{ontologies,curricula,plans,evaluations}/{id}` | Retrieve and verify an artifact |

Creation returns `{id, artifact}`, except jobs, which return their job state. Missing artifacts return 404, invalid requests 400, missing/wrong tokens 401. Ontology and curriculum creation are idempotent for identical canonical content. Job submission intentionally creates a new run; an exclusive GPU lock prevents competing jobs within the same store.

```powershell
$headers = @{ Authorization = "Bearer $env:NOTELLA_API_TOKEN" }
$ontology = Invoke-RestMethod http://127.0.0.1:8765/v1/ontologies -Method Post -Headers $headers -ContentType application/json -Body (Get-Content examples/layertime.ontology.json -Raw)
$payload = @{ ontologyId=$ontology.id; examples=(Get-Content examples/layertime.examples.json -Raw | ConvertFrom-Json) } | ConvertTo-Json -Depth 40
$curriculum = Invoke-RestMethod http://127.0.0.1:8765/v1/curricula -Method Post -Headers $headers -ContentType application/json -Body $payload
```

## Real local training

The core remains dependency-free. Training requires an existing CUDA environment with the pinned packages recorded in `training-requirements.txt`, a licensed local base model, and the included training engine. No weights are downloaded by the API. The engine is reused from the tested LayerTime implementation with a Notella-specific curriculum verifier; its provenance is recorded in `training_engine/PROVENANCE.json`.

```powershell
python -m notella serve --store data --engine training_engine --python C:\workspace\TUltra-Project\LayerTime\tools\ai-training\.venv\Scripts\python.exe --model qwen3-4b=C:\workspace\TUltra-Project\LayerTime\tools\ai-training\models\qwen3-4b-instruct-2507
```

Only model aliases configured by the server owner can be used. API callers cannot supply executable names, commands, model paths or output paths. Jobs export hash-checked datasets, preserve separate validation/test splits, and run the trainer without a shell. The trainer uses training and validation only. Models and Python environments can live anywhere; the LayerTime paths above are local examples, not required locations.

One server process per store is supported. Keep the server running while training: it records child completion and releases the lock. If the server exits unexpectedly, the child may continue; inspect `jobs/<id>/job.json`, its PID, adapter manifests and `gpu.lock` before manually recovering. Never delete a lock merely because the server restarted. The lock does not coordinate other applications using the GPU.

## Evaluation and limitations

`evaluate()` measures schema validity, coverage and exact target agreement on a held-out split. It explicitly does **not** measure semantic accuracy. Interpretations need criterion-based review tied to exact generated outputs, plus independent field evidence before product qualification. All artifacts and models remain `releaseEligible=false`.

The initial camp profile contains 30 training variants from ten synthetic families, two validation families and three test families. These are policy-teaching examples, not 35 observed incidents. The 120-second timing window and posture levels are proposed project policy, not calibrated attack probabilities. No model can establish a looming attack merely because two events occur close together.

See [temporal evidence design](docs/temporal-evidence.md) and [development results](docs/results.md).
