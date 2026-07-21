import os
import joblib
import pandas as pd

from sklearn.ensemble import IsolationForest

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv("data/training_dataset_v3.csv")

FEATURES = [

    "Suction press",

    "Discharge press",

    "Voltage",

    "Current",

    "Flow Rate",

    "Pressure_Difference",

    "Pressure_Ratio",

    "Electrical_Load",

    "Flow_Utilization"

]

X = df[FEATURES]

print("=" * 60)
print("TRAINING ANOMALY DETECTOR")
print("=" * 60)

# =====================================================
# MODEL
# =====================================================

model = IsolationForest(

    n_estimators=200,

    contamination=0.05,

    random_state=42

)

model.fit(X)

prediction = model.predict(X)

df["Anomaly"] = prediction

normal = (prediction == 1).sum()
abnormal = (prediction == -1).sum()

print(f"Normal Samples   : {normal}")
print(f"Abnormal Samples : {abnormal}")

# =====================================================
# SAVE MODEL
# =====================================================

os.makedirs("models", exist_ok=True)

joblib.dump(

    model,

    "models/anomaly_detector.pkl"

)

print("\nSaved")

print("models/anomaly_detector.pkl")

# =====================================================
# SAVE DATASET
# =====================================================

df.to_csv(

    "training_reports/anomaly_analysis.csv",

    index=False

)

print("training_reports/anomaly_analysis.csv")