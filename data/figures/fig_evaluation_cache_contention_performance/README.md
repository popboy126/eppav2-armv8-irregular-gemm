# Cache-Contention Performance

LaTeX label: `fig:evaluation_cache_contention_performance`

Inputs: `processed_data/single_thread/cache_contention/*.csv`

Each platform table contains 3,000 shapes. Bars are mean per-shape speedups over OpenBLAS and lines are arithmetic mean GFLOP/s.

```powershell
uv run python -B -m figures.fig_evaluation_cache_contention_performance.plot
```
