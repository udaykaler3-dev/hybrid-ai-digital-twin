"""
====================================================
AI DIGITAL TWIN V2
Digital Twin Engine
====================================================
"""

from utils.model_loader import predict_kwh

from utils.compressor_health import (
    compressor_health,
    health_status,
    recommendation
)

from utils.alarm_engine import generate_alarms

from utils.historian import save_prediction


def digital_twin_engine(
    suction,
    discharge,
    voltage,
    current,
    flow,
    hmr,
    actual_kwh
):

    # ==========================================
    # AI Prediction
    # ==========================================

    prediction = predict_kwh(
        [
            suction,
            discharge,
            voltage,
            current,
            flow,
            hmr
        ]
    )

    # ==========================================
    # Health Report
    # ==========================================

    report = compressor_health(

        suction=suction,

        discharge=discharge,

        current=current,

        flow=flow,

        hmr=hmr,

        predicted_kwh=prediction,

        actual_kwh=actual_kwh

    )

    # ==========================================
    # Build Digital Twin
    # ==========================================

    twin = {

        "prediction": prediction,

        "health": report["Overall Health"],

        "status": health_status(
            report["Overall Health"]
        ),

        "recommendation": recommendation(
            report
        ),

        "report": report,

        "inputs": {

            "suction": suction,

            "discharge": discharge,

            "voltage": voltage,

            "current": current,

            "flow": flow,

            "hmr": hmr,

            "actual_kwh": actual_kwh

        }

    }

    # ==========================================
    # Generate Industrial Alarms
    # ==========================================

    twin["alarms"] = generate_alarms(twin)

    # ==========================================
    # Save to Historian
    # ==========================================

    save_prediction(twin)

    # ==========================================
    # Return Twin
    # ==========================================

    return twin