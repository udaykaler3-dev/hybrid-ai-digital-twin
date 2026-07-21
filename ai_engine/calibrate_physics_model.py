import json
import os

import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# ==========================================================
# LOAD DATA
# ==========================================================

df = pd.read_csv("data/training_dataset_v3.csv")

# ==========================================================
# ENGINEERING FEATURES
# ==========================================================

FEATURES = [

    "Current",

    "Flow Rate",

    "Pressure_Ratio"

]

TARGET = "Power_kW"

X = df[FEATURES]

y = df[TARGET]

# ==========================================================
# TRAIN PHYSICS MODEL
# ==========================================================

model = LinearRegression()

model.fit(X, y)

prediction = model.predict(X)

r2 = r2_score(y, prediction)

print("=" * 60)
print("PHYSICS MODEL CALIBRATION")
print("=" * 60)

print(f"Training R2 : {r2:.4f}")

print("\nIntercept")

print(model.intercept_)

print("\nCoefficients")

for feature, coef in zip(FEATURES, model.coef_):

    print(f"{feature:20s}: {coef:.6f}")

# ==========================================================
# SAVE COEFFICIENTS
# ==========================================================

coefficients = {

    "intercept": float(model.intercept_),

    "current": float(model.coef_[0]),

    "flow": float(model.coef_[1]),

    "pressure_ratio": float(model.coef_[2])

}

os.makedirs("models", exist_ok=True)

with open(

    "models/physics_coefficients.json",

    "w"

) as f:

    json.dump(

        coefficients,

        f,

        indent=4

    )

print("\nSaved")

print("models/physics_coefficients.json")