# API reference — v1

The Python service and HTTP transport share the same artifact model. Core functions raise ValidationError for invalid data and FileNotFoundError for a missing artifact. The HTTP transport maps these to JSON errors. The small Client wrapper raises standard urllib HTTP errors.

## Artifact envelope and identity

Creation of an ontology, curriculum, plan or evaluation returns:

```json
{"id": "64-character-sha256-identifier", "artifact": {"example": "content"}}
```

The illustrative identifier above is not a valid actual ID. IDs are lowercase hex SHA-256 fingerprints of UTF-8 canonical JSON: sorted keys, compact separators, Unicode preserved, nonfinite numbers rejected. GET returns the artifact itself, not the creation envelope. Job IDs are separate 32-character hex identifiers.

Supported artifact kinds are ontologies, curricula, plans and evaluations. Stored content is checked against its ID on retrieval. The store creates complete temporary files and hard-links them into their content-addressed names without overwriting existing artifacts. Use a local filesystem supporting hard links; the tested installation is NTFS.

## Register an ontology

Python: `api.register_ontology(ontology)`

HTTP: `POST /v1/ontologies`, body = ontology object.

| Field | Required type | Meaning |
|---|---|---|
| name | nonempty string | Human-readable domain/profile name |
| version | nonempty string | Human-managed ontology version |
| concepts | nonempty object | Concept identifier → nonempty definition string |
| relations | array | Objects containing exactly subject, predicate and object |
| instruction | nonempty string | Task and interpretation instructions |
| outputSchema | object | Supported JSON Schema subset for target objects |

Each relation endpoint must name a concept; predicate is a nonempty string. An empty relations array is accepted, although meaningful relationships are central to the intended method. Arbitrary extra ontology metadata is preserved in the artifact but is not automatically placed in the prompt; put model-relevant policy in instruction or input explicitly.

The supported output-schema keywords are type, properties, required, additionalProperties (boolean), items, enum, const, minLength, maxLength, minItems, maxItems, uniqueItems, minimum, maximum and description. Types are object, array, string, integer, number, boolean and null. Type unions, references, regex patterns, combinators and formats are unsupported. Unsupported nested keywords are rejected at registration. Schema validation establishes structure, not truth.

## Compile a curriculum

Python: `api.compile(ontology_id, examples, exclusions=None)`

HTTP: `POST /v1/curricula`:

```json
{"ontologyId": "<actual ontology ID>", "examples": [], "excludedPromptHashes": []}
```

The empty examples array shown for shape must be replaced with at least one training example. A real record is demonstrated in [curriculum design](curricula.md).

| Example field | Required content |
|---|---|
| id | Unique nonempty string within the curriculum |
| family | Nonempty original-scenario/source-family identifier |
| split | train, validation or test |
| concepts | Nonempty array of ontology concept identifiers |
| source | Provenance object described below |
| input | Nonempty model-visible user text |
| target | JSON value satisfying outputSchema |

Source fields id, kind, reference, permission and labelAuthor are required nonempty strings. kind must be synthetic, document or field. Training examples additionally require trainingAllowed=true. A held-out example need not have training admission. File paths and URLs in source.reference are recorded as provenance; the API does not fetch them or verify their content automatically.

The compiled artifact contains formatVersion, ontologyId, examples, split counts, excluded hashes, limitations and releaseEligible=false. Each example contains rendered messages, its original family/split/source, output schema and prompt fingerprint. Supervised messages contain an assistant target; never include that target when performing model inference.

## Create a training plan

Python: `api.plan(curriculum_id, base_model, steps=100, rank=16, learning_rate=0.00005)`

HTTP: `POST /v1/plans`:

```json
{"curriculumId": "<actual curriculum ID>", "baseModel": "qwen3-4b", "steps": 60, "rank": 16, "learningRate": 0.00005}
```

steps must be an integer from 1 to 100000. rank must be an integer from 1 to 128. learningRate must be finite, greater than zero and at most 0.001. Boolean values are not accepted as integers. baseModel is a nonempty alias; existence and allowlisting are checked at job submission.

A plan records intended settings and split counts. It does not start training. Current defaults are developmental implementation defaults, not empirically optimal settings.

## Start and inspect a job

Python: `jobs.start(plan_id)` on a configured Jobs backend, or `client.start_job(plan_id)` over HTTP.

HTTP: `POST /v1/jobs`, body = `{"planId":"<actual plan ID>"}`.

The backend must be configured with a local engine, a Python executable and a model-alias map. A separate validation split is required. The training request cannot override these server-owned paths. Successful submission returns a job object rather than an artifact envelope. Possible statuses are starting, running, completed and failed. During a normal live-server lifecycle, running transitions to completed for exit code zero or failed for a nonzero exit.

