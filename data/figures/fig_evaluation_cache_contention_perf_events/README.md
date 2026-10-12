# Hardware-Counter Mechanism Validation

LaTeX label: `fig:evaluation_cache_contention_perf_events`

Input: `processed_data/perf_events/mechanism_perf_event_summary.csv`

The cache-contention panel uses shape `6x360x2928` and L1D stores per kFLOP. The L2-prefetch panel uses shape `11x560x1792` and L2-miss stall cycles per kFLOP. Both panels overlay single-thread GFLOP/s.

```powershell
uv run python -B -m figures.fig_evaluation_cache_contention_perf_events.plot
```
