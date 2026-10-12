# TCC Reproducibility Data

This package contains the data and processing logic for the quantitative figures and evaluation tables in `A Theoretical Cache Analysis and Optimizations for Irregular Matrix Multiplication on ARMv8 Processors`.

## Contents

- `raw_data`: 41 allowlisted experiment archives and two gem5 task files used by active manuscript results.
- `processed_data`: analysis-ready per-shape, per-observation, and summary CSV files.
- `figures`: one directory for each active quantitative manuscript figure group.
- `tables`: data or generation logic for each active evaluation table.
- `common`: shared archive parsing, aggregation, and plotting code.
- `outputs`: regenerated manuscript panels and generated table data.
- `manifest.csv`: manuscript-label-to-artifact mapping.
- `checksums.sha256`: SHA-256 integrity records for all raw and processed data files.

The BLIS/Goto procedure, fine-grained packing, and EPPAv2 method diagrams are not included because they are explanatory diagrams rather than experimental results. Fully commented manuscript figures and their obsolete analysis paths are also excluded.

## Environment

Run every Python entry point through `uv`. The `pyproject.toml` in the parent reproducibility directory defines the standalone artifact environment.

## Rebuild Analysis Tables

```powershell
uv run python -B prepare_data.py
```

This command parses the packaged performance archives, applies the paper's padding correction and median aggregation, prepares the motivation PMU means, reconstructs the multi-thread summaries, recomputes cache-model diagnostics, and validates the PMU mechanism tables.

## Reproduce All Figures and Tables

```powershell
uv run python -B reproduce_all.py
```

Generated files are written to `outputs` using the filenames referenced by the manuscript.

## Validate the Package

```powershell
uv run python -B validate_package.py
```

## Data Levels

Single-thread, application, motivation, and multi-thread analysis tables are regenerated directly from packaged archives by `prepare_data.py`. Cache-model long-form rows and PMU mechanism detail tables are included as analysis-level records because their upstream generation requires the complete gem5/cache-model and multi-bundle PMU pipelines. Their raw archives remain in `raw_data`, and every value plotted in the manuscript is present in the corresponding analysis-level CSV.

## Aggregation Rules

- Single-thread and application performance use the median of repeated trials for each shape and implementation.
- Padded application shapes are rescaled to the original operation count before aggregation.
- Performance bars use the arithmetic mean of per-shape performance ratios.
- Performance lines use arithmetic mean GFLOP/s across shapes.
- Multi-thread curves use arithmetic mean GFLOP/s across 1,500 paired shapes.
- Cache-model CDFs use absolute miss-rate error in percentage points.
