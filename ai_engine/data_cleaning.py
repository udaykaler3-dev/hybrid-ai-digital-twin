import pandas as pd
import numpy as np

# =====================================================
# LOAD DATA
# =====================================================

INPUT_FILE = "data/engineered_data.csv"
OUTPUT_FILE = "data/cleaned_engineered_data.csv"

df = pd.read_csv(INPUT_FILE)

print("=" * 70)
print("ENGINEERING DATA CLEANING")
print("=" * 70)

original_rows = len(df)

# =====================================================
# CREATE STATUS COLUMN
# =====================================================

df["Status"] = "VALID"

# =====================================================
# ENGINEERING RULES
# =====================================================

# Rule 1 : Negative values
df.loc[df["Suction press"] < 0, "Status"] = "INVALID"
df.loc[df["Discharge press"] < 0, "Status"] = "INVALID"
df.loc[df["Voltage"] <= 0, "Status"] = "INVALID"
df.loc[df["Current"] <= 0, "Status"] = "INVALID"
df.loc[df["Flow Rate"] < 0, "Status"] = "INVALID"

# Rule 2 : Short duration readings
df.loc[df["HMR_Hours"] < 0.25, "Status"] = "WARNING"

# Rule 3 : Motor power check
df.loc[df["Power_kW"] > 30, "Status"] = "WARNING"

# Rule 4 : Pressure relationship
df.loc[
    df["Discharge press"] <= df["Suction press"],
    "Status"
] = "WARNING"

# Rule 5 : Flow capacity
df.loc[df["Flow Rate"] > 1000, "Status"] = "INVALID"

# =====================================================
# OUTLIER DETECTION (IQR)
# =====================================================

numeric_columns = [

    "Suction press",
    "Discharge press",
    "Voltage",
    "Current",
    "Flow Rate",
    "Power_kW"

]

for col in numeric_columns:

    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)

    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    mask = (df[col] < lower) | (df[col] > upper)

    df.loc[mask, "Status"] = "WARNING"

# =====================================================
# SUMMARY
# =====================================================

print("\nSTATUS SUMMARY")
print("-" * 40)

print(df["Status"].value_counts())

# =====================================================
# CREATE CLEAN DATASET
# =====================================================

clean_df = df[df["Status"] != "INVALID"].copy()

print("\nROWS")

print(f"Original : {original_rows}")
print(f"Remaining : {len(clean_df)}")

# =====================================================
# SAVE
# =====================================================

clean_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nSaved")

print(OUTPUT_FILE)