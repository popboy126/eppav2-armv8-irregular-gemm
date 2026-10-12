from __future__ import annotations

from pathlib import Path
from typing import Sequence

import numpy as np
import pandas as pd


def performance_summary(
    frame: pd.DataFrame, algorithms: Sequence[str], baseline: str
) -> pd.DataFrame:
    missing = [name for name in algorithms if name not in frame.columns]
    if missing:
        raise ValueError(f"Missing performance columns: {missing}")
    rows = []
    for algorithm in algorithms:
        rows.append(
            {
                "algorithm_id": algorithm,
                "mean_gflops": frame[algorithm].mean(),
                "speedup": (frame[algorithm] / frame[baseline]).mean(),
            }
        )
    return pd.DataFrame(rows)


def _diagnostic_row(group: pd.DataFrame, algorithm: str) -> dict:
    error = group["predicted"] - group["actual"]
    ranks_actual = group["actual"].rank(method="average")
    ranks_predicted = group["predicted"].rank(method="average")
    return {
        "algorithm": algorithm,
        "count": len(group),
        "mae": error.abs().mean(),
        "rmse": np.sqrt((error**2).mean()),
        "bias": error.mean(),
        "pearson": group["actual"].corr(group["predicted"]),
        "spearman": ranks_actual.corr(ranks_predicted),
        "p90_abs_error": error.abs().quantile(0.9),
    }


def cache_diagnostics(rows: pd.DataFrame) -> pd.DataFrame:
    output = []
    for (platform, cache), cache_rows in rows.groupby(
        ["platform", "cache"], sort=False
    ):
        for algorithm, algorithm_rows in cache_rows.groupby("algo", sort=False):
            output.append(
                {"platform": platform, "cache": cache, **_diagnostic_row(algorithm_rows, algorithm)}
            )
        output.append(
            {"platform": platform, "cache": cache, **_diagnostic_row(cache_rows, "all")}
        )
    return pd.DataFrame(output)


def read_csv(path: Path, required: Sequence[str]) -> pd.DataFrame:
    frame = pd.read_csv(path)
    missing = sorted(set(required) - set(frame.columns))
    if missing:
        raise ValueError(f"{path} is missing columns {missing}")
    return frame
