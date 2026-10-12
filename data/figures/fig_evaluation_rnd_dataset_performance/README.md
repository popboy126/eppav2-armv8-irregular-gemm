# Random-Set Performance

LaTeX label: `fig:evaluation_rnd_dataset_performance`

Inputs: `processed_data/single_thread/random/*.csv`

Each platform table contains the same 8,000 shapes. Bars are mean per-shape speedups over OpenBLAS and lines are arithmetic mean GFLOP/s.

```powershell
uv run python -B -m figures.fig_evaluation_rnd_dataset_performance.plot
```
