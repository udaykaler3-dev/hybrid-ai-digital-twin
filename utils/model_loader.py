import joblib
import pandas as pd

# ==========================================
# Load AI Model
# ==========================================

MODEL_PATH = "models/compressor_model.pkl"

model = joblib.load(MODEL_PATH)


# ==========================================
# Predict Compressor Power (KWH)
# ==========================================

def predict_kwh(values):

    columns = [
        "Suction press",
        "Discharge press",
        "Voltage",
        "Current",
        "Flow Rate",
        "HMR_Hours"
    ]

    df = pd.DataFrame([values], columns=columns)

    prediction = model.predict(df)[0]

    return float(prediction)