# Runtime-document archive: morphology checkpoint

This archive preserves 3,217 runtime documents and metadata files, including training/validation data, corpus and plan records, model outputs, logs, metrics, source snapshots, tokenizer assets, scheduler/scaler/RNG metadata and test results. Identical bytes share one blob: 664 blobs preserve 485,335,522 original bytes in 35,906,307 archived bytes.

- `index.json` maps every original relative path to its exact bytes, SHA-256, length and modification time.
- `blobs/` contains the byte-exact data. Git attributes prevent line-ending conversion.
- `excluded-binaries.json` inventories 43 model-weight/optimizer binaries retained locally, with hashes, sizes and paths. No binary weights were published.
- `summary.json` records completeness counts and the automated scan boundary. Inspected source records are synthetic. The credential-pattern check found no matches; it is not a formal security guarantee.

Verify without extracting:

```powershell
python checkpoint/inspect_morphology_archive.py --verify
```

Inspect the source path in `index.json`, then extract one file to a new destination:

```powershell
python checkpoint/inspect_morphology_archive.py --source runtime/scenario-model-v5/training-result.json --output runtime/review-training-result.json
```

The extractor verifies the hash and refuses to overwrite an existing output. Archived pickle-format training metadata is preserved for provenance; the inspector does not deserialize it. Historical process IDs/statuses are snapshots, not live job controls. Reproduction must use the exact historical sources/configuration and separately available licensed model assets; do not substitute current root code and claim identical provenance.
