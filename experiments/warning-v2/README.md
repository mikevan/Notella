# Warning representation experiment v2 — prepared after the baseline

The first completed adapter missed the critical-warning trigger. A plausible issue is that generic caution about proving attacks overrides the distinct precautionary policy. This is a hypothesis, not a demonstrated cause.

The next controlled experiment gives warning posture and causal certainty different explicit fields. It keeps causation=not_established even when posture=critical. Missing clocks, unknown signals, source dependence, reversed order and verified benign explanations receive distinct reasons. The proposed warning policy remains synthetic and uncalibrated.

`prepare.py` loads only the previously authored training and validation families. It does not load the frozen test file, generated acceptance answers or interpretation reviews. It prepares 30 training examples and two development-validation examples, with no test examples. The planned fresh-base run is 120 updates (four passes over this small training set), using the established 4B QLoRA configuration.

These are representation changes to existing synthetic teaching examples, not 32 new independent observations. Development validation is limited to a corroborated critical sequence and an unknown-signal contrast. Passing those would not establish performance on missing clocks, benign operations, broader Wi-Fi interpretation or field use.

Before training, preserve the requested baseline check-in. Then compare the base model and candidate on the exact same model-visible development prompts, with the same generation settings. Use development validation to assess this hypothesis. New independent, prospectively frozen scenarios are still needed before claiming generalization; the three previously inspected test outputs are not a fresh independent test for this repair.

Preparation command, from C:\workspace\Notella:

```powershell
$env:PYTHONPATH = (Get-Location).Path
python experiments/warning-v2/prepare.py
```

This writes versioned artifacts and a plan under runtime/warning-v2 and does **not** launch training. It is intentionally separate from the owner-reviewed foundation checkpoint.

## Reproduce this experiment

The versioned development-examples.json contains only the 30 training and two development-validation examples. Preparation no longer requires ignored original runtime files. Existing test data and generated test outputs are not loaded by prepare.py.

After the owner-run baseline check-in, from the Notella folder:

```powershell
$env:PYTHONPATH = (Get-Location).Path
$env:NOTELLA_EXPERIMENT_MODEL = 'C:\workspace\TUltra-Project\LayerTime\tools\ai-training\models\qwen3-4b-instruct-2507'
$env:HF_HUB_OFFLINE = '1'
python experiments/warning-v2/prepare.py
& C:\workspace\TUltra-Project\LayerTime\tools\ai-training\.venv\Scripts\python.exe experiments/warning-v2/run.py
```

run.py starts real GPU training and then sequential base/adapted generation. It refuses an existing launch.json to preserve a prior run. Do not rerun over a completed or interrupted experiment; inspect and create a new version for a new run. Model paths and the Python executable can be replaced for another compatible local setup.

Output: runtime/warning-v2/comparison.json, base-validation.json, adapted-validation.json and the job's complete source/data/adapter snapshots. PROTOCOL.md defines the interpretation criteria separately from structural scores.

This run changes the output contract, instructions, data mixture and number of passes relative to the initial 742-update run. It does not isolate which of those changes caused a difference. The matched base/adapted comparison tests training effects within the new representation; comparison with the earlier run is descriptive only.
