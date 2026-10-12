# EPPAv2 ARMv8 Irregular GEMM Artifact

This repository contains the reproducibility artifact for the manuscript "EPPAv2: Optimizing Irregular Matrix Multiplication on ARM Processors via Cache-Aware Packing and Prefetching."

The public project name is `eppav2-armv8-irregular-gemm`.

## Repository Contents

- `data/` contains the raw and processed experimental data, figure and table generation scripts, integrity checksums, and generated manuscript outputs.
- `code/` is reserved for the implementation corresponding to the manuscript.

Detailed mappings from manuscript labels to data, scripts, and outputs are provided in `data/README.md` and `data/manifest.csv`.

## Code Availability

The implementation corresponding to `code/` will be provided after the manuscript is accepted. The directory is intentionally empty in the submission version of this artifact.

## Environment

The artifact requires Python 3.13 and uses `uv` for environment management. From the repository root, create the project environment with:

```powershell
uv sync
```

The exact direct dependency versions are declared in `pyproject.toml`.

## Rebuild Processed Data

```powershell
uv run python -B data/prepare_data.py
```

This command rebuilds the analysis-ready tables from the packaged archives and refreshes the raw and processed data checksums.

## Reproduce Figures and Tables

```powershell
uv run python -B data/reproduce_all.py
```

Generated manuscript panels and table data are written to `data/outputs/`.

## Validate the Artifact

```powershell
uv run python -B data/validate_package.py
```

Validation checks the Python sources, artifact manifest, file inventory, expected outputs, and SHA-256 records for raw and processed data.

## Scope

The artifact covers the quantitative figures and evaluation tables used by the manuscript. Explanatory architecture and method diagrams are excluded because they are not generated from experimental data. See `data/README.md` for the complete inclusion and exclusion policy.
