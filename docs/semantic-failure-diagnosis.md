# Tutorial 15: Diagnose a semantic training failure

This walkthrough uses the completed [scenario comparison](../experiments/scenario-model-v3/RESULTS.md). Run the read-only reports from the project directory:

```powershell
python experiments/scenario-model-v3/summarize.py
python experiments/scenario-model-v3/audit_revisions.py
```

The first reports criticality, structure and evidence agreement separately. The second checks the direction and endpoints of changes between successive prefixes. Never call a correct escalation direction sufficient when both endpoint severities are wrong. Neither report judges explanation truth automatically or demonstrates persistent model memory.

## Start with the semantic rule, not the graph shape

The ontology is the semantic model. In this profile, current reviewed compromise evidence on the primary asset warrants critical posture without requiring a preceding scan/authentication sequence. A benign explanation only covers its explicitly referenced observations. A correction withdraws support for the originating event and its reposts. These rules govern interpretation of changing nodes and edges; recognizing concept names or reproducing JSON is insufficient.

Inspect `S-Q71-step-1` in the preserved trained outputs. It produces a contract-valid state but calls the standalone compromise contextual. This isolates a semantic failure from schema failure. At step 4 its explanation says the benign operation does not negate compromise, but its decision still falls to contextual. At step 5 it retains criticality after correction. Inspect the explanation, citations, retained/withdrawn support and final decision together.

## Audit what examples actually teach

The training source has 20 rows, but only 11 normalized distinct visible prefixes, all in one authored family. Seven first-observation rows are contextual; every critical row contains all three scan/authentication/compromise concepts. This creates a plausible shortcut: sequence shape predicts the label, while the ontology's standalone-compromise rule is never demonstrated. The output behavior is consistent with that shortcut, but this experiment does not prove its cause.

A curriculum correction should teach contrastive semantic changes across newly authored families: sufficient evidence alone, irrelevant additions, scoped explanations, actual retraction, shared-source repetition and unresolved order. Give the trainer explicit rule coverage and transition coverage to review before admission. Balance semantic conditions, not merely label counts. Duplicated prefixes should not silently dominate training exposure.

Do not copy the inspected development cases or their answers into training. Write fresh training families and freeze separate untouched evaluation families before running another experiment. The existing cases remain a known diagnostic; subsequent improvement on them is not independent generalization evidence.

## Change one thing first

First change the curriculum while holding model, optimizer settings and update budget fixed. Retain exact failed outputs and compare rule handling, decision revisions, evidence support and graph contracts again. A larger step budget, changed loss weighting and delta representation are separate experiments. Loss reduction is not a replacement for generated-answer evaluation; this run's low loss coexisted with wrong decisions and repetitive generation.

For deployment, validate proposed updates before replacing an incident's accepted state. Reject unsupported clearing and reuse of retracted support, retain the last validated state, and mark uncertain proposals for review. Permit justified de-escalation after a valid correction. This consistency gate is a required integration step, not an already implemented detector or proof that the model understands the ontology.
