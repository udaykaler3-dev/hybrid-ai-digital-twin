import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv("data/engineered_data.csv")

print("=" * 60)
print("FEATURE ANALYSIS")
print("=" * 60)

# ==========================================
# CORRELATION
# ==========================================

corr = df.corr(numeric_only=True)

target = "KWH Diff"

print("\nCorrelation with Target (KWH Diff)\n")

print(
    corr[target]
    .sort_values(ascending=False)
)

# ==========================================
# SAVE CORRELATION MATRIX
# ==========================================

corr.to_csv(
    "data/correlation_matrix.csv"
)

# ==========================================
# FEATURE IMPORTANCE PLOT
# ==========================================

feature_corr = (
    corr[target]
    .drop(target)
    .sort_values()
)

plt.figure(figsize=(10,6))

feature_corr.plot(kind="barh")

plt.title("Feature Correlation with KWH")

plt.xlabel("Correlation")

plt.tight_layout()

plt.savefig("data/feature_correlation.png")

print("\nCorrelation Matrix Saved")

print("Feature Plot Saved")