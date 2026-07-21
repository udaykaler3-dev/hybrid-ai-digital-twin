import pandas as pd

# ==========================================
# LOAD DATA
# ==========================================

INPUT_FILE = "data/engineered_data.csv"
OUTPUT_FILE = "data/training_dataset_v3.csv"

df = pd.read_csv(INPUT_FILE)

print("=" * 70)
print("CREATING TRAINING DATASET V3")
print("=" * 70)

original_rows = len(df)

# ==========================================
# REMOVE VERY SHORT RUNS
# ==========================================

df = df[df["HMR_Hours"] >= 0.25]

# ==========================================
# REMOVE IMPOSSIBLE POWER
# ==========================================

df = df[df["Power_kW"] >= 0]
df = df[df["Power_kW"] <= 30]

# ==========================================
# REMOVE IMPOSSIBLE PRESSURES
# ==========================================

df = df[df["Suction press"] > 0]
df = df[df["Discharge press"] > 0]

# ==========================================
# REMOVE IMPOSSIBLE FLOW
# ==========================================

df = df[df["Flow Rate"] >= 0]
df = df[df["Flow Rate"] <= 1000]

# ==========================================
# REMOVE IMPOSSIBLE CURRENT
# ==========================================

df = df[df["Current"] > 0]

# ==========================================
# REMOVE IMPOSSIBLE VOLTAGE
# ==========================================

df = df[(df["Voltage"] >= 380) & (df["Voltage"] <= 440)]

# ==========================================
# REPORT
# ==========================================

print(f"Original Rows : {original_rows}")
print(f"Remaining Rows : {len(df)}")
print(f"Rows Removed : {original_rows - len(df)}")

# ==========================================
# SAVE
# ==========================================

df.to_csv(OUTPUT_FILE, index=False)

print("\nTraining dataset created successfully.")
print(f"Saved as: {OUTPUT_FILE}")