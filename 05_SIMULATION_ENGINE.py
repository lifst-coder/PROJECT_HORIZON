"""
PROJECT HORIZON simulation engine

Monte Carlo scenario bands for a few technology and resource variables.
These are scenario bands under stated assumptions, not forecasts.

Data-centre electricity is anchored to the IEA figures recorded in
phase1_5/CLAIM_REGISTRY.csv (C002-C004) and to the IEA 2035 Base Case and range:

    2025: 485 TWh (estimate)       2030: about 945-950 TWh (Base Case)
    2035: about 1,200 TWh (Base Case), 700-1,700 TWh across IEA cases

Nothing beyond 2035 has an external anchor. Those years are extrapolation and
are flagged as such in the output.

Run:  python 05_SIMULATION_ENGINE.py            # writes 06_SIMULATION_SUMMARY.csv
      python 05_SIMULATION_ENGINE.py --full     # also writes 06_SIMULATION_RESULTS.csv
"""
import argparse

import numpy as np
import pandas as pd

YEARS = [2030, 2035, 2040, 2050]
DC_BASE_YEAR, DC_BASE_TWH = 2025, 485.0
ROBOT_BASE_YEAR, ROBOT_BASE_M = 2025, 5.08  # IFR World Robotics 2026: 5.079 million units

# (low, mode, high) for numpy's triangular sampler
DC_GROWTH_TO_2030 = (0.10, 0.144, 0.19)    # mode reproduces 485 -> about 950 TWh
DC_GROWTH_2030_2035 = (-0.06, 0.07, 0.12)   # median 4.8%/yr gives about 1,200 TWh; spans the IEA 2035 range of 700-1,700 TWh
DC_POST_2035_DAMPING = 0.5                  # assumption: growth halves after 2035
AI_SHARE_2030 = (0.30, 0.40, 0.50)
ROBOT_CAGR = (0.05, 0.07, 0.10)
HUMANOID_DOUBLING_MONTHS = (6, 9, 12)
HUMANOID_2025_M, HUMANOID_CAP_M = 0.016, 10.0
FUSION_START = (2032, 2035, 2045)
SMR_GW_2035 = (5, 20, 50)

VARIABLES = [
    "dc_electricity_twh",
    "ai_electricity_twh",
    "industrial_robot_stock_m",
    "humanoid_annual_prod_m",
    "smr_capacity_gw",
]


def dc_electricity(year, g1, g2):
    """Three-phase path: IEA-anchored to 2030, IEA-ranged to 2035, damped extrapolation after."""
    twh = DC_BASE_TWH * (1 + g1) ** (min(year, 2030) - DC_BASE_YEAR)
    if year > 2030:
        twh *= (1 + g2) ** (min(year, 2035) - 2030)
    if year > 2035:
        twh *= (1 + max(0.0, g2) * DC_POST_2035_DAMPING) ** (year - 2035)
    return twh


def run_simulation(n_sims=1000, seed=42):
    rng = np.random.default_rng(seed)
    rows = []
    for sim in range(n_sims):
        g1 = rng.triangular(*DC_GROWTH_TO_2030)
        g2 = rng.triangular(*DC_GROWTH_2030_2035)
        ai_share = rng.triangular(*AI_SHARE_2030)
        robot_cagr = rng.triangular(*ROBOT_CAGR)
        doubling = rng.triangular(*HUMANOID_DOUBLING_MONTHS)
        fusion_start = int(rng.triangular(*FUSION_START))
        smr_2035 = rng.triangular(*SMR_GW_2035)

        for year in YEARS:
            dc = dc_electricity(year, g1, g2)
            ai_share_y = min(0.65, ai_share + 0.015 * max(0, year - 2030))
            raw = HUMANOID_2025_M * 2 ** ((year - 2025) * 12 / doubling)
            rows.append(
                {
                    "sim": sim,
                    "year": year,
                    "dc_electricity_twh": round(dc, 1),
                    "ai_electricity_twh": round(dc * ai_share_y, 1),
                    "industrial_robot_stock_m": round(ROBOT_BASE_M * (1 + robot_cagr) ** (year - ROBOT_BASE_YEAR), 2),
                    "humanoid_annual_prod_m": round(raw / (1 + raw / HUMANOID_CAP_M), 3),
                    "fusion_online": int(year >= fusion_start),
                    "smr_capacity_gw": round(smr_2035 * max(0.0, (year - 2030) / 5.0), 1),
                }
            )
    return pd.DataFrame(rows)


def summarize(df):
    """p10 / p50 / p90 per year and variable, plus the share of runs with fusion online."""
    out = []
    for year, g in df.groupby("year"):
        for var in VARIABLES:
            p10, p50, p90 = np.percentile(g[var], [10, 50, 90])
            out.append(
                {
                    "year": year,
                    "variable": var,
                    "p10": round(float(p10), 2),
                    "p50": round(float(p50), 2),
                    "p90": round(float(p90), 2),
                    "basis": "extrapolation" if year > 2035 else "anchored_or_assumed",
                }
            )
        share = float(g["fusion_online"].mean())
        out.append({"year": year, "variable": "fusion_online_share", "p10": share, "p50": share, "p90": share,
                    "basis": "assumption"})
    return pd.DataFrame(out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PROJECT HORIZON Monte Carlo scenario bands")
    parser.add_argument("--sims", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--full", action="store_true", help="also write every run to 06_SIMULATION_RESULTS.csv")
    args = parser.parse_args()

    results = run_simulation(args.sims, args.seed)
    summary = summarize(results)
    summary.to_csv("06_SIMULATION_SUMMARY.csv", index=False)
    if args.full:
        results.to_csv("06_SIMULATION_RESULTS.csv", index=False)
    print(summary[summary["variable"] == "dc_electricity_twh"].to_string(index=False))
    print("Wrote 06_SIMULATION_SUMMARY.csv")
