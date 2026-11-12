# Contract diagnostic v5 — compatibility result

This changes representation, trusted instructions and output-state constraints together, without training. The old adapter does not automatically transfer: it matches 5/10 primary cases, 4/6 old probes and 0/3 new probes, versus 4/10, 4/6 and 0/3 for the base. These incorrect decisions remain failures.

Checks reject all observed wrong outputs in this selected cohort, and two unsupported input specimens are deferred; neither rejection nor deferral is counted as a correct model decision. This does not prove universal rejection of incorrect answers.

The two new captured-payload variants render to exactly the clean uncertain-signal prompt and output in each model condition. The marked text is excluded, but the clean decision is itself wrong here. The prior captured-text probe uses a different time delay, so it is not claimed to have the same prompt as that clean anchor.

This compatibility failure motivated v6 training on the exact typed representation with fresh development controls. Some old normalized anchors equal training inputs and must remain regressions. No model weights or old scores were altered during this diagnostic. Registry lookup is not source authentication or external validation.
