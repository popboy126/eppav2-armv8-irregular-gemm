from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MaxNLocator

from common.plotting import configure, save_figure


ROOT = Path(__file__).resolve().parents[2]
BLUE = "#0072B2"
VERMILLION = "#D55E00"
DARK = "#262626"
GRID = "#B8B8B8"
LABELS = {
    "tvm": "TVM",
    "openblas": "OpenBLAS",
    "armpl": "ARMPL",
    "blis": "BLIS",
    "libshalom": "LibShalom",
    "eppav2": "EPPAv2",
}


def plot_panel(frame: pd.DataFrame, output: Path) -> None:
    configure()
    providers = frame["provider"].tolist()
    labels = [LABELS[p] for p in providers]
    latency_ms = frame["mean_latency_ms"].tolist()
    speedup = frame["mean_speedup"].tolist()
    x = list(range(len(labels)))
    fig, left = plt.subplots(figsize=(2.6, 1.9))
    bars = left.bar(
        x,
        speedup,
        width=0.62,
        color=BLUE,
        edgecolor=DARK,
        linewidth=0.35,
        alpha=0.88,
        zorder=2,
    )
    left.set_ylabel("Speedup", fontsize=7.5, color=BLUE)
    left.tick_params(axis="y", labelcolor=BLUE, labelsize=6.5, width=0.6, length=2.5)
    left.tick_params(axis="x", labelsize=6.5, width=0.6, length=2.5, pad=1)
    left.set_ylim(0, max(speedup) * 1.25)
    left.yaxis.set_major_locator(MaxNLocator(nbins=4, min_n_ticks=3))
    left.set_axisbelow(True)
    left.set_xticks(x)
    left.set_xticklabels(labels)
    plt.setp(left.get_xticklabels(), rotation=30, ha="right", rotation_mode="anchor")
    left.bar_label(
        bars,
        fmt="%.2f",
        label_type="edge",
        padding=1.5,
        fontsize=6,
        color=DARK,
    )
    right = left.twinx()
    right.plot(
        x,
        latency_ms,
        color=VERMILLION,
        marker="o",
        markerfacecolor="white",
        markeredgecolor=VERMILLION,
        markeredgewidth=0.8,
        linewidth=1.1,
        markersize=3.5,
        zorder=3,
    )
    right.set_ylabel("Latency (ms)", fontsize=7.5, color=VERMILLION)
    right.tick_params(
        axis="y", labelcolor=VERMILLION, labelsize=6.5, width=0.6, length=2.5
    )
    right.set_ylim(0, max(latency_ms) * 1.22)
    right.yaxis.set_major_locator(MaxNLocator(nbins=4, min_n_ticks=3))
    left.grid(axis="y", color=GRID, linestyle="--", linewidth=0.45, alpha=0.7)
    left.spines["top"].set_visible(False)
    right.spines["top"].set_visible(False)
    left.spines["left"].set_color(BLUE)
    right.spines["right"].set_color(VERMILLION)
    fig.subplots_adjust(left=0.16, right=0.85, bottom=0.27, top=0.94)
    output.parent.mkdir(parents=True, exist_ok=True)
    save_figure(fig, output, facecolor="white", bbox_inches="tight", pad_inches=0.01)
    plt.close(fig)


def main() -> None:
    for slug in ("rpi_t2", "rpi_t4"):
        frame = pd.read_csv(ROOT / "processed_data/end2end" / f"{slug}.csv")
        threads = slug.rsplit("_", 1)[-1]
        plot_panel(
            frame,
            ROOT / "outputs" / f"evaluation_rpi_end2end_{threads}_performance.pdf",
        )


if __name__ == "__main__":
    main()
