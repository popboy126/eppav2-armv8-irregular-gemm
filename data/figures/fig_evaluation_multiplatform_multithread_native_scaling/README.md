# Multi-Thread Scaling

LaTeX label: `fig:evaluation_multiplatform_multithread_native_scaling`

Inputs: `processed_data/multithread/kp920.csv` and `processed_data/multithread/graviton2.csv`

Strong and weak scaling report arithmetic mean GFLOP/s over 1,500 paired shapes at 1, 2, 4, 8, and 16 threads.

```powershell
uv run python -B -m figures.fig_evaluation_multiplatform_multithread_native_scaling.plot
```
