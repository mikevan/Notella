# Retraction and repetitive-output curriculum protocol

Owner instruction: tackle retraction errors and repetitive output, hold model and training settings fixed, rerun comparison. This run starts a fresh adapter from the same local Qwen3-4B-Instruct-2507 base, not from v4's adapter.

## Fixed controls

Ontology 27f3474132eb10cccbb5c2eb0a2126fba8f2156dd2f254bc16fa9a6bfcca5efa and reference rule are unchanged. Same twenty training rows, eighty requested optimizer updates, rank 16/alpha 32, q_proj/v_proj LoRA, learning rate 0.0001, seed 42, batch 1/accumulation 1, NF4 QLoRA, completion-only loss, CPU frozen-logit offload, 4096 training/context bound and engine/package versions. Greedy generation and its 1536-output-token cap remain unchanged. No repetition penalty, constrained decoding, output repair, warning-continuity retries or loss weighting is introduced into this comparison.

Actual launch commands are compared after normalizing snapshot/dataset/output paths. Final reporting verifies actual arguments, engine hashes, packages and base intake identity. Preflight confirms all eighteen known prompt hashes match and every input/reference answer fits without truncation. Training maximum is 2403 tokens; evaluation reference answers need at most 857 output tokens.

## Curriculum intervention

Twenty unique prefixes are selected as ten before/after contrasts from one synthetic authoring suite, not ten independent source families. Some earlier steps are intentionally omitted from training exposure; their evidence remains present in each selected visible prefix. The generic contract still validates visible-prefix history, graph identity and counts. Cases include:

- Compromise withdrawn with no surviving link: critical to contextual.
- A repost and its originating compromise withdrawn together: critical to contextual.
- Compromise withdrawn while scan/auth support survives: critical to high.
- Benign explanation of a scan/auth pair followed by compromise then its withdrawal: critical to contextual.
- An unrelated asset's compromise remains after the primary compromise is withdrawn: primary posture becomes contextual.
- Two independent primary compromise assertions, only one withdrawn: remain critical.
- Successive withdrawals of independent assertions: critical until the final active assertion is removed.
- Secondary-asset correction with primary compromise intact: remain critical.
- Withdrawn compromise leaves high concern, then benign explanation weakens the surviving pair: high to contextual.
- A genuinely new compromise after a withdrawn one: contextual to critical.

Targets distinguish active primary compromise IDs from retired report IDs. Assessment rationales are short, fact-specific, and use varied sentence structures. Change summaries state the evidence update without repeating the rationale. Graph/schema and raw visible-prefix input format do not change. This is a combined curriculum intervention: coverage, exposure mix and target prose change together, so improvements cannot isolate which element caused them.

Class counts are critical 11, contextual 7, high 2. Labels and criticality trajectories are explicitly checked against the unchanged rule reference, in addition to structural validation. Corrections on credentials were attempted during authoring but rejected by the unchanged ontology, whose correction relation targets compromise evidence. Those drafts were revised before admission/launch; no ontology or active job snapshot was edited to accommodate them.

Reviewer and author are the same agent. Semantic motifs are intentionally informed by diagnosed failures, but new scenarios and targets are authored from the rule reference, not copied from inspected evaluation objects or generated answers. This is synthetic development, not independent expert review or field truth.

## Evaluation and repetition

All eighteen v4 prefixes are now known inspected diagnostics. Six new controls (F-1120/F-1230) froze before training: an unrelated correction must not clear current primary compromise, and new credential activity must not revive a withdrawn compromise. The previous adapter is compared on known cases only; it is not generated on the fresh six. Fresh controls share author/policy and semantic motifs with training, so do not establish independent generalization.

Reuse the previous base outputs on the eighteen unchanged known prompts only after prompt hashes and exact re-scoring agree. Generate the six fresh baseline outputs and all twenty-four new-adapter outputs. Preserve every output, time, token count, failure and score. Do not restart over existing journals or silently drop cases. Keep current-vs-historical support, scope, graph contract, assessment changes and token-cap failures separate.

The narrative repetition diagnostic in repetition.py is fixed before candidate generation: tokenize rationale/summary prose into lowercase words; flag a narrative of at least 36 words when some 12-word window occurs at least three times and duplicate-window fraction is at least 0.25. Inspect incomplete quoted prose as well as valid JSON; exclude ordinary graph-field repetition. This heuristic is not a correctness judge. The same code scores previous/base/new outputs, with its hash recorded in evidence.

## Execution and retained evidence

Training started immediately after validated preparation. run_comparison.ps1 waits for 80 applied updates, zero skips and finite weights, then runs base and adapted generation serially and report.py. report.py validates provenance and saves exact outputs/receipts and hashes under evidence/, excluding model weights. audit_revisions.py reports changes between independently prompted prefixes, not persistent model-state rollout.

Progress: inspect runtime/scenario-model-v5/training-runner.log and generation logs, or run progress.py. After completion RESULTS.md and evidence/comparison.json contain separate known/fresh measures. Do not rerun preparation/training/generation over preserved artifacts; explicit recovery must preserve failures. No Git staging, commits or pushes are performed. No phone model, notification integration or operational alert guarantee is changed by this experiment.
