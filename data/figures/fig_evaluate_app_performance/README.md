# Application-Derived GEMM Performance

LaTeX label: `fig:evaluate_app_performance`

Inputs: `processed_data/application/{pystack,gromacs,scanpy}/{kp920,graviton2}.csv`

Bars are mean per-shape speedups over OpenBLAS and lines are arithmetic mean GFLOP/s for aligned GEMM records derived from PyStack, GROMACS, and Scanpy.

```powershell
uv run python -B -m figures.fig_evaluate_app_performance.plot
```
