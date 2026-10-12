# Cache-Contention Ablation

LaTeX label: `fig:evaluation_cache_contention_ablation`

Inputs: `processed_data/single_thread/cache_contention/*.csv`

The figure compares Full EPPAv2 with deterministic branch-removal variants on the same 3,000 shapes per platform. Bars are normalized to Full and lines are arithmetic mean GFLOP/s.

```powershell
uv run python -B -m figures.fig_evaluation_cache_contention_ablation.plot
```
