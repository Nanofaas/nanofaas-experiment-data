# nanofaas experiment data

Selected experimental data for the main [nanofaas manuscript](https://github.com/Nanofaas/nanofaas-paper-overleaf).
Each directory represents one experiment. Only the final measurement versions
used by the main paper are included; all repetitions contributing to those
results are retained. Incremental platform-comparison and fixed-target-offload
runs are organized as single campaigns, with original provenance preserved.

## Experiments

| Directory | Retained measurements | Compressed size |
|---|---|---:|
| [JVM/native builds and retained-module costs](experiments/01-module-cost) | 3 independent blocks, 24 arms | 10.7 MiB |
| [Cross-platform QR service](experiments/02-platform-comparison) | 25 runs, 104 plotted phases, 13 table rows | 21.8 MiB |
| [Concurrency adaptation with fixed replica counts](experiments/03-concurrency-adaptation) | 24 evaluation runs + 4 calibration runs | 83.4 MiB |
| [Keep-ready versus scale-to-zero](experiments/04-replica-reactivation) | 5 runtimes × 2 treatments × 3 cycles | 0.8 MiB |
| [Pressure-triggered forwarding to a fixed target](experiments/05-fixed-target-offloading) | 3 modes × 5 rates, 15 arms | 52.9 MiB |
| [Coordinated execution on ten edge nodes](experiments/06-ten-edge-offloading) | Oracle + ARI, 54 epochs each, common Python reference | 29.6 MiB |

## Download

Readable summaries, manifests, and provenance are stored in Git. Compressed
measurement archives are public assets of the
[paper-main-v1 release](https://github.com/Nanofaas/nanofaas-experiment-data/releases/tag/paper-main-v1),
so cloning this repository does not download all raw measurements. No Git LFS or
access to the original private repositories is needed.

Install Python 3.11+ and `zstd`, then choose an experiment:

```sh
python3 scripts/fetch.py 02-platform-comparison --output /path/to/data
python3 scripts/verify.py /path/to/data/02-platform-comparison
```

The same commands apply to all six directory names. Download destinations must
be new: the script does not overwrite existing data. Allow space for both the
compressed archive and its extracted files; the complete collection is about
8 GiB uncompressed.

Each experiment has one deterministic `.tar.zst` stream, split when necessary
into ordered parts of at most **90 MiB**. In this release each compressed stream
fits in a single part. `archive.json` records public download URLs, part sizes,
part SHA-256 checksums and the reconstructed stream checksum. `source-files.json`
records the original provenance and checksum of every retained input. The
verifier checks those bytes; it also recalculates the QR latency percentiles and
throughputs and the concurrency request counts from the published event logs.

## Selection and interpretation

- Superseded nanofaas configurations, failed setup attempts, diagnostic pilots,
  the earlier five-edge campaign and the uncorrected/overnight ten-edge runs are
  excluded. Container images, VM provisioning state, and unrelated manuscript
  material are not part of this deposit.
- Warm-up and idle observations are retained where they belong to the selected
  measurement runs; they are distinguished from measurement phases.
- A consolidated directory does not imply identical configuration, equal
  replication, or independent hosts. The platform campaign retains three runs
  for each selected baseline and each nanofaas runtime, but one per final Spin
  rate. Replica-reactivation cycles reuse deployments. Offloading runs are
  single observations per condition.
- The ten-edge archive contains the verified inputs required by the main-paper
  analysis, including raw request and control-plan records and the frozen Python
  reference. It does not contain the complete original VM diagnostic dumps.
- Historical source paths and implementation identifiers in provenance identify
  the data actually used. They do not require access to those source repositories
  to download or check this deposit.

`paper-binding.json` identifies the manuscript revision and relevant local-input
hashes at packaging time. `verification.json` records the performed checks.
The deposit preserves measurements; it does not rerun deployments or experiments.
