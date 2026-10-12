from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
PLATFORMS = ("FT2000+", "KP920")
ALGORITHMS = ("np", "p", "p_l2p", "all")


def main() -> None:
    diagnostics = pd.read_csv(ROOT / "processed_data/cache_model/diagnostics.csv")
    rows = []
    for platform in PLATFORMS:
        for algorithm in ALGORITHMS:
            row = {"platform": platform, "kernel": algorithm}
            for cache in ("l1d", "l2"):
                match = diagnostics[
                    (diagnostics["platform"] == platform)
                    & (diagnostics["cache"] == cache)
                    & (diagnostics["algorithm"] == algorithm)
                ]
                if len(match) != 1:
                    raise ValueError(f"Expected one row for {platform}/{cache}/{algorithm}")
                values = match.iloc[0]
                row.update(
                    {
                        f"{cache}_mae_pp": 100 * values["mae"],
                        f"{cache}_rmse_pp": 100 * values["rmse"],
                        f"{cache}_pearson": values["pearson"],
                        f"{cache}_spearman": values["spearman"],
                    }
                )
            rows.append(row)
    output = ROOT / "outputs/table_evaluation_cache_model_validation.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(output, index=False, float_format="%.12g")


if __name__ == "__main__":
    main()
