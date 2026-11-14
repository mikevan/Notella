[Tutorial index](index.md) · [Tutorial 0: environment setup](setup.md)

# Tutorial 2: use Notella from another application

The training workflow should be usable by other tools without binding the purpose to one interface. This tutorial exposes the same inspectable local workflow through HTTP; it is a development component, not a deployed protection service.

**Outcome:** run the local service and use the same curriculum workflow through its HTTP API. No training starts in this tutorial.

## 1. Start a server with a known token

In a PowerShell window:

```powershell
# Run from the project root selected in Tutorial 0.
$env:NOTELLA_API_TOKEN = python -c "import secrets; print(secrets.token_urlsafe(32))"
# Copy the token into your second local client's environment through your normal secret-handling process.
python -m notella serve --store runtime/http-tutorial --port 8765
```

Keep this window open. Do not put a real token in source control or shared screenshots. The service requires at least 24 characters and binds only to loopback. A missing token causes startup to fail rather than silently exposing an unauthenticated service.

In a second window:

```powershell
Invoke-RestMethod http://127.0.0.1:8765/health
```

Expect product=Notella, apiVersion=v1 and status=ok. Health is the only unauthenticated endpoint. A successful health request does not imply a training backend is configured.

## 2. Run the HTTP example

Set `NOTELLA_API_TOKEN` in the client window to the same token, using your preferred secret mechanism. Then:

```powershell
# Run from the project root selected in Tutorial 0.
python -m examples.http_tutorial
```

The client registers the temperature ontology, compiles its examples, creates a plan and submits the authored fixture to the structural evaluator. Expect one fixture schema pass, one exact target match, semanticAccuracyMeasured=false and trainingStarted=false.

The server and client use HTTP. The client needs the token and URL, not access to the server's artifact files or Python object state.

## 3. Write a small client yourself

```python
import os
from notella import Client
from examples.tutorial import teaching_material

client = Client(os.environ['NOTELLA_API_TOKEN'])
ontology, examples = teaching_material()
o = client.register_ontology(ontology)
c = client.compile(o['id'], examples)
saved = client.get('curricula', c['id'])
print(saved['splits'])
```

The Python client is a thin HTTP wrapper using the standard library. Non-Python applications can call the same endpoints with JSON. HTTP errors propagate as `urllib.error.HTTPError`; inspect the status and JSON error body before retrying.

## 4. Call an endpoint from PowerShell

```powershell
$headers = @{ Authorization = "Bearer $env:NOTELLA_API_TOKEN" }
$spec = Invoke-RestMethod http://127.0.0.1:8765/v1/openapi.json -Headers $headers
$spec.info
```

This retrieves the machine-readable OpenAPI 3.1 description. Request examples and field constraints are expanded in the [API reference](api-reference.md). The dynamically supplied ontology output contract is validated separately by Notella's supported JSON Schema subset.

For a real LayerTime ontology:

```powershell
$ontology = Invoke-RestMethod http://127.0.0.1:8765/v1/ontologies -Method Post -Headers $headers -ContentType application/json -Body (Get-Content examples/layertime.ontology.json -Raw)
$request = @{ ontologyId=$ontology.id; examples=(Get-Content examples/layertime.examples.json -Raw | ConvertFrom-Json) } | ConvertTo-Json -Depth 40
$curriculum = Invoke-RestMethod http://127.0.0.1:8765/v1/curricula -Method Post -Headers $headers -ContentType application/json -Body $request
$curriculum.artifact.splits
```

Expect 30 training, two validation and three test examples. They are synthetic examples of a proposed warning policy, not observed attacks.

## 5. Understand retries

Registering identical canonical artifact content is idempotent: the same content returns the same ID. Submitting a training job is different: it requests a new run. Do not automatically retry POST /v1/jobs after a network timeout without checking the store and existing job state. A GPU lock prevents a second concurrent job in that store, but it is not a general idempotency key.

Stop the server with Ctrl+C after the tutorial. For real jobs, keep it running until the child has finished and the completed/failed state has been saved. See [training](training.md) for recovery limitations.

---

[Previous: Tutorial 1 — Your first semantic curriculum](tutorial.md) · [Next: Tutorial 3 — Design a useful curriculum](curricula.md)
