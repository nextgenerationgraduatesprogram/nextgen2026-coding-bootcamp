from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def create_demand_plots(
    hourly_profile_csv: Path,
    high_demand_share_csv: Path,
    output_dir: Path,
) -> dict:
    """Generate and save plots based on analysis results."""
    # Load analysis results
    profile = pd.read_csv(hourly_profile_csv)
    share = pd.read_csv(high_demand_share_csv)

    output_dir.mkdir(parents=True, exist_ok=True)

    # Plot 1: Mean hourly rentals by day type
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    for day_type, group in profile.groupby("day_type"):
        ax1.plot(group["hour"], group["mean_rentals"], marker="o", label=day_type)

    ax1.set_title("Mean hourly bike rentals by day type")
    ax1.set_xlabel("Hour of day")
    ax1.set_ylabel("Mean rentals")
    ax1.legend()
    ax1.grid(alpha=0.3)
    fig1.tight_layout()

    plot1_path = output_dir / "hourly_demand_by_day_type.png"
    fig1.savefig(plot1_path, dpi=150)
    plt.close(fig1)

    # Plot 2: High-demand share by hour
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.bar(share["hour"], share["high_demand_share"])
    ax2.set_title("Share of high-demand observations by hour")
    ax2.set_xlabel("Hour of day")
    ax2.set_ylabel("High-demand share")
    ax2.grid(axis="y", alpha=0.3)
    fig2.tight_layout()

    plot2_path = output_dir / "high_demand_share_by_hour.png"
    fig2.savefig(plot2_path, dpi=150)
    plt.close(fig2)

    return {
        "plot1": str(plot1_path),
        "plot2": str(plot2_path),
    }


def run_report(cfg) -> dict:
    """Run the report stage with a composed configuration."""
    results_dir = Path(cfg.paths.results_dir)
    hourly_profile_csv = results_dir / "hourly_profile.csv"
    high_demand_share_csv = results_dir / "high_demand_share_by_hour.csv"

    plots = create_demand_plots(
        hourly_profile_csv=hourly_profile_csv,
        high_demand_share_csv=high_demand_share_csv,
        output_dir=results_dir,
    )

    return {"plots": plots}
