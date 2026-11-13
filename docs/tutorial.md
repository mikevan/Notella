# Tutorial 1: your first semantic curriculum

**Outcome:** create and retrieve a versioned ontology, compile five examples, create a training plan and evaluate an authored fixture. This tutorial does not load or train a model.

## 1. Check the environment

```powershell
Set-Location C:\workspace\Notella
python --version
python -m unittest discover -s tests -v
```

Use Python 3.11 or later. The core uses the standard library. If `python` is not on your path, substitute the full path of a suitable Python executable in every command. Installing the core with `python -m pip install -e .` is optional when running from this project folder.

## 2. Run the complete example

```powershell
python -m examples.tutorial --store runtime/tutorial
```

The example prints four content-addressed IDs and these values:

```json
{
  "splits": {"train": 3, "validation": 1, "test": 1},
  "fixtureOnly": true,
  "modelLoaded": false,
  "trainingStarted": false,
  "semanticAccuracyMeasured": false
}
```

IDs are SHA-256 fingerprints of canonical content. Running the same example again produces the same artifact IDs. Changing a definition, target or source annotation produces a new relevant artifact. The summary is also saved as `runtime/tutorial/tutorial-result.json`.

## 3. Define the semantic model and represent it as an ontology

The ontology **is the explicit representation of the semantic model**. As the trainer, define what the application must understand: its entities, observations, meanings, relationships and evidence requirements. Then express that model as an ontology. Scenario examples and expected decisions follow from that specification.

For the intended scenario workflow, the AI learns to interpret changes in this semantic model over time. Nodes represent scoped semantic elements, typed edges represent supported relationships, and morphology includes changes in their support, structure and interpretation. This temperature example teaches a small static distinction; it does not yet demonstrate evolving attack scenarios. Continue with [the full method](semantic-ontology-morphology.md) and [Colibri scenario authoring](scenario-authoring.md).

Open `examples/tutorial.py`. `teaching_material()` returns the ontology and its examples. The ontology defines observation, threshold and interpretation, then connects them with supportedBy and comparedAgainst relations.

```python
from examples.tutorial import teaching_material
from notella import Notella

api = Notella('runtime/my-first-curriculum')
ontology, examples = teaching_material()
registered = api.register_ontology(ontology)
print(registered['id'])
```

The output contract requires a finding string, an exceedsThreshold boolean and a limitation string. The contract constrains the answer's shape; the authored target demonstrates the intended meaning.

For the real LayerTime application, continue with the [ontology walkthrough](layertime-ontology.md): nine concepts, four relationships, a worked example and the limits of the proposed threat policy. This first tutorial retains the smaller temperature example so the reusable API is easy to learn.

## 4. Compile the examples

```python
curriculum = api.compile(registered['id'], examples)
print(curriculum['artifact']['splits'])
```

Three training families teach above, below and exactly at a strictly-greater-than threshold. Separate validation and test families supply different readings. The compiler checks source admission, concept references, family/input separation and target structure. It also serializes the ontology into each model-visible system message.

These are five synthetic teaching examples from a tiny related domain. Their existence does not establish generalization. Distinct IDs are not sufficient to establish independence; this example is intentionally educational.

## 5. Inspect an expected failure

```python
from copy import deepcopy
from notella import ValidationError

bad = deepcopy(examples)
bad[-1]['family'] = bad[0]['family']
try:
    api.compile(registered['id'], bad)
except ValidationError as error:
    print(error)  # Family crosses splits
```

This rejects a training family reused as a test family. Try changing a concept reference to an unknown concept or setting the training source's trainingAllowed to false. Both should also be rejected. A rejected example should be corrected or explicitly excluded, rather than silently relabelled to make a check pass.

## 6. Create a plan without starting training

```python
plan = api.plan(curriculum['id'], 'configured-model-alias', steps=30)
print(plan['artifact'])
```

A plan is an immutable description of the intended run. Creating it does not reserve a GPU or launch a process. The model string is an alias that the server owner must later map to a local directory. This tutorial intentionally leaves it unconfigured.

## 7. Inspect a fixture evaluation

```python
fixture = {'test-warm': examples[-1]['target']}
evaluation = api.evaluate(curriculum['id'], fixture, split='test')
print(evaluation['artifact'])
```

Expect total=1, schemaPasses=1 and exactTargetMatches=1. This uses the reference answer itself to exercise the evaluator. It is not model output and must never be reported as model accuracy. semanticAccuracyMeasured stays false.

## 8. Retrieve the exact curriculum

```python
saved = api.get('curricula', curriculum['id'])
print(saved['examples'][0]['messages'])
```

Retrieval verifies the stored content hash. Inspect the system prompt, user observation and assistant target. The assistant answer is retained for supervised training, but an inference application must send only the preceding messages.

Next: [repeat this workflow over HTTP](http-tutorial.md), or [design a curriculum for your own domain](curricula.md).
