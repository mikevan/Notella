# Tutorial 8: supply measured temporal facts without inventing a warning

**Outcome:** derive a clock-aware time relation from the LayerTime profile's observation and retain a provenance receipt. This source-checkout adapter does not compute posture, drone identity, source independence or attack probability.

Run from C:\workspace\Notella, or add that folder to your Python path. The domain-specific adapter lives in profiles/layertime; the general interval calculator remains in notella.correlation. It is an example profile extension, not a separately installed core package.

## Derive a relation

```python
from profiles.layertime.temporal_features import derive_temporal_fact

observation = {
    'timeBasis': 'relative milliseconds on a shared clock',
    'linkingWindowMs': 120000,
    'disruption': {'timeMs': 1000, 'uncertaintyMs': 100},
    'drone': {'timeMs': 19000, 'uncertaintyMs': 100},
}
fact = derive_temporal_fact(observation)
print(fact['value']['measurement'])
```

Expect order=after, delayIntervalMs=[17800,18200], withinWindow=true and causationEstablished=false. These are interval calculations under the supplied clock assumption. They do not independently establish that the clocks were synchronized or that either event was classified correctly.

## Keep unknown distinct from false

If the clock basis is not the supported shared-clock assertion, the adapter returns unknown order and no numeric delay subtraction. A missing timestamp also leaves order unknown. Overlapping uncertainty can make order uncertain. An interval straddling the window can leave withinWindow null even when order is after. None of these is proof that the events are unrelated.

An entirely later interval outside the configured window yields withinWindow=false. That is a failure of this configured temporal link, not a claim that no separate hazard exists.

## Preserve receipts and inputs

The adapter does not mutate its input. Its result retains the source observation SHA-256, algorithm identity/version, configured window, assumption scope and a statement that clock alignment was not independently verified. Invalid uncertainty, timestamp or window values are rejected. Full receipts belong beside the original observations and exact model outputs.

The v4 diagnostic adds only the measurement and window to model-visible facts. It keeps full receipts outside the model context for audit. It supplies no target label, posture or trigger decision. Neither the helper nor the language model should treat a time association as proven causation.

## Reproduce the experiment

After the v4 primary and robustness comparisons have completed:

```powershell
$env:NOTELLA_EXPERIMENT_MODEL = 'C:\workspace\TUltra-Project\LayerTime\tools\ai-training\models\qwen3-4b-instruct-2507'
& C:\workspace\TUltra-Project\LayerTime\tools\ai-training\.venv\Scripts\python.exe experiments/warning-v4-expanded/run_temporal_facts.py
```

The runner refuses existing output logs to preserve completed results. Use a new experiment version rather than overwrite them. It uses the same saved adapter, a matched base condition, the same decoding and the existing labels. This is additional inference context, not further training.

## Read the actual limits

On the selected authored development cases, adding measured time facts moved the adapter from 7/10 to 9/10 full primary-case matches and from 3/6 to 4/6 robustness matches. The base remained at 1/10 and 3/6 respectively. The measurements helped the selected temporal failures but introduced a wrong reason code on the benign case. Instruction-like captured text and source-lineage aliases still fail.

These are post-hoc development observations, not independent field accuracy or proof that the adapter learned arithmetic. The full report and exact outputs are preserved in experiments/warning-v4-expanded/RESULTS.md and runtime/warning-v4-temporal-facts. The profile needs stronger input boundaries, explicit source lineage and output consistency checks before deployment can be considered.
