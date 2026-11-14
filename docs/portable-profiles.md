# Tutorial 6: package a reproducible training profile

Work toward self-protection should be reproducible beyond one developer's machine. Portable profiles preserve the definitions, examples, and settings needed to inspect and repeat a training preparation without claiming that reproducibility proves correctness.

**Outcome:** package an ontology, examples and training settings as a portable profile that another Notella installation can verify and prepare. Preparation creates versioned artifacts and a plan; it does not launch training.

## Why a profile pack?

An experiment should not depend on an ignored runtime folder from one developer's machine. A profile pack includes the actual ontology and example files, their hashes, and explicit plan settings. Notella checks the files before admitting their examples through the normal compiler.

A profile is a reproducibility format, not a signature or permission certificate. Someone can edit files and recompute their hashes. Source permissions, label authorship and training admission still need the review described in the curriculum guide.

## 1. Inspect the working example

The balanced source-identity diagnostic lives at experiments/warning-v3-fit. Its files are:

```text
profile.json
ontology.json
development-examples.json
PROTOCOL.md
```

The examples contain six training variants from two original families and two separate development-validation examples. There are no test examples in this pack. This is a deliberately limited fit diagnostic, not a full warning model or independent evaluation.

## 2. Understand the manifest

```json
{
  "formatVersion": "notella.profile.v1",
  "ontology": {"file": "ontology.json", "sha256": "<actual file SHA-256>"},
  "examples": {"file": "development-examples.json", "sha256": "<actual file SHA-256>"},
  "training": {
    "baseModel": "qwen3-4b",
    "steps": 60,
    "rank": 16,
    "learningRate": 0.0001
  }
}
```

Replace illustrative hashes with actual lowercase SHA-256 values. Components must use relative paths that stay within the profile folder after resolution; ../ escapes and absolute paths are rejected. Only baseModel, steps, rank and learningRate are supported training settings. An optional excludedPromptHashes array uses the compiler's normal exclusion convention.

File hashes are byte-sensitive. Reformatting a JSON file changes its file hash even if its parsed content is equivalent. Notella's internal artifact IDs, in contrast, depend on canonical parsed content. These identities serve different purposes: the pack verifies the supplied files, and the core identifies their structured contents.

## 3. Prepare without training

```python
from notella import Notella
from notella.profile import prepare_profile

api = Notella('runtime/profile-tutorial')
receipt = prepare_profile(api, 'experiments/warning-v3-fit/profile.json')
print(receipt)
```

Expect ontologyId, curriculumId, planId, split counts, profileSha256, componentSha256 and trainingStarted=false. Preparing this pack on a second compatible installation should recreate the same ontology, curriculum and plan IDs. The pack does not include model weights or an executable path.

The baseModel is a logical alias. A server owner must explicitly map it to an already present licensed model directory before a job can start. Copying a profile never grants permission to download a model, execute a command or launch a job.

## 4. Create your own pack

Start with the ontology and examples from the first tutorial:

```python
import hashlib, json
from pathlib import Path
from examples.tutorial import teaching_material

folder = Path('runtime/my-profile')
folder.mkdir(parents=True, exist_ok=True)
ontology, examples = teaching_material()
manifest = {
    'formatVersion': 'notella.profile.v1',
    'training': {'baseModel': 'my-local-model', 'steps': 30, 'rank': 16, 'learningRate': 0.00005},
}
for key, value in [('ontology', ontology), ('examples', examples)]:
    path = folder / (key + '.json')
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')
    manifest[key] = {'file': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
(folder / 'profile.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
```

Then call prepare_profile on runtime/my-profile/profile.json. Expect the temperature tutorial's three training, one validation and one test examples. No model is loaded.

## 5. Check a failure

Change a value in examples.json without changing the manifest. Preparation should reject it with a component hash mismatch. Preserve the original pack, review the change, update the hash in a new pack version and prepare again. Do not remove the integrity check to make a changed file pass.

UTF-8 manifests and component files with or without a BOM are accepted, including files saved by Windows PowerShell. Other encodings should be converted explicitly before packaging.

## What the pack does not prove

Hash verification does not establish that a source is correct, permission is genuine, an ontology is logically consistent, a label is independently reviewed, or the resulting model understands the domain. It makes the exact inputs and intended settings portable and reviewable so those questions can be investigated.
