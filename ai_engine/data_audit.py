import pandas as pd
import os

# ==========================================
# LOAD DATASET
# ==========================================

DATA_PATH = "data/validated_data.csv"

if not os.path.exists(DATA_PATH):
    print(f"\nERROR : Dataset not found -> {DATA_PATH}")
    exit()

df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("        AI DIGITAL TWIN - DATASET AUDIT")
print("=" * 60)

# ==========================================
# BASIC INFORMATION
# ==========================================

print("\nDATASET INFORMATION")
print("-" * 60)

print(f"Rows              : {len(df)}")
print(f"Columns           : {len(df.columns)}")

print("\nColumn Names")

for col in df.columns:
    print(f" - {col}")

# ==========================================
# MISSING VALUES
# ==========================================

print("\nMISSING VALUES")
print("-" * 60)

print(df.isnull().sum())

# ==========================================
# DUPLICATES
# ==========================================

duplicates = df.duplicated().sum()

print("\nDUPLICATE ROWS")
print("-" * 60)

print(f"Duplicate Rows : {duplicates}")

# ==========================================
# DESCRIPTIVE STATISTICS
# ==========================================

print("\nSTATISTICAL SUMMARY")
print("-" * 60)

print(df.describe())

# ==========================================
# ENGINEERING VALIDATION
# ==========================================

print("\nENGINEERING VALIDATION")
print("-" * 60)

negative_pressure = (
    (df["Suction press"] < 0) |
    (df["Discharge press"] < 0)
).sum()

negative_current = (
    df["Current"] < 0
).sum()

negative_flow = (
    df["Flow Rate"] < 0
).sum()

zero_voltage = (
    df["Voltage"] <= 0
).sum()

flow_over_capacity = (
    df["Flow Rate"] > 1000
).sum()

pressure_issue = (
    df["Discharge press"] <= df["Suction press"]
).sum()

print(f"Negative Pressure Rows     : {negative_pressure}")
print(f"Negative Current Rows      : {negative_current}")
print(f"Negative Flow Rows         : {negative_flow}")
print(f"Zero Voltage Rows          : {zero_voltage}")
print(f"Flow >1000 SCM/hr          : {flow_over_capacity}")
print(f"Discharge <= Suction       : {pressure_issue}")

# ==========================================
# DATA QUALITY SCORE
# ==========================================

issues = (
    negative_pressure +
    negative_current +
    negative_flow +
    zero_voltage +
    flow_over_capacity
)

score = (
    (len(df) - issues) /
    len(df)
) * 100

print("\nDATA QUALITY SCORE")
print("-" * 60)

print(f"{score:.2f} %")

print("\nAudit Completed Successfully.")