# Tutorial 4: run and inspect a real training job

The purpose of training is better evidence-grounded understanding, not a completed run. Reproduce the preparation, preserve failures, and judge the resulting model separately before considering any warning application.

**Outcome:** submit an admitted curriculum to the local LoRA backend and inspect concrete completion evidence. Training can consume significant time and GPU resources; the earlier tutorials do not start it.

## 1. Configure the environment explicitly

The core API has no third-party dependencies. Training uses the versions in `training-requirements.txt`; the tested machine used torch 2.8.0+cu128 on an RTX 2070 with 8 GiB. Install the CUDA build appropriate to your own system in a dedicated environment. A plain torch version number alone does not select a suitable CUDA wheel.

Weights must already exist locally and be licensed for the intended use. Notella does not download them. The current engine assumes a causal language model with a compatible chat template, a defined EOS token and architecture support for its LoRA target layers. It is not a guarantee of compatibility with every model advertised as an SLM.

The code currently uses FP16 compute with NF4 double quantization, rank/alpha LoRA settings, completion-only supervised loss and frozen embedding/output matrices on CPU. Those implementation choices suit the tested environment and may need a separate backend for another platform. CPU-only training is not supported by this backend.

## 2. Start the API with an allowlisted model

The local machine already has a compatible environment and base model:

```powershell
Set-Location C:\workspace\Notella
$env:NOTELLA_API_TOKEN = python -c "import secrets; print(secrets.token_urlsafe(32))"
python -m notella serve --store data --engine training_engine --python C:\workspace\TUltra-Project\LayerTime\tools\ai-training\.venv\Scripts\python.exe --model qwen3-4b=C:\workspace\TUltra-Project\LayerTime\tools\ai-training\models\qwen3-4b-instruct-2507
```

The API process can use a normal Python interpreter. The --python option selects the training environment. The --model option maps a public alias to a server-owned local directory. Replace these paths when moving the service; the core does not depend on LayerTime's folder layout.

Use one server process per store. The local exclusive lock coordinates Notella jobs within that store, not unrelated GPU applications. Check other workloads before training.

## 3. Compile a curriculum and create a plan

```python
import json, os
from pathlib import Path
from notella import Client

client = Client(os.environ['NOTELLA_API_TOKEN'])
o = client.register_ontology(json.loads(Path('examples/layertime.ontology.json').read_text()))
c = client.compile(o['id'], json.loads(Path('examples/layertime.examples.json').read_text()))
p = client.plan(c['id'], 'qwen3-4b', steps=60, rank=16, learning_rate=0.00005)
print(p['id'])
```

This example plans two passes' worth of updates for 30 training variants at accumulation=1. It is a small developmental run, not a recipe proven to produce a useful model. The larger completed 742-update run also included existing admitted LayerTime material and is retained separately.

## 4. Start training deliberately

```python
job = client.start_job(p['id'])
print(job['id'], job['status'])
```

This is the step that starts real work on the GPU. The service exports a job-specific hash-checked dataset, snapshots API and engine source, and launches a fixed argument array without a shell. API callers cannot choose arbitrary executables or output paths.

The engine reads training and validation. It verifies the test split for integrity but never supplies its answers to the trainer. Oversized examples fail instead of silently truncating labels. No existing adapter is continued by the current public plan interface; runs start from the configured base.

## 5. Poll the job and inspect evidence

```python
import time
while job['status'] in ('starting', 'running'):
    time.sleep(5)
    job = client.get('jobs', job['id'])
print(job['status'], job.get('exitCode'))
```

Job folders live under your store's `jobs/<id>/`:

| Artifact | What to inspect |
|---|---|
| job.json | Plan ID, process ID, status, exit code, command and source hashes |
| dataset/manifest.json | Exact ontology, split hashes, exclusions and development status |
| engine/ and api-source/ | Source used by the job |
| stdout.log / stderr.log | Token lengths, progress, loss and failures |
| adapter/optimizer-stability.json | Applied updates versus skipped mixed-precision iterations |
| adapter/weight-stability.json | Finiteness of saved adapter tensors |
| adapter/runtime-manifest.json | Actual packages, arguments and source/corpus hashes |
| adapter/training-metrics.json | Runtime, loss, measured memory and global step |
| adapter/development-manifest.json | Development-only model status |

Requested steps are not evidence of applied updates. A successful process and finite saved weights establish numeric completion, not semantic accuracy. Loss is an optimization diagnostic. Generate and review held-out answers before claiming behavior improved.

## 6. Handle failure or interruption

A nonzero child exit produces failed status. Preserve the logs and partial output. The backend does not automatically retry, overwrite adapters or fall back to another model. Fix the cause and submit a new plan/job as appropriate.

Keep the server alive while its job runs. If it crashes, the child can continue and the GPU lock deliberately remains. Inspect the stored PID, whether that exact process is still active, the adapter manifests and logs before recovering. Automatic stale-job reconciliation and cancellation are not yet implemented. Do not delete a lock solely because you reopened the API.

The retained engine has checkpoint machinery, but the public API does not expose resumptions yet. A future resume API must verify source, model, data and training arguments against the saved state; it must not turn a partial directory into a new untracked run.

## 7. Reproduce the integration probe

```powershell
$env:NOTELLA_TEST_MODEL='C:\workspace\TUltra-Project\LayerTime\tools\ai-training\models\qwen3-4b-instruct-2507'
& C:\workspace\TUltra-Project\LayerTime\tools\ai-training\.venv\Scripts\python.exe verify_backend.py
```

This launches a temporary authenticated HTTP server and a real two-update job, then stores its numeric results. It is intentionally an integration probe. Its reference to the LayerTime warning curriculum does not make two updates an effective warning model.


## Long semantic-state targets and the 8 GB workstation

The first scenario run retained full GPU vocabulary-logit/loss buffers for long graph targets and stopped after 19 applied updates without a final adapter when optimizer progress ceased near GPU capacity. No OOM exception was reported. A chunked-loss-only longest-target check did not complete an update and was preserved separately.

The current --cpu-frozen-layers path keeps the frozen output projection and its large logits on CPU, computes token-mean cross entropy in checkpointed chunks there, and transfers the scalar loss back to CUDA. Prompt masking and target shift are unchanged. Optional training-environment tests compare loss/gradient values and exercise differentiable CPU-logit/GPU-loss transfer. A two-update check on the longest scenario training example completed with zero skips and finite weights before the fresh full run. Actual source/device/precision choices are recorded per job; numerical equivalence within the tested tolerance is not a claim of bitwise identity.

Colibri is a local teacher inference engine in this workflow. It can propose scenarios but is not the student optimizer or an automatic remedy for training activation/loss memory. No other applications are stopped to make the model fit. Do not combine discarded partial-run updates or the two-update hardware check with a fresh adapter's applied-update count.
