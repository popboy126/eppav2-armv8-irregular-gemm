# Cache-Model Validation

LaTeX label: `fig:evaluation_cache_model_validation`

Input: `processed_data/cache_model/heldout_v3_rows.csv`

The four panels contain empirical CDFs of absolute miss-rate error for 200 held-out shapes per kernel on Phytium 2000+-like and KunPeng920-like cache systems.

```powershell
uv run python -B -m figures.fig_evaluation_cache_model_validation.plot
```
