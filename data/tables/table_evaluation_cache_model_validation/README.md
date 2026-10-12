# Cache-Model Diagnostics

LaTeX label: `table:evaluation_cache_model_validation`

Input: `processed_data/cache_model/diagnostics.csv`

The generator combines L1D and L2 diagnostics, converts MAE and RMSE to percentage points, and writes `outputs/table_evaluation_cache_model_validation.csv`.

```powershell
uv run python -B -m tables.table_evaluation_cache_model_validation.generate
```
