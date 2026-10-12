# End-to-End Sentence-Embedding Latency

LaTeX label: `fig:evaluation_rpi_end2end_performance`

Inputs: `processed_data/end2end/rpi_{t2,t4}.csv`

Each panel reports the all-MiniLM-L6-v2 sentence-embedding latency on the Raspberry Pi 3B with two and four threads. Bars are the mean per-sample speedup of EPPAv2 over each provider (`>1` means EPPAv2 is faster) and lines are the mean end-to-end latency in milliseconds.

```powershell
uv run python -B -m figures.fig_evaluation_rpi_end2end_performance.plot
```
