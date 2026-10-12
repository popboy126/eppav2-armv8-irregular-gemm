# Performance Degradation and Memory Stalls

LaTeX label: `fig:ir_gemm_performance_reduction_and_mem_stall`

Input: `processed_data/motivation/performance_degradation_kp920.csv`

The performance panel reports percent of the KunPeng920 single-core peak of 41.6 GFLOP/s. The stall panels report each event divided by CPU cycles. All panels use `M=20`, `N=64`, and varying `K`.

```powershell
uv run python -B -m figures.fig_ir_gemm_performance_reduction_and_mem_stall.plot
```
