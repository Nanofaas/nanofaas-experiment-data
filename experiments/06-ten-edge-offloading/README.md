# Coordinated execution on ten edge nodes

Paper mapping: Section sec:ten-edge and Figures fig:ten-edge-dynamics / fig:ten-edge-results.

## Selection

Only the selected afternoon Oracle and corrected ARI pair, plus their common frozen Python allocation reference: 54 one-minute epochs and 142,242 edge-origin requests per run. The five-edge studies, the earlier uncorrected ARI run and the overnight pair are excluded. Retained raw files are the verified analysis inputs (request ledgers, outcomes, forecasts, plans, activation records and frozen reference), not a full VM diagnostic dump. All retained original bytes match the source provenance hashes.

## Files

- `derived/`: readable result summaries used in the main paper.
- `source-files.json`: SHA-256, byte count and original source for every retained input.
- `archive.json`: ordered release parts, sizes and checksums.
- The downloaded archive contains `raw/` and `derived/`, preserving measured values.

## Download and verify

From the repository root, with Python 3.11+ and `zstd` installed:

```sh
python3 scripts/fetch.py 06-ten-edge-offloading --output /path/to/data
python3 scripts/verify.py /path/to/data/06-ten-edge-offloading
```

Parts are at most 90 MiB. They form one continuous `.tar.zst` stream and are not
individually extractable. The download script checks each part and the full
archive, rejects unsafe member paths, then extracts the experiment directory.
The verification script checks every retained source byte and the result
populations; for QR and concurrency it also rechecks request-level metrics.

The dataset preserves the original experimental replication and limitations.
Missing observations are not synthesized, and configurations are not pooled
across superseded implementation versions.
