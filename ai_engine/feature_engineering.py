import pandas as pd
import numpy as np
import os

# ==========================================
# LOAD DATASET
# ==========================================

INPUT_FILE = "data/validated_data.csv"
OUTPUT_FILE = "data/engineered_data.csv"

df = pd.read_csv(INPUT_FILE)

print("=" * 60)
print("FEATURE ENGINEERING")
print("=" * 60)

# ==========================================
# ENGINEERING FEATURES
# ==========================================

# Pressure Difference
df["Pressure_Difference"] = (
    df["Discharge press"] - df["Suction press"]
)

# Pressure Ratio
df["Pressure_Ratio"] = (
    df["Discharge press"] /
    df["Suction press"].replace(0, np.nan)
)

# Electrical Power Index
df["Electrical_Load"] = (
    df["Voltage"] *
    df["Current"]
)

# Compressor Delivery Flow
RATED_FLOW = 1000

df["Compressor Delivery Flow"] = (
    df["Flow Rate"] /
    RATED_FLOW
)

# Specific Energy
df["Specific_Energy"] = (
    df["KWH Diff"] /
    df["Flow Rate"].replace(0, np.nan)
)
# ==========================================
# NEW TARGET
# ==========================================

df["Power_kW"] = (
    df["KWH Diff"] /
    df["HMR_Hours"].replace(0, np.nan)
)

# Energy Per Hour
df["Energy_per_Hour"] = (
    df["KWH Diff"] /
    df["HMR_Hours"].replace(0, np.nan)
)

# Compressor Load Index
df["Load_Index"] = (
    df["Pressure_Ratio"] *
    df["Flow_Utilization"]
)

# ==========================================
# CLEAN
# ==========================================

df.replace(
    [np.inf, -np.inf],
    np.nan,
    inplace=True
)

df.fillna(
    0,
    inplace=True
)

# ==========================================
# SAVE
# ==========================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nEngineering Features Created Successfully.\n")

print(df.head())

print("\nSaved As")

print(OUTPUT_FILE)