from math import ceil
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from common.plotting import configure, save_figure


ROOT = Path(__file__).resolve().parents[2]
STYLES = {
    "np": (r"$np$", "#0072B2", "-"),
    "p": (r"$fp$", "#D55E00", "--"),
    "p_l2p": (r"$fp\_l2p$", "#009E73", "-."),
}
PLATFORMS = {"FT2000+": "ft2000", "KP920": "kp920"}


def plot_cdf(rows: pd.DataFrame, output: Path, show_legend: bool) -> None:
    configure()
    fig, axis = plt.subplots(figsize=(2.25, 2.25))
    upper = max(5, ceil(100 * rows["abs_error"].max() / 5) * 5)
    axis.axhline(90, color="#3A3A3A", linewidth=0.9, linestyle="--", zorder=1)
    for algorithm, (label, color, linestyle) in STYLES.items():
        errors = (100 * rows.loc[rows["algo"] == algorithm, "abs_error"]).sort_values()
        cumulative = [100 * index / len(errors) for index in range(len(errors) + 1)]
        axis.step(
            [0.0, *errors],
            cumulative,
            where="post",
            label=label,
            color=color,
            linestyle=linestyle,
            linewidth=1.25,
            alpha=0.95,
            zorder=2,
        )
    axis.set_xlabel("Absolute error (pp)", fontsize=8)
    axis.set_ylabel("Cumulative shapes (%)", fontsize=8)
    axis.set_xlim(0, upper)
    axis.set_ylim(0, 100)
    axis.grid(True, color="#B8B8B8", linewidth=0.45, linestyle=":", alpha=0.75)
    axis.tick_params(axis="both", labelsize=7, width=0.6, length=2.5)
    if show_legend:
        axis.legend(
            loc="lower right",
            frameon=True,
            facecolor="white",
            edgecolor="#4D4D4D",
            framealpha=0.9,
            fontsize=7.5,
            handletextpad=0.35,
        )
    fig.subplots_adjust(left=0.22, right=0.98, bottom=0.19, top=0.97)
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
    rows = pd.read_csv(ROOT / "processed_data/cache_model/heldout_v3_rows.csv")
    for platform, slug in PLATFORMS.items():
        platform_rows = rows[rows["platform"] == platform]
        for cache in ("l1d", "l2"):
            plot_cdf(
                platform_rows[platform_rows["cache"] == cache],
                ROOT / "outputs" / f"evaluation_{slug}_{cache}_cache_model_validation.pdf",
                platform == "FT2000+" and cache == "l1d",
            )


if __name__ == "__main__":
    main()
