"""
=========================================================
GASONET DIGITAL TWIN
HYBRID AI PREDICTION ENGINE
=========================================================

Author : Uday Kaler
=========================================================
"""

# ==========================================================
# IMPORTS
# ==========================================================

import joblib
import pandas as pd

from ai_engine.engineering_rules import validate_inputs
from ai_engine.power_estimator import estimate_power
from ai_engine.health_engine import evaluate_health
from ai_engine.anomaly_engine import detect_anomaly


# ==========================================================
# LOAD MACHINE LEARNING MODEL
# ==========================================================

MODEL_PATH = "models/compressor_model_v3.pkl"

ml_model = joblib.load(MODEL_PATH)

print("✓ Compressor Model Loaded")
# ==========================================================
# PREDICTION FUNCTION
# ==========================================================

def predict(inputs: dict) -> dict:
    """
    Hybrid AI Prediction Engine

    Parameters
    ----------
    inputs : dict
        Compressor operating data

    Returns
    -------
    dict
        Prediction result
    """

    # ======================================================
    # STEP 1
    # ENGINEERING VALIDATION
    # ======================================================

    validation = validate_inputs(inputs)

    if not validation.valid:

        return {

            "valid": False,

            "warnings": validation.warnings

        }

    # Validated engineered features
    features = validation.features
        # ======================================================
    # STEP 2
    # MACHINE LEARNING FEATURE VECTOR
    # ======================================================

    model_input = pd.DataFrame([{

        "Suction press": inputs["suction"],

        "Discharge press": inputs["discharge"],

        "Voltage": inputs["voltage"],

        "Current": inputs["current"],

        "Flow Rate": inputs["flow"],

        "HMR_Hours": inputs["hmr"],

        "Pressure_Difference": features["Pressure_Difference"],

        "Pressure_Ratio": features["Pressure_Ratio"],

        "Electrical_Load": features["Electrical_Load"],

        "Flow_Utilization": features["Flow_Utilization"],

        "Load_Index": features["Load_Index"]

    }])
        # ======================================================
    # STEP 3
    # MACHINE LEARNING PREDICTION
    # ======================================================

    ml_power = float(
        ml_model.predict(model_input)[0]
    )

    ml_power = round(
        ml_power,
        2
    )
        # ======================================================
    # STEP 4
    # PHYSICS-BASED POWER PREDICTION
    # ======================================================

    physics_power = estimate_power(
        inputs,
        features
    )

    physics_power = round(
        float(physics_power),
        2
    )
        # ======================================================
    # STEP 5
    # MODEL DIFFERENCE
    # ======================================================

    model_difference = abs(
        ml_power -
        physics_power
    )

    model_difference = round(
        model_difference,
        2
    )
    
        # ======================================================
    # STEP 6
    # HYBRID POWER PREDICTION
    # ======================================================

    # Dynamic weighting based on model agreement

    if model_difference <= 2:

        ml_weight = 0.80
        physics_weight = 0.20

    elif model_difference <= 5:

        ml_weight = 0.70
        physics_weight = 0.30

    else:

        ml_weight = 0.60
        physics_weight = 0.40

    predicted_power = (

        ml_weight * ml_power +

        physics_weight * physics_power

    )

    predicted_power = round(
        predicted_power,
        2
    )
        # ======================================================
    # STEP 7
    # ENERGY CALCULATION
    # ======================================================

    predicted_energy = predicted_power * inputs["hmr"]

    predicted_energy = round(
        predicted_energy,
        2
    )
        # ======================================================
    # STEP 8
    # ANOMALY DETECTION
    # ======================================================

    anomaly_result = detect_anomaly(
        inputs,
        features
    )

    anomaly = anomaly_result["anomaly"]

    anomaly_score = anomaly_result["score"]
        # ======================================================
    # STEP 9
    # HEALTH ENGINE INPUT
    # ======================================================

    health_input = {

        "inputs": {

            "flow": inputs["flow"],

            "suction_pressure": inputs["suction"],

            "discharge_pressure": inputs["discharge"],

            "current": inputs["current"],

            "voltage": inputs["voltage"],

            "hmr_hours": inputs["hmr"]

        },

        "ml_power": ml_power,

        "physics_power": physics_power

    }
        # ======================================================
    # STEP 10
    # HEALTH EVALUATION
    # ======================================================

    health_result = evaluate_health(
        health_input
    )
        # ======================================================
    # STEP 11
    # EXTRACT HEALTH RESULTS
    # ======================================================

    health = health_result["health"]

    status = health_result["status"]

    health_scores = health_result["scores"]

    reasons = health_result["reasons"]

    recommendations = health_result["recommendations"]
        # ======================================================
    # STEP 12
    # BUILD FINAL RESULT
    # ======================================================

    result = {

        # --------------------------------------------
        # Status
        # --------------------------------------------

        "valid": True,

        # --------------------------------------------
        # Original Inputs
        # --------------------------------------------

        "inputs": inputs,

        "features": features,

        # --------------------------------------------
        # Power Prediction
        # --------------------------------------------

        "predicted_power": predicted_power,

        "predicted_energy": predicted_energy,

        "ml_power": ml_power,

        "physics_power": physics_power,

        "model_difference": round(
            abs(ml_power - physics_power),
            2
        ),

        "ml_weight": ml_weight,

        "physics_weight": physics_weight,

        # --------------------------------------------
        # Anomaly
        # --------------------------------------------

        "anomaly": anomaly,

        "anomaly_score": anomaly_score,

        # --------------------------------------------
        # Health Assessment
        # --------------------------------------------

        "health": health,

        "status": status,

        "health_scores": health_scores,

        "reasons": reasons,

        "recommendations": recommendations,

        # --------------------------------------------
        # Engine Information
        # --------------------------------------------

        "engine": "Hybrid AI Digital Twin V3",

        "model": "compressor_model_v3.pkl"

    }

    # ======================================================
    # STEP 13
    # RETURN RESULT
    # ======================================================

    return result