import pandas as pd

df = pd.read_csv("data/training_dataset_v3.csv")

print("=" * 50)
print("POWER STATISTICS")
print("=" * 50)

print(df["Power_kW"].describe())

print("\n" + "=" * 50)
print("POWER VALUE COUNTS")
print("=" * 50)

print(df["Power_kW"].value_counts().sort_index())