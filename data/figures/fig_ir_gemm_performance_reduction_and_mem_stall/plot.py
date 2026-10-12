from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.pyplot import rcParams

from common.plotting import save_figure


ROOT = Path(__file__).resolve().parents[2]
FONT_SIZE = 95
LINE_WIDTH = 8
LABELS = (
    ("libshalom", "LibShalom", "orange"),
    ("openblas", "OpenBLAS", "green"),
    ("blis", "BLIS", "red"),
    ("blasfeo", "BLASFEO", "cyan"),
    ("libxsmm", "LIBXSMM", "brown"),
    ("eppa_p", "fp", "gray"),
)


def plot_performance(frame: pd.DataFrame, output: Path) -> None:
    rcParams["xtick.labelsize"] = FONT_SIZE
    rcParams["ytick.labelsize"] = FONT_SIZE
    fig = plt.figure(figsize=(50, 25))
    axis = fig.add_subplot(1, 1, 1)
    for algorithm, label, color in LABELS:
        rows = frame[frame["bin_label"] == algorithm].sort_values(by=["k"])
        axis.plot(
            rows["k"],
            100 * rows["performance"] / 41.6,
            color=color,
            linestyle="solid",
            label=label,
            linewidth=LINE_WIDTH,
            markersize=4 * LINE_WIDTH,
        )
    axis.legend(loc="upper right", ncols=3, frameon=False, fontsize=FONT_SIZE)
    axis.set_xlabel("K", fontsize=FONT_SIZE)
    axis.set_ylabel("% of Peak", fontsize=FONT_SIZE)
    plt.tight_layout(pad=0)
    save_figure(fig, output, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def plot_stall_cycles(frame: pd.DataFrame, event: str, output: Path) -> None:
    rcParams["xtick.labelsize"] = FONT_SIZE
    rcParams["ytick.labelsize"] = FONT_SIZE
    fig = plt.figure(figsize=(50, 25), facecolor="white")
    axis = fig.add_subplot(1, 1, 1)
    for algorithm, label, color in LABELS:
        rows = frame[frame["bin_label"] == algorithm].sort_values(by=["k"])
        axis.plot(
            rows["k"],
            100 * rows[event] / rows["cpu-cycles"],
            color=color,
            linestyle="solid",
            label=label,
            linewidth=LINE_WIDTH,
            markersize=4 * LINE_WIDTH,
        )
    _, upper = axis.get_ylim()
    axis.set_ylim(top=1.12 * upper)
    axis.legend(loc="upper left", ncols=3, frameon=False, fontsize=FONT_SIZE)
    axis.set_xlabel("K", fontsize=FONT_SIZE)
    axis.set_ylabel("% of Cycles", fontsize=FONT_SIZE)
    plt.tight_layout(pad=0)
    save_figure(fig, output, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main() -> None:
    frame = pd.read_csv(
        ROOT / "processed_data/motivation/performance_degradation_kp920.csv"
    )
    plot_performance(
        frame,
        ROOT / "outputs/performance_analysis_performance_degrade_on_kp920.pdf",
    )
    for event in ("mem_stall_l1miss", "mem_stall_l2miss"):
        plot_stall_cycles(
            frame,
            event,
            ROOT
            / "outputs"
            / f"performance_analysis_ratio_cycles_of_event_{event}_on_kp920.pdf",
        )


if __name__ == "__main__":
    main()
