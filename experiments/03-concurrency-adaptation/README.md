# Concurrency adaptation with fixed replica counts

Paper mapping: Table tab:concurrency and Figure fig:concurrency.

## Selection

The final 24 evaluation runs: four policies × two scenarios × three repetitions on separate VM pairs. Four calibration runs are retained separately because they underpin the calibrated fixed limit. Qualification/debug attempts and earlier experiments are excluded. Extended diagnostic summaries changed after archival and are not used by the main paper; they are excluded. Original request ledgers and telemetry match the frozen archive hashes.

## Files

- `derived/`: readable result summaries used in the main paper.
- `source-files.json`: SHA-256, byte count and original source for every retained input.
- `archive.json`: ordered release parts, sizes and checksums.
- The downloaded archive contains `raw/` and `derived/`, preserving measured values.

## Download and verify

From the repository root, with Python 3.11+ and `zstd` installed:

```sh
python3 scripts/fetch.py 03-concurrency-adaptation --output /path/to/data
python3 scripts/verify.py /path/to/data/03-concurrency-adaptation
```

Parts are at most 90 MiB. They form one continuous `.tar.zst` stream and are not
individually extractable. The download script checks each part and the full
archive, rejects unsafe member paths, then extracts the experiment directory.
The verification script checks every retained source byte and the result
populations; for QR and concurrency it also rechecks request-level metrics.

The dataset preserves the original experimental replication and limitations.
Missing observations are not synthesized, and configurations are not pooled
across superseded implementation versions.
