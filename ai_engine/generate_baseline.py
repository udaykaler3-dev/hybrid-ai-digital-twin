"""
=========================================================
GASONET DIGITAL TWIN
STATION BASELINE GENERATOR
=========================================================

This module generates station-specific baseline values
from historical compressor operating data.

The generated baseline is used by the Health Engine
instead of manually selected thresholds.

Author : Uday Kaler
=========================================================
"""

# ==========================================================
# IMPORTS
# ==========================================================

import json
import pandas as pd
from pathlib import Path


# ==========================================================
# FILE PATHS
# ==========================================================

DATA_FILE = Path("data/cleaned_engineered_data.csv")

OUTPUT_FILE = Path("ai_engine/station_baseline.json")
# ==========================================================
# LOAD HISTORICAL DATA
# ==========================================================

def load_historical_data() -> pd.DataFrame:
    """
    Load historical compressor operating data.
    """

    df = pd.read_csv(DATA_FILE)

    print(f"✓ Total Records Loaded : {len(df)}")

    return df
# ==========================================================
# REMOVE INVALID OPERATING RECORDS
# ==========================================================

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove physically invalid operating records.

    Rules
    -----
    1. Discharge Pressure must be greater than Suction Pressure.
    2. Flow must be positive.
    3. Current must be positive.
    4. Voltage must be positive.
    5. HMR Hours must be positive.
    """

    df = df.copy()

    df = df[
        df["Discharge press"] >
        df["Suction press"]
    ]

    df = df[
        df["Flow Rate"] > 0
    ]

    df = df[
        df["Current"] > 0
    ]

    df = df[
        df["Voltage"] > 0
    ]

    df = df[
        df["HMR_Hours"] > 0
    ]

    print(f"✓ Valid Records : {len(df)}")

    return df.reset_index(drop=True)
# ==========================================================
# CALCULATE STATION BASELINE
# ==========================================================

def calculate_baseline(df: pd.DataFrame) -> dict:
    """
    Calculate station-specific baseline values
    from historical compressor data.

    Percentile-based statistics are used to
    reduce the influence of outliers.
    """

    # ---------------------------------------------
    # Pressure Rise
    # ---------------------------------------------

    pressure_rise = (
        df["Discharge press"] -
        df["Suction press"]
    )

    # ---------------------------------------------
    # Baseline Dictionary
    # ---------------------------------------------

    baseline = {

        # -----------------------------------------
        # Flow (kg/hr)
        # -----------------------------------------

        "flow_optimum":
            round(df["Flow Rate"].median(), 2),

        "flow_min":
            round(df["Flow Rate"].quantile(0.10), 2),

        "flow_max":
            round(df["Flow Rate"].quantile(0.90), 2),

        # -----------------------------------------
        # Pressure Rise (bar)
        # -----------------------------------------

        "pressure_rise_optimum":
            round(pressure_rise.median(), 2),

        "pressure_rise_min":
            round(pressure_rise.quantile(0.10), 2),

        "pressure_rise_max":
            round(pressure_rise.quantile(0.90), 2),

        # -----------------------------------------
        # Current (A)
        # -----------------------------------------

        "current_optimum":
            round(df["Current"].median(), 2),

        "current_warning":
            round(df["Current"].quantile(0.90), 2),

        "current_critical":
    round(
        max(
            df["Current"].quantile(0.95) + 2.0,
            df["Current"].max()
        ),
        2
    ),

        # -----------------------------------------
        # Voltage (V)
        # -----------------------------------------

        "voltage_nominal":
            round(df["Voltage"].median(), 2),

        "voltage_tolerance":
    round(
        max(
            5.0,
            (
                df["Voltage"].quantile(0.90)
                -
                df["Voltage"].quantile(0.10)
            ) / 2
        ),
        2
    ),

        # -----------------------------------------
        # HMR (hours/day)
        # -----------------------------------------

        "hmr_optimum":
            round(df["HMR_Hours"].median(), 2),

        "hmr_warning":
            round(df["HMR_Hours"].quantile(0.90), 2),

        "hmr_critical":
            round(df["HMR_Hours"].quantile(0.95), 2)

    }

    return baseline
# ==========================================================
# SAVE BASELINE
# ==========================================================

def save_baseline(baseline: dict) -> None:
    """
    Save baseline values to a JSON file.
    """

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w") as file:
        json.dump(
            baseline,
            file,
            indent=4
        )

    print(f"✓ Baseline saved to {OUTPUT_FILE}")
    # ==========================================================
# MAIN
# ==========================================================

def main():

    print("\nGenerating Gasonet Station Baseline...\n")

    df = load_historical_data()

    df = clean_data(df)

    baseline = calculate_baseline(df)

    save_baseline(baseline)

    print("\nGenerated Baseline\n")

    for key, value in baseline.items():

        print(f"{key:<25} : {value}")

    print("\n✓ Station baseline generation completed.")


if __name__ == "__main__":

    main()