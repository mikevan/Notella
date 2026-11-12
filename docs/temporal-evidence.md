# Temporal evidence and precautionary posture

The system must keep four judgments separate: what was observed, which events are associated, what causal explanation is supported, and what protective urgency is warranted. High urgency can coexist with uncertain causation. A single scalar called “confidence” obscures these differences.

## Initial evidence model

Each event needs an event ID, observation type, entity and location references, source and upstream provenance, timestamp, clock domain, synchronization method, time uncertainty, detector reliability scope and counterevidence. Reports copied from one source count as one evidential origin. Generic RF energy does not establish drone identity; a network outage does not establish intentional DDoS.

For event A and B with uncertainty bounds, compute the possible delay interval:

`[(B.time - B.uncertainty) - (A.time + A.uncertainty), (B.time + B.uncertainty) - (A.time - A.uncertainty)]`

Positive lower bound establishes order under the supplied clock assumptions. A positive interval entirely within the policy window supports the time-bounded association. Overlapping intervals leave order unresolved. An interval straddling the window leaves inclusion unresolved. Different unsynchronized clock domains cannot be subtracted without a justified alignment. `notella.correlation.temporal_link` implements the bounded arithmetic; callers must establish clock comparability first.

## Methods to investigate

1. Event matching: test identity, location, temporal order and plausible delay. Document windows before looking at outcomes, and include reversed, missing-time and unrelated-location controls.
2. Repeated sequences: estimate how often B follows A compared with matched baseline periods and comparable locations. Account for observation coverage, weather, scheduled activity, shared interference and other confounders. Report sample size and uncertainty rather than claiming significance from one pair.
3. Lagged association: examine cross-correlation or event-triggered hazard rates with a predeclared lag range. Autocorrelation, common causes and searching many lags can create misleading peaks. Temporal predictability, including Granger-style tests, does not by itself identify a causal mechanism.
4. Causal models: draw explicit competing graphs, such as hostile operation causing both disruption and drone presence, versus ordinary interference plus an unrelated aid drone. Observational association cannot identify all edges. Seek natural experiments or other defensible identification strategies; do not provoke unsafe events to collect evidence.
5. Calibrated warning models: if adequate representative labelled outcomes become available, compare likelihood ratios or calibrated prediction models against a base-rate baseline. Never invent priors, multiply dependent sensor likelihoods, or present arbitrary weighted scores as attack probability. Select thresholds against the consequences of missed and false warnings, with prospective validation.

These are research directions; only interval arithmetic is implemented in this release. No learned causal estimator or field-calibrated risk model is claimed.

## Camp warning teaching policy

Under the supplied credible ongoing-threat context, credible local deliberate disruption followed shortly by independently corroborated drone presence can warrant an extremely high **precautionary** posture. The model should communicate a possible looming attack as an urgent warning, name the supporting observations, and explicitly leave coordination, perpetrator and actual attack outcome unresolved.

The synthetic policy uses a 120-second example window. It is an adjustable policy parameter, not an established attack signature. Missing timestamps, clock overlap, generic RF, repeated social posts and benign explanations must change the explanation. Failure of the combined trigger does not erase a credible standalone drone hazard or the standing threat context. Recommend the established local civilian safety plan and trusted warning channels; do not invent routes, shelter guarantees or instructions to confront a suspected actor.

## Foundations and limits

[NIST SP 800-94](https://csrc.nist.gov/pubs/sp/800/94/final) describes intrusion-detection limitations, including false positives and negatives. [CDC causal-analysis guidance](https://www.cdc.gov/field-epi-manual/php/chapters/analyze-interpret-data.html) discusses temporal sequence, alternative evidence and causal interpretation. [CDC intervention guidance](https://www.cdc.gov/field-epi-manual/php/chapters/interventions.html) separates the weight of evidence from the consequences of acting or delaying.

The CDC material supplies general reasoning principles from epidemiology; applying those principles to RF/drone warnings is a project design inference, not validation of this use case. These sources do not establish that the proposed disruption/drone sequence predicts an attack.
