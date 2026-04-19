from __future__ import annotations

from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "measurements.csv"
RESULTS_DIR = PROJECT_ROOT / "results"
SUMMARY_PATH = RESULTS_DIR / "summary_by_group.csv"
FIGURE_PATH = RESULTS_DIR / "mean_by_group.png"


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["group"] = df["group"].astype(str).str.strip().str.upper()
    df["reading"] = pd.to_numeric(df["reading"], errors="coerce")
    return df.dropna(subset=["group", "reading"])


def make_summary() -> pd.DataFrame:
    df = load_data()
    return (
        df.groupby("group", as_index=False)
        .agg(mean_reading=("reading", "mean"), n=("reading", "size"))
        .sort_values("group")
    )


def save_plot(summary: pd.DataFrame) -> None:
    RESULTS_DIR.mkdir(exist_ok=True)

    ax = summary.plot(kind="bar", x="group", y="mean_reading", legend=False)
    ax.set_ylabel("Mean reading")
    ax.set_title("Mean reading by group")

    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(FIGURE_PATH, dpi=150)
    plt.close(fig)


def main() -> None:
    RESULTS_DIR.mkdir(exist_ok=True)

    summary = make_summary()
    summary.to_csv(SUMMARY_PATH, index=False)
    save_plot(summary)

    print("Wrote results/summary_by_group.csv")
    print("Wrote results/mean_by_group.png")


if __name__ == "__main__":
    main()
