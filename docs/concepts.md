# The method, explained

**The ontology represents the semantic model. Our intended AI captures changes in that model over time (morphology) and interprets them. The trainer's job begins with defining that semantic model and its ontology representation.**

Read [Semantic Ontology Morphology](semantic-ontology-morphology.md) for the intended scenario reasoning, evidence-backed nodes and typed edges, and the distinction between an ontology definition and changing scenario state. The examples below introduce the existing training plumbing; they do not demonstrate the full scenario-level method.

## Start with a distinction the model needs to learn

Suppose a temperature sensor reports 32 degrees Celsius, and a configured rule has a threshold of 30. The observation is 32; the threshold is a policy parameter. The justified interpretation is that the reading exceeds the threshold. Neither number proves a fire or explains why the room warmed.

A model can produce fluent text while confusing these roles. Notella makes the roles explicit and teaches contrasting examples so that changing a relevant fact should change the interpretation.

## Ontology: the structure of the domain

An ontology represents the semantic model through explicit concepts, attributes, identities and relationships. The trainer decides what those elements mean, what evidence supports them and how they should be represented before examples are generated. In the tutorial, the concepts are observation, threshold and interpretation. The interpretation is supported by the observation and compared against the threshold. Concepts have definitions; relations have a subject, predicate and object.

In LayerTime, concepts include temporal precedence, source independence, signal identity, causal claim and warning posture. An urgent warning is a different judgment from an established cause. Keeping those concepts separate is part of the desired behavior.

Notella 0.1 stores this structure as explicit JSON and places it in training prompts. It checks that relation endpoints and example concept references exist. It does not run logical entailment, prove ontology consistency or implement an OWL reasoner. Those would be additional capabilities.

## Semantic: what the examples are teaching

“Semantic” refers to meaning: what a measurement represents, what a relationship supports and what a claim leaves unresolved. It is the intended learning objective, not a guarantee created by naming concepts.

Good semantic contrasts change one relevant relationship. For example, change a reading from above to below a threshold while preserving the units and rule. In LayerTime, change a matching network identity to a different one, or replace independently corroborated drone presence with a generic RF signal. The answer should change for the right reason.

## LoRA: how the model is adapted

Low-rank adaptation trains a comparatively small set of additional model weights while leaving the base model frozen. The included engine uses quantized base weights for QLoRA and masks prompt tokens out of the supervised loss. The target answer supplies the learning signal.

The ontology does not change the mathematics of LoRA. It guides the curriculum, the concepts exposed in the prompt, the target distinctions and the evaluation design. “Ontology-guided semantic LoRA training” describes that combination.

## A complete evidence chain

Source knowledge → ontology definitions → authored examples → admitted curriculum → training plan → applied updates → generated answers → interpretation review → qualification.

Each arrow can fail. A wrong definition produces wrong examples. A family leaking across splits makes evaluation misleading. A completed optimizer run can preserve previous errors. Schema checks do not catch all false explanations. Notella records this chain so failures can be investigated rather than hidden behind one success score.

## What makes a useful result

For the tool: another application can submit a well-defined curriculum and obtain an auditable training job. For the model: held-out, meaningfully different cases receive justified interpretations, including appropriate uncertainty. For deployment: independently reviewed evidence and relevant device/field tests support the intended use.

The first two-update integration probe established tool plumbing. The 742-update LayerTime run established actual training. Neither alone established useful field accuracy.

## Walk through the actual LayerTime ontology

The [LayerTime ontology walkthrough](layertime-ontology.md) explains all nine concepts, the four relationships, the proposed warning policy, ten output combinations and a runnable uncertainty-interval example. It distinguishes ontology meaning, policy choices, input assertions and demonstrated model behavior.
