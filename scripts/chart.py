#!/usr/bin/env python3
"""
Generate a 6-panel workout timeline chart from Intervals.icu activity stream data.

Panels:
  1. Raw power (watts)
  2. 30s smoothed power, zone-colored
  3. Heart rate (bpm) with zone bands
  4. Cadence (rpm)
  5. Elevation (m)
  6. W'bal (kJ) — computed via Waterworth differential model

Usage:
  # File-based input (preferred for large datasets):
  python3 scripts/chart.py --input /tmp/streams.json --output /tmp/workout_chart.png

  # The input JSON file should have this structure:
  # {
  #   "power": [...],  "hr": [...],  "cadence": [...],
  #   "altitude": [...],  "time": [...],
  #   "ftp": 325,  "wprime": 25000,
  #   "hr_zones": [137, 152, 159, 170, 175, 180, 189],
  #   "laps": [600, 1200]  // optional, lap times in seconds
  # }
"""

import argparse
import json
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np


# --- W'bal computation (Waterworth differential model) ---

def compute_wbal(power: np.ndarray, cp: float, wprime: float) -> np.ndarray:
    """Compute W'bal using the Waterworth differential model.

    At each second:
      - If power > CP: W'bal decreases by (power - CP) joules
      - If power <= CP: W'bal reconstitutes toward W' with first-order kinetics

    Reference: Waterworth (2013), used by GoldenCheetah as default.
    """
    n = len(power)
    wbal = np.empty(n)
    wbal[0] = wprime

    for i in range(1, n):
        p = power[i]
        if p > cp:
            wbal[i] = wbal[i - 1] - (p - cp)
        else:
            wbal[i] = wbal[i - 1] + (wprime - wbal[i - 1]) * (
                1 - np.exp(-(cp - p) / wprime)
            )
        wbal[i] = np.clip(wbal[i], 0, wprime)

    return wbal


# --- Zone coloring ---

def get_zone_colors():
    """Coggan 7-zone colors matching typical training software."""
    return [
        "#aaaaaa",  # Z1 Active Recovery — gray
        "#2ecc71",  # Z2 Endurance — green
        "#f1c40f",  # Z3 Tempo — yellow
        "#e67e22",  # Z4 Threshold — orange
        "#e74c3c",  # Z5 VO2max — red
        "#9b59b6",  # Z6 Anaerobic — purple
        "#2c3e50",  # Z7 Neuromuscular — dark
    ]


def power_to_zone_index(power_val: float, ftp: float) -> int:
    """Map a power value to a Coggan zone index (0-6)."""
    pct = power_val / ftp * 100
    if pct < 55:
        return 0
    elif pct < 75:
        return 1
    elif pct < 90:
        return 2
    elif pct < 105:
        return 3
    elif pct < 120:
        return 4
    elif pct < 150:
        return 5
    else:
        return 6


