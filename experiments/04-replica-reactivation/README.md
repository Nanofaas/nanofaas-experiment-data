# Keep-ready versus scale-to-zero

Paper mapping: Figure fig:reactivation.

## Selection

Only the final dispatch-fix campaign: five function runtimes, two treatments, three idle/reactivation cycles per treatment (30 cycles). Cycles reuse deployments and are not independent VM repetitions. Earlier lifecycle pilots are excluded.

## Files

- `derived/`: readable result summaries used in the main paper.
- `source-files.json`: SHA-256, byte count and original source for every retained input.
- `archive.json`: ordered release parts, sizes and checksums.
- The downloaded archive contains `raw/` and `derived/`, preserving measured values.

## Download and verify

From the repository root, with Python 3.11+ and `zstd` installed:

```sh
python3 scripts/fetch.py 04-replica-reactivation --output /path/to/data
python3 scripts/verify.py /path/to/data/04-replica-reactivation
```

Parts are at most 90 MiB. They form one continuous `.tar.zst` stream and are not
individually extractable. The download script checks each part and the full
archive, rejects unsafe member paths, then extracts the experiment directory.
The verification script checks every retained source byte and the result
populations; for QR and concurrency it also rechecks request-level metrics.

The dataset preserves the original experimental replication and limitations.
Missing observations are not synthesized, and configurations are not pooled
across superseded implementation versions.
