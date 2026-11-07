# Pressure-triggered forwarding to a fixed target

Paper mapping: Section extensions / Fixed-target forwarding.

## Selection

One consolidated campaign of 15 final arms: local-only, pressure forwarding and direct cloud at 20, 100, 300, 400 and 500 requests/s. The successful initial sweep and the subsequent 400/500 extension are combined, preserving each original source. The failed launch that preceded measurement is excluded. Each mode/rate has one run.

## Files

- `derived/`: readable result summaries used in the main paper.
- `source-files.json`: SHA-256, byte count and original source for every retained input.
- `archive.json`: ordered release parts, sizes and checksums.
- The downloaded archive contains `raw/` and `derived/`, preserving measured values.

## Download and verify

From the repository root, with Python 3.11+ and `zstd` installed:

```sh
python3 scripts/fetch.py 05-fixed-target-offloading --output /path/to/data
python3 scripts/verify.py /path/to/data/05-fixed-target-offloading
```

Parts are at most 90 MiB. They form one continuous `.tar.zst` stream and are not
individually extractable. The download script checks each part and the full
archive, rejects unsafe member paths, then extracts the experiment directory.
The verification script checks every retained source byte and the result
populations; for QR and concurrency it also rechecks request-level metrics.

The dataset preserves the original experimental replication and limitations.
Missing observations are not synthesized, and configurations are not pooled
across superseded implementation versions.
