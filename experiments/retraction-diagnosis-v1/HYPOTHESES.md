# Five root-cause hypotheses: tests to design next

These are ranked working hypotheses, not established causes. Retraction correctness and repetitive generation require separate scorecards. No additional diagnostic training or readback generation has been executed under this plan. The completed interface audit is documented separately.

| Rank | Hypothesis | Discriminating test |
| --- | --- | --- |
| 1 | Small, related curricula teach scenario shortcuts instead of conditional semantic rules. | Compare exact trained cases with equivalent cases whose IDs, ordering and asset assignments change; keep semantic labels and model weights fixed. Good fit but poor equivalent-case performance supports a generalization problem. |
| 2 | Evidence-state reconstruction interferes with interpretation. | Supply mechanically derived active/retracted facts for failed cases without supplying severity or target explanations. Improvement with fixed weights supports the reconstruction-burden hypothesis. |
| 3 | The loss emphasizes long graph/prose output more than the critical semantic decisions. | Measure error/loss by output component, then separately propose a controlled supervision ablation. A loss change is a new training condition and must not be silently introduced into the existing comparison. |
| 4 | The current LoRA setup does not reliably learn the examples it sees. | Replay exact trained examples before changing anything else. Compare base and saved adapter on identical prompts; inspect effective labels/gradients and adapter application if even training examples fail. |
| 5 | Early generated errors create self-reinforcing continuation loops. | Compare continuation after a mistaken generated prefix with continuation after a corrected prefix under fixed weights. Forced-prefix diagnostics are not held-out accuracy or new training targets. |

Run hypothesis 4's sanity check first, then hypothesis 2's state-input test. Freeze cases, outputs, pass/fail criteria and controls before inspecting results. Numerical stability is not proof of adequate learning. The token cap stops the observed loops; it does not explain incorrect meanings already produced before exhaustion. Warning-continuity tooling contains failures and does not establish any root cause.
