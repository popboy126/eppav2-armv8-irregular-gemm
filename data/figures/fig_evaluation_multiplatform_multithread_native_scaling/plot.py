from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import MaxNLocator

from common.plotting import GRID, configure, save_figure


ROOT = Path(__file__).resolve().parents[2]
THREADS = (1, 2, 4, 8, 16)
STYLES = {
    "eppav2": ("EPPAv2", "#0072B2", "o", 1.8),
    "armpl": ("ARMPL", "#CC79A7", "D", 1.05),
    "openblas": ("OpenBLAS", "#56B4E9", "P", 1.05),
    "blis": ("BLIS", "#E69F00", "v", 1.05),
    "eigen": ("Eigen", "#6A6A6A", "X", 1.05),
    "cake": ("CAKE", "#009E73", "^", 1.05),
}


def plot_panel(frame: pd.DataFrame, scaling: str, output: Path) -> None:
    configure()
    positions = np.arange(len(THREADS))
    fig, axis = plt.subplots(figsize=(3.35, 2.45))
    for algorithm, (name, color, marker, width) in STYLES.items():
        rows = (
            frame[
                (frame["scaling_type"] == scaling)
                & (frame["algorithm_id"] == algorithm)
            ]
            .set_index("threads")
            .loc[list(THREADS)]
        )
        axis.plot(
            positions,
            rows["mean_gflops"],
            label=name if scaling == "strong" else None,
            color=color,
            marker=marker,
            linewidth=width,
            markersize=4.2 if algorithm == "eppav2" else 3.4,
            markerfacecolor="white",
            markeredgewidth=0.8,
        )
    axis.set_xticks(positions, [str(value) for value in THREADS])
    axis.set_xlabel("Threads", fontsize=8)
    axis.set_ylabel(f"{scaling.capitalize()} performance (GFLOP/s)", fontsize=8)
    axis.tick_params(axis="both", labelsize=7, width=0.6, length=2.5)
    axis.grid(axis="y", color=GRID, linestyle="--", linewidth=0.45, alpha=0.7)
    axis.set_axisbelow(True)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.yaxis.set_major_locator(MaxNLocator(nbins=5, min_n_ticks=4))
    axis.set_ylim(bottom=0)
    if scaling == "strong":
        axis.legend(frameon=False, fontsize=5.7, ncol=2, loc="upper left")
    fig.subplots_adjust(left=0.18, right=0.98, bottom=0.20, top=0.97)
    output.parent.mkdir(parents=True, exist_ok=True)
    save_figure(
        fig,
        output,
        facecolor="white",
        bbox_inches="tight",
        pad_inches=0.02,
    )
    plt.close(fig)


def main() -> None:
    for platform in ("kp920", "graviton2"):
        frame = pd.read_csv(ROOT / "processed_data/multithread" / f"{platform}.csv")
        for scaling in ("strong", "weak"):
            plot_panel(
                frame,
                scaling,
                ROOT
                / "outputs"
                / f"evaluation_{platform}_multithread_native_{scaling}_performance.pdf",
            )


if __name__ == "__main__":
    main()
