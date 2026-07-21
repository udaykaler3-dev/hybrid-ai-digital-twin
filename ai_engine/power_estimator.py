"""
Physics-Based Power Estimator
AI Digital Twin V3
"""

import math

# ==========================================================
# COMPRESSOR CONSTANTS
# ==========================================================

MOTOR_POWER = 22.0          # kW
MAX_FLOW = 1000.0           # SCM/hr

REFERENCE_PRESSURE_RATIO = 250 / 180

REFERENCE_CURRENT = 18.0

REFERENCE_FLOW = 780


def estimate_power(inputs, features):
    """
    Estimate compressor power using engineering relationships.

    Returns
    -------
    estimated_power : float
    """

    current = inputs["current"]
    flow = inputs["flow"]

    pressure_ratio = features["Pressure_Ratio"]

    # -------------------------------------------------
    # NORMALIZED TERMS
    # -------------------------------------------------

    current_factor = current / REFERENCE_CURRENT

    flow_factor = flow / REFERENCE_FLOW

    pressure_factor = (
        pressure_ratio /
        REFERENCE_PRESSURE_RATIO
    )

    # -------------------------------------------------
    # LOAD INDEX
    # -------------------------------------------------

    load = (
        0.45 * current_factor +
        0.35 * flow_factor +
        0.20 * pressure_factor
    )

    load = max(0.0, min(load, 1.50))

    estimated_power = MOTOR_POWER * load

    estimated_power = round(
        estimated_power,
        2
    )

    return estimated_power