# Cross-platform QR service

Paper mapping: Table tab:platform-results and Figure fig:platform-throughput.

## Selection

One consolidated campaign with 25 definitive runs and 104 plotted load phases: FunLess, tinyFaaS, Serverledge, Fn and faasd (three runs each); nanofaas JVM/native (three runs each at a final 300 requests/s); Spin (one run each at final rates 250, 260, 270 and 300 requests/s). Only the four-CPU/4-GiB runs used in the current results are included. Earlier nanofaas versions, two-CPU runs, the direct reference, and superseded Spin trials are excluded. Original source identifiers remain in run-index.json; aggregation does not imply identical configuration or replication across platforms.

## Files

- `derived/`: readable result summaries used in the main paper.
- `source-files.json`: SHA-256, byte count and original source for every retained input.
- `archive.json`: ordered release parts, sizes and checksums.
- The downloaded archive contains `raw/` and `derived/`, preserving measured values.

## Download and verify

From the repository root, with Python 3.11+ and `zstd` installed:

```sh
python3 scripts/fetch.py 02-platform-comparison --output /path/to/data
python3 scripts/verify.py /path/to/data/02-platform-comparison
```

Parts are at most 90 MiB. They form one continuous `.tar.zst` stream and are not
individually extractable. The download script checks each part and the full
archive, rejects unsafe member paths, then extracts the experiment directory.
The verification script checks every retained source byte and the result
populations; for QR and concurrency it also rechecks request-level metrics.

The dataset preserves the original experimental replication and limitations.
Missing observations are not synthesized, and configurations are not pooled
across superseded implementation versions.