`GET /v1/jobs/{id}` returns persisted state including planId, createdAt, PID, command, source hashes and, after child exit, exitCode and finishedAt. Paths and process information are intentionally available to authenticated local developer clients. Remote multi-tenant use is not supported.

The GPU lock is exclusive to the store. A request encountering it returns a validation error; there is no queue. Job submission is not idempotent. See [training recovery](training.md) before handling an interrupted server or stale-looking lock.

## Evaluate supplied predictions

Python: `api.evaluate(curriculum_id, predictions, split='test')`.

HTTP: `POST /v1/evaluations`:

```json
{
  "curriculumId": "<actual curriculum ID>",
  "split": "test",
  "predictions": {"test-warm": {"finding": "An illustrative finding", "exceedsThreshold": true, "limitation": "Illustrative limitation"}}
}
```

predictions maps exact example IDs to already-parsed JSON values, not JSON strings. IDs must belong to the selected validation/test split. Missing predictions are retained as present=false and do not pass schema checks. Unknown or wrong-split IDs reject the request. The API does not generate predictions or invoke a judge model.

The result reports per-example presence, schema validity, exactTargetMatch and any schema error; aggregate total, schemaPasses and exactTargetMatches; semanticAccuracyMeasured=false and releaseEligible=false. Exact matches are a diagnostic, not a semantic scoring method.

## Retrieve artifacts and API discovery

`GET /v1/{kind}/{id}` returns and verifies an artifact. Python: `api.get(kind, identity)` or `client.get(kind, identity)`.

`GET /v1/openapi.json` returns the generated OpenAPI 3.1 description. It is authenticated. `GET /health` is public and reports product, API version and basic process health.

## Errors and transport limits

| Status | Example cause | Action |
|---|---|---|
| 400 | Missing field, wrong split, invalid schema, unavailable backend/model, held GPU lock | Correct the request or inspect the running job |
| 401 | Missing or incorrect bearer token | Supply the server's token |
| 404 | Missing artifact/job or unknown route | Check kind and exact ID |
| 413 | Missing/zero or over-4-MiB request length | Supply a supported JSON body; keep version-0.1 curricula bounded |
| 500 | Unexpected local server/storage failure | Inspect local state; preserve evidence |

Error bodies have `{"error":"message"}`. There is no CORS support, streaming upload, chunked request handling, public hosting or pagination in 0.1. This is a small local developer service. Large datasets should be handled through a future bounded import API rather than removing request limits without resource planning.


## Hash-bound interpretation reviews

POST /v1/interpretation-reviews records explicit reviewer judgments against exact output text and criteria. GET /v1/interpretation-reviews/{id} retrieves them. This complements structural evaluations and does not automate semantic truth. See the [runnable review tutorial](semantic-reviews.md) for field definitions and Python/HTTP examples.


## Python contract extensions

`notella.lineage.summarize_lineage(labels, registry)` returns a model-facing origin topology and a separate provenance receipt. Unknown/unreviewed labels never become invented independent origins.

`notella.output_contracts.inspect_output(output, schema, allowed_states, fields)` checks exact generated text, schema and declared field combinations. It returns violations and a hash, never a repaired answer or ground-truth certification.

The source-checkout LayerTime adapter provides `profiles.layertime.decision_contract.project_observation` and `inspect_warning_output`. These explicitly project relevant observations and check necessary evidence relations. They are profile helpers, not automatic behavior of every core endpoint and not additional HTTP routes. See the [runnable contract tutorial](input-output-contracts.md).

## Optional local teacher Python API

Use `notella.teachers.LocalTeacher` and `teaching_candidate` for a loopback Colibri/OpenAI-compatible teacher. This is a Python interface, not a new HTTP route. Candidate receipts pin the provider source hash, request identity and saved-result integrity hash, and always start pending review. See [Tutorial 10](teachers.md) for runnable examples, explicit retries, model-intake limits and the separate curriculum-admission boundary.

The optional `notella.teacher_reviews.record_teacher_review` Python API binds criterion judgments to an exact pending teacher candidate. Its `id`/`artifact` return envelope follows other artifact APIs. Review never grants training permission. See [the teacher tutorial](teachers.md).

## Scenario Python API

`notella.scenarios.scenario_output_schema(concepts)`, `validate_scenario(ontology, scenario)`, `validate_scenario_set(ontology, scenarios)`, `evidence_counts(evidence_by_id, refs)` and `compile_scenario_examples(ontology, scenarios)` provide the first assessment-scenario contract. Validation receipts identify what was checked and keep semantic correctness/source authenticity false. Export does not grant admission or start training. See [Tutorial 11](scenarios.md) for runnable examples, fields and failures. No new scenario HTTP route is implemented.
