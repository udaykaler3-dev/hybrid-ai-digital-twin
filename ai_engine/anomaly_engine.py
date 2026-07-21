"""
=========================================================
AI DIGITAL TWIN V3
ANOMALY DETECTION ENGINE
=========================================================
Author : Uday Kaler
=========================================================
"""

# ==========================================================
# IMPORTS
# ==========================================================

import joblib
import pandas as pd

# ==========================================================
# LOAD ANOMALY MODEL
# ==========================================================

MODEL_PATH = "models/anomaly_detector.pkl"

anomaly_model = joblib.load(MODEL_PATH)

# ==========================================================
# DETECT ANOMALY
# ==========================================================

def detect_anomaly(inputs, features):

    """
    Detect whether the operating condition is
    Normal or Abnormal using Isolation Forest.
    """

    sample = pd.DataFrame([{

        "Suction press": inputs["suction"],

        "Discharge press": inputs["discharge"],

        "Voltage": inputs["voltage"],

        "Current": inputs["current"],

        "Flow Rate": inputs["flow"],

        "Pressure_Difference": features["Pressure_Difference"],

        "Pressure_Ratio": features["Pressure_Ratio"],

        "Electrical_Load": features["Electrical_Load"],

        "Flow_Utilization": features["Flow_Utilization"]

    }])

    prediction = anomaly_model.predict(sample)[0]

    score = float(anomaly_model.decision_function(sample)[0])

    if prediction == 1:

        anomaly = "Normal"

    else:

        anomaly = "Abnormal"

    return {

        "anomaly": anomaly,

        "score": round(score, 4)

    }