def smooth(data: np.ndarray, window: int = 30) -> np.ndarray:
    """Rolling average with same-length output."""
    if len(data) < window:
        return data
    kernel = np.ones(window) / window
    smoothed = np.convolve(data, kernel, mode="same")
    # Fix edges
    for i in range(window // 2):
        smoothed[i] = np.mean(data[: i + window // 2 + 1])
        smoothed[-(i + 1)] = np.mean(data[-(i + window // 2 + 1) :])
    return smoothed


# --- Chart generation ---

def generate_chart(
    power: np.ndarray,
    hr: np.ndarray,
    cadence: np.ndarray,
    altitude: np.ndarray,
    time_seconds: np.ndarray,
    ftp: float,
    wprime: float,
    hr_zones: list[float],
    output_path: str,
    laps: list[int] | None = None,
):
    """Generate the 6-panel workout timeline chart."""

    # Compute derived data
    power_smooth = smooth(power, 30)
    wbal = compute_wbal(power, ftp, wprime)
    wbal_kj = wbal / 1000.0

    # Time axis in minutes
    time_min = time_seconds / 60.0

    # Zone boundaries in watts
    zone_pcts = [0, 55, 75, 90, 105, 120, 150]
    zone_watts = [ftp * p / 100 for p in zone_pcts]
    zone_colors = get_zone_colors()
    zone_names = ["Z1", "Z2", "Z3", "Z4", "Z5", "Z6", "Z7"]

    # HR zone colors (lighter versions)
    hr_zone_colors = [
        "#d5f5e3",  # Z1
        "#abebc6",  # Z2
        "#f9e79f",  # Z3
        "#f5cba7",  # Z4
        "#f1948a",  # Z5
        "#d2b4de",  # Z6
        "#aab7b8",  # Z7
    ]

    # --- Figure setup ---
    fig, axes = plt.subplots(
        6, 1,
        figsize=(20, 14),
        sharex=True,
        gridspec_kw={"height_ratios": [2.5, 2.5, 2, 1.5, 1.5, 2]},
    )
    fig.patch.set_facecolor("#1a1a2e")

    for ax in axes:
        ax.set_facecolor("#16213e")
        ax.tick_params(colors="#cccccc", labelsize=11)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_color("#444444")
        ax.spines["left"].set_color("#444444")

    # --- Panel 1: Raw Power ---
    ax1 = axes[0]
    ax1.plot(time_min, power, color="#7777ff", alpha=0.5, linewidth=0.4)
    ax1.plot(time_min, power_smooth, color="#aaaaff", linewidth=1.0)
    ax1.set_ylabel("Power (W)", color="#cccccc", fontsize=12)
    ax1.set_ylim(0, max(np.percentile(power, 99.5) * 1.1, ftp * 1.5))
    # FTP line
    ax1.axhline(y=ftp, color="#e74c3c", linestyle="--", alpha=0.5, linewidth=0.8)
    ax1.text(time_min[-1] * 0.99, ftp + 5, f"FTP {ftp}W", color="#e74c3c",
             fontsize=10, ha="right", alpha=0.7)

    # --- Panel 2: Zone-colored 30s power ---
    ax2 = axes[1]
    # Plot zone-colored segments
    for i in range(len(time_min) - 1):
        zone_idx = power_to_zone_index(power_smooth[i], ftp)
        ax2.fill_between(
            time_min[i : i + 2],
            0,
            power_smooth[i : i + 2],
            color=zone_colors[zone_idx],
            alpha=0.7,
            linewidth=0,
        )
    ax2.set_ylabel("30s Power", color="#cccccc", fontsize=12)
    ax2.set_ylim(0, max(np.percentile(power_smooth, 99.5) * 1.1, ftp * 1.5))
    # Zone boundary lines
    for w, name in zip(zone_watts[1:], zone_names[1:]):
        if w < ax2.get_ylim()[1]:
            ax2.axhline(y=w, color="#ffffff", linestyle=":", alpha=0.15, linewidth=0.5)

    # --- Panel 3: Heart Rate ---
    ax3 = axes[2]
    # HR zone bands
    hr_boundaries = [0] + list(hr_zones)
    for j in range(len(hr_boundaries) - 1):
        ax3.axhspan(hr_boundaries[j], hr_boundaries[j + 1],
                     color=hr_zone_colors[j], alpha=0.15)
    ax3.plot(time_min, hr, color="#e74c3c", linewidth=0.8, alpha=0.85)
    hr_smooth = smooth(hr, 30)
    ax3.plot(time_min, hr_smooth, color="#ff6b6b", linewidth=1.2)
    ax3.set_ylabel("HR (bpm)", color="#cccccc", fontsize=12)
    valid_hr = hr[hr > 0]
    if len(valid_hr) > 0:
        ax3.set_ylim(max(valid_hr.min() - 10, 60), min(valid_hr.max() + 10, 210))

    # --- Panel 4: Cadence ---
    ax4 = axes[3]
    ax4.plot(time_min, cadence, color="#e056c1", linewidth=0.5, alpha=0.5)
    cad_smooth = smooth(cadence, 15)
    ax4.plot(time_min, cad_smooth, color="#e056c1", linewidth=1.0)
    ax4.set_ylabel("Cadence", color="#cccccc", fontsize=12)
    valid_cad = cadence[cadence > 0]
    if len(valid_cad) > 0:
        ax4.set_ylim(0, min(valid_cad.max() + 20, 150))

    # --- Panel 5: Elevation ---
    ax5 = axes[4]
    ax5.fill_between(time_min, altitude, color="#888888", alpha=0.4)
    ax5.plot(time_min, altitude, color="#aaaaaa", linewidth=0.8)
    ax5.set_ylabel("Elev (m)", color="#cccccc", fontsize=12)
    if altitude.max() - altitude.min() > 1:
        ax5.set_ylim(altitude.min() - 5, altitude.max() + 15)

    # --- Panel 6: W'bal ---
    ax6 = axes[5]
    wprime_kj = wprime / 1000.0
    # Color gradient: green when full, red when depleted
    for i in range(len(time_min) - 1):
        pct = wbal_kj[i] / wprime_kj
        r = 1 - pct
        g = pct
        color = (min(r, 1), min(g, 1), 0.2)
        ax6.fill_between(time_min[i : i + 2], 0, wbal_kj[i : i + 2],
                         color=color, alpha=0.6, linewidth=0)
    ax6.plot(time_min, wbal_kj, color="#2ecc71", linewidth=1.0)
    ax6.set_ylabel("W'bal (kJ)", color="#cccccc", fontsize=12)
    ax6.set_ylim(0, wprime_kj * 1.05)
    ax6.axhline(y=wprime_kj * 0.25, color="#e74c3c", linestyle="--",
                alpha=0.4, linewidth=0.8)
    ax6.text(time_min[-1] * 0.99, wprime_kj * 0.25 + 0.3, "25% W'",
             color="#e74c3c", fontsize=10, ha="right", alpha=0.5)
    ax6.set_xlabel("Time (minutes)", color="#cccccc", fontsize=12)

    # --- Lap boundaries (if provided) ---
    if laps:
        for lap_sec in laps:
            lap_min = lap_sec / 60.0
            for ax in axes:
                ax.axvline(x=lap_min, color="#ffffff", linestyle="-",
                           alpha=0.25, linewidth=0.8)

    # --- Final layout ---
    plt.tight_layout(h_pad=0.3)
    plt.savefig(output_path, dpi=130, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close()

    return output_path


# --- CLI ---

def main():
    parser = argparse.ArgumentParser(description="Generate workout timeline chart")
    parser.add_argument("--input", required=True,
                        help="Path to JSON file with stream data and parameters")
    parser.add_argument("--output", required=True, help="Output PNG file path")

    args = parser.parse_args()

    with open(args.input) as f:
        data = json.load(f)

    power = np.array(data["power"], dtype=float)
    hr = np.array(data["hr"], dtype=float)
    cadence = np.array(data["cadence"], dtype=float)
    altitude = np.array(data["altitude"], dtype=float)
    time_seconds = np.array(data["time"], dtype=float)

    output = generate_chart(
        power=power,
        hr=hr,
        cadence=cadence,
        altitude=altitude,
        time_seconds=time_seconds,
        ftp=float(data["ftp"]),
        wprime=float(data["wprime"]),
        hr_zones=data["hr_zones"],
        output_path=args.output,
        laps=data.get("laps"),
    )

    print(f"Chart saved to {output}")


if __name__ == "__main__":
    main()
