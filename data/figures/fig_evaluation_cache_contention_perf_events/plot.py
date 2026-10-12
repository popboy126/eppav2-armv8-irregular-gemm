from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import MaxNLocator

from common.plotting import BLUE, DARK, GRID, VERMILLION, configure, save_figure


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
    "eppa_v2_date_t1",
    "eppa_v3.25_t1",
)
PANELS = {
    "cache_contention": (
        "6x360x2928",
        "l1d_cache_wr_per_kflop",
        "L1D stores/kFLOP",
    ),
    "l2_stream_prefetch": (
        "11x560x1792",
        "mem_stall_l2miss_per_kflop",
        "L2-miss stall cycles/kFLOP",
    ),
}


def plot_panel(frame: pd.DataFrame, panel: str, output: Path) -> None:
    shape, metric, ylabel = PANELS[panel]
    rows = frame[frame["shape_key"] == shape].set_index("bin_label").loc[list(ALGORITHMS)]
    labels = rows["kernel"].tolist()
    values = rows[metric].astype(float).to_numpy()
    performance = rows["gflops"].astype(float).to_numpy()
    positions = np.arange(len(labels))
    configure()
    fig, left = plt.subplots(figsize=(3.35, 1.72))
    bars = left.bar(
        positions,
        values,
        width=0.70,
        color=BLUE,
        edgecolor=DARK,
        linewidth=0.35,
        alpha=0.88,
        zorder=2,
    )
    left.set_ylabel(ylabel, fontsize=7.5, color=BLUE)
    left.set_xticks(positions, labels)
    left.tick_params(axis="y", labelcolor=BLUE, labelsize=6.5, width=0.6, length=2.5)
    left.tick_params(axis="x", labelsize=6.0, width=0.6, length=2.5, pad=1)
    for label in left.get_xticklabels():
        label.set_rotation(28)
        label.set_ha("right")
        label.set_rotation_mode("anchor")
    left.set_ylim(0, max(values) * 1.24)
    left.yaxis.set_major_locator(MaxNLocator(nbins=4, min_n_ticks=3))
    left.set_axisbelow(True)
    metric_max = max(values)
    for bar, value in zip(bars, values):
        is_tall = value >= metric_max * 0.15
        if is_tall:
            left.text(
                bar.get_x() + bar.get_width() / 2,
                value - metric_max * 0.025,
                f"{value:.1f}",
                ha="center",
                va="top",
                rotation=90,
                fontsize=5.5,
                color="white",
                zorder=4,
            )
            continue
        left.text(
            bar.get_x() + bar.get_width() / 2,
            value + metric_max * 0.015,
            f"{value:.1f}",
            ha="center",
            va="bottom",
            fontsize=5.5,
            color=DARK,
            zorder=4,
        )
    right = left.twinx()
    right.plot(
        positions,
        performance,
        color=VERMILLION,
        marker="o",
        markerfacecolor="white",
        markeredgecolor=VERMILLION,
        markeredgewidth=0.8,
        linewidth=1.1,
        markersize=3.5,
        zorder=3,
    )
    right.set_ylabel("Performance (GFLOP/s)", fontsize=7.5, color=VERMILLION)
    right.tick_params(axis="y", labelcolor=VERMILLION, labelsize=6.5, width=0.6, length=2.5)
    right.set_ylim(0, max(performance) * 1.24)
    right.yaxis.set_major_locator(MaxNLocator(nbins=4, min_n_ticks=3))
    left.grid(axis="y", color=GRID, linestyle="--", linewidth=0.45, alpha=0.7)
    left.spines["top"].set_visible(False)
    right.spines["top"].set_visible(False)
    left.spines["left"].set_color(BLUE)
    right.spines["right"].set_color(VERMILLION)
    fig.subplots_adjust(left=0.14, right=0.86, bottom=0.30, top=0.89)
    output.parent.mkdir(parents=True, exist_ok=True)
    save_figure(fig, output, facecolor="white")
    plt.close(fig)


def main() -> None:
    frame = pd.read_csv(
        ROOT / "processed_data/perf_events/mechanism_perf_event_summary.csv"
    )
    for panel in PANELS:
        plot_panel(
            frame,
            panel,
            ROOT / "outputs" / f"evaluation_kp920_mechanism_perf_events_{panel}.pdf",
        )


if __name__ == "__main__":
    main()
