from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MaxNLocator

from common.metrics import performance_summary
from common.plotting import configure, save_figure


ROOT = Path(__file__).resolve().parents[2]
ALGORITHMS = (
    "cake_t1",
    "eigen_t1",
    "blis_t1",
    "openblas_t1",
    "armpl_t1",
    "blasfeo_t1",
    "libxsmm_t1",
    "libshalom_t1",
    "eppa_v3.25_t1",
)
NAMES = {
    "cake_t1": "CAKE",
    "eigen_t1": "Eigen",
    "blis_t1": "BLIS",
    "openblas_t1": "OpenBLAS",
    "armpl_t1": "ARMPL",
    "blasfeo_t1": "BLASFEO",
    "libxsmm_t1": "LIBXSMM",
    "libshalom_t1": "LibShalom",
    "eppa_v3.25_t1": "EPPAv2",
}
BASELINE_BLUE = "#4C78A8"
EPPA_ORANGE = "#E76F51"
PERFORMANCE_DARK = "#333333"
NEUTRAL_DARK = "#262626"
NEUTRAL_GRID = "#B8B8B8"


def plot_panel(summary: pd.DataFrame, output: Path) -> None:
    configure()
    algorithm_ids = summary["algorithm_id"].tolist()
    algorithm_names = [NAMES.get(name, name) for name in algorithm_ids]
    speedups = summary["speedup"]
    performance = summary["mean_gflops"]
    fig, speedup_axis = plt.subplots(figsize=(2.35, 1.45))
    bar_colors = [
        EPPA_ORANGE if name == "eppa_v3.25_t1" else BASELINE_BLUE
        for name in algorithm_ids
    ]
    bars = speedup_axis.bar(
        algorithm_names,
        speedups,
        width=0.78,
        color=bar_colors,
        edgecolor=NEUTRAL_DARK,
        linewidth=0.3,
        zorder=2,
    )
    speedup_axis.axhline(
        1.0,
        color=NEUTRAL_DARK,
        linestyle=(0, (2.5, 2.0)),
        linewidth=0.55,
        alpha=0.75,
        zorder=1,
    )
    speedup_axis.set_ylabel("Speedup over OpenBLAS", fontsize=7.2)
    speedup_axis.tick_params(
        axis="y", labelsize=6.2, width=0.5, length=2.3, pad=1.5
    )
    speedup_axis.tick_params(
        axis="x", labelsize=5.7, width=0.5, length=2.3, pad=1.0
    )
    speedup_axis.set_ylim(0, max(1.05, float(speedups.max()) * 1.18))
    speedup_axis.yaxis.set_major_locator(MaxNLocator(nbins=4, min_n_ticks=3))
    speedup_axis.set_axisbelow(True)
    plt.setp(
        speedup_axis.get_xticklabels(),
        rotation=42,
        ha="right",
        rotation_mode="anchor",
    )
    speedup_axis.bar_label(
        bars,
        fmt="%.2f",
        label_type="edge",
        padding=1.0,
        fontsize=5.1,
        color=NEUTRAL_DARK,
    )
    performance_axis = speedup_axis.twinx()
    performance_axis.plot(
        algorithm_names,
        performance,
        color=PERFORMANCE_DARK,
        marker="o",
        markerfacecolor="white",
        markeredgecolor=PERFORMANCE_DARK,
        markeredgewidth=0.7,
        linewidth=1.0,
        markersize=3.2,
        zorder=3,
    )
    performance_axis.set_ylabel("Performance (GFLOP/s)", fontsize=7.2)
    performance_axis.tick_params(
        axis="y", labelsize=6.2, width=0.5, length=2.3, pad=1.5
    )
    performance_axis.set_ylim(
        0, max(1.0, float(performance.max()) * 1.16)
    )
    performance_axis.yaxis.set_major_locator(MaxNLocator(nbins=4, min_n_ticks=3))
    speedup_axis.grid(
        axis="y",
        color=NEUTRAL_GRID,
        linestyle=(0, (2.5, 2.5)),
        linewidth=0.4,
        alpha=0.65,
    )
    speedup_axis.spines["top"].set_visible(False)
    performance_axis.spines["top"].set_visible(False)
    fig.subplots_adjust(left=0.17, right=0.83, bottom=0.31, top=0.91)
    save_figure(
        fig,
        output,
        creator="plot_application_figure.py",
        facecolor="white",
    )
    plt.close(fig)


def main() -> None:
    for workload in ("pystack", "gromacs", "scanpy"):
        for platform in ("kp920", "graviton2"):
            frame = pd.read_csv(
                ROOT / "processed_data/application" / workload / f"{platform}.csv"
            )
            summary = performance_summary(frame, ALGORITHMS, "openblas_t1")
            plot_panel(
                summary,
                ROOT / "outputs" / f"evaluate_{platform}_app_{workload}_performance.pdf",
            )


if __name__ == "__main__":
    main()
