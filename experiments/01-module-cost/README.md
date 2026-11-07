# JVM/native builds and retained-module costs

Paper mapping: Resource table (tab:module-arms) and Figure fig:module-cost.

## Selection

Three final independent VM blocks, eight configurations per block (JVM/native × Base/C/S/CS). All 24 arms are retained. Failed launches and the incomplete predecessor campaign are excluded.

## Files

- `derived/`: readable result summaries used in the main paper.
- `source-files.json`: SHA-256, byte count and original source for every retained input.
- `archive.json`: ordered release parts, sizes and checksums.
- The downloaded archive contains `raw/` and `derived/`, preserving measured values.

## Download and verify

From the repository root, with Python 3.11+ and `zstd` installed:

```sh
python3 scripts/fetch.py 01-module-cost --output /path/to/data
python3 scripts/verify.py /path/to/data/01-module-cost
```

Parts are at most 90 MiB. They form one continuous `.tar.zst` stream and are not
individually extractable. The download script checks each part and the full
archive, rejects unsafe member paths, then extracts the experiment directory.
The verification script checks every retained source byte and the result
populations; for QR and concurrency it also rechecks request-level metrics.

The dataset preserves the original experimental replication and limitations.
Missing observations are not synthesized, and configurations are not pooled
across superseded implementation versions.
