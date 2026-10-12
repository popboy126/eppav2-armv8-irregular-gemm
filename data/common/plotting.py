from __future__ import annotations

from pathlib import Path
from typing import Mapping

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.pyplot import rcParams
from matplotlib.ticker import MaxNLocator


BLUE = "#0072B2"
VERMILLION = "#D55E00"
DARK = "#262626"
GRID = "#B8B8B8"


def configure() -> None:
    rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
            "mathtext.fontset": "stix",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "axes.linewidth": 0.6,
        }
    )


def save_figure(fig, output: Path, creator: str | None = None, **kwargs) -> None:
    if creator is None:
        fig.savefig(output, **kwargs)
    else:
        fig.savefig(output, metadata={"Creator": creator}, **kwargs)


def plot_bar_line(
    summary,
    names: Mapping[str, str],
    output: Path,
    bar_ylabel: str,
    bar_colors: Mapping[str, str] | None = None,
) -> None:
    configure()
    labels = [names.get(value, value) for value in summary["algorithm_id"]]
    colors = [
        bar_colors.get(value, BLUE) if bar_colors else BLUE
        for value in summary["algorithm_id"]
    ]
    fig, left = plt.subplots(figsize=(2.35, 1.45))
    bars = left.bar(
        labels,
        summary["speedup"],
        width=0.86,
        color=colors,
        edgecolor=DARK,
        linewidth=0.35,
        alpha=0.88,
        zorder=2,
    )
    left.set_ylabel(bar_ylabel, fontsize=7.5, color=BLUE)
    left.tick_params(axis="y", labelcolor=BLUE, labelsize=6.5, width=0.6, length=2.5)
    left.tick_params(axis="x", labelsize=6.0, width=0.6, length=2.5, pad=1)
    left.set_ylim(0, max(1.0, float(summary["speedup"].max())) * 1.25)
    left.yaxis.set_major_locator(MaxNLocator(nbins=4, min_n_ticks=3))
    left.grid(axis="y", color=GRID, linestyle="--", linewidth=0.45, alpha=0.7)
    left.set_axisbelow(True)
    plt.setp(left.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    left.bar_label(
        bars,
        fmt="%.2f",
        label_type="edge",
        padding=-7,
        fontsize=5.5,
        color="white",
    )
    right = left.twinx()
    right.plot(
        labels,
        summary["mean_gflops"],
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
    right.tick_params(
        axis="y", labelcolor=VERMILLION, labelsize=6.5, width=0.6, length=2.5
    )
    right.set_ylim(0, max(1.0, float(summary["mean_gflops"].max())) * 1.25)
    right.yaxis.set_major_locator(MaxNLocator(nbins=4, min_n_ticks=3))
    left.spines["top"].set_visible(False)
    right.spines["top"].set_visible(False)
    left.spines["left"].set_color(BLUE)
    right.spines["right"].set_color(VERMILLION)
    fig.subplots_adjust(left=0.16, right=0.85, bottom=0.29, top=0.97)
    output.parent.mkdir(parents=True, exist_ok=True)
    save_figure(fig, output, facecolor="white")
    plt.close(fig)
