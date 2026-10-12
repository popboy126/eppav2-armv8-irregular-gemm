from __future__ import annotations

from pathlib import Path
from typing import Mapping, Sequence

import pandas as pd

from common.metrics import performance_summary
from common.plotting import plot_bar_line


BASELINE_ALGORITHMS = (
    "cake_t1",
    "eigen_t1",
    "blis_t1",
    "openblas_t1",
    "armpl_t1",
    "blasfeo_t1",
    "libxsmm_t1",
    "libshalom_t1",
    "eppa_v2_date_t1",
    "eppa_v3.25_t1",
)
BASELINE_NAMES = {
    "cake_t1": "CAKE",
    "eigen_t1": "EIGEN",
    "blis_t1": "BLIS",
    "openblas_t1": "OpenBLAS",
    "armpl_t1": "ARMPL",
    "blasfeo_t1": "BLASFEO",
    "libxsmm_t1": "LIBXSMM",
    "libshalom_t1": "LibShalom",
    "eppa_v2_date_t1": "EPPA",
    "eppa_v3.25_t1": "EPPAv2",
}
PLATFORMS = {"ft2000": "ft2000", "kp920": "kp920", "graviton2": "graviton2"}


def plot_performance_set(
    data_dir: Path,
    output_dir: Path,
    output_names: Mapping[str, str],
    algorithms: Sequence[str] = BASELINE_ALGORITHMS,
    names: Mapping[str, str] = BASELINE_NAMES,
    baseline: str = "openblas_t1",
    bar_ylabel: str = "Speedup",
) -> None:
    for platform in PLATFORMS:
        frame = pd.read_csv(data_dir / f"{platform}.csv")
        summary = performance_summary(frame, algorithms, baseline)
        plot_bar_line(
            summary,
            names,
            output_dir / output_names[platform],
            bar_ylabel,
        )
