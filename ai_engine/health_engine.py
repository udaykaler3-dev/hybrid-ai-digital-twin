"""
==========================================================
GASONET BOOSTER COMPRESSOR HEALTH ENGINE
==========================================================

Purpose
-------
Evaluate booster cdhealth using
engineering rules and hybrid AI.

This module combines:

1. Flow Performance
2. Pressure Performance
3. Electrical Performance
4. Operating Efficiency
5. Model Agreement
6. Operating Condition

Author:
Uday Kaler
==========================================================
"""

from typing import Dict


# ==========================================================
# GASONET STATION BASELINE
# ==========================================================

import json
from pathlib import Path

BASELINE_FILE = Path("ai_engine/station_baseline.json")

with open(BASELINE_FILE, "r") as file:
    BASELINE = json.load(file)


# ==========================================================
# HEALTH STATUS LIMITS
# ==========================================================

EXCELLENT = 95
GOOD = 85
MODERATE = 70
POOR = 55
# ==========================================================
# FLOW PERFORMANCE SCORE
# ==========================================================

def calculate_flow_score(flow: float) -> float:
    """
    Evaluate compressor flow performance.

    Parameters
    ----------
    flow : float
        Average flow rate (kg/hr)

    Returns
    -------
    float
        Flow score (0–100)
    """

    optimum = BASELINE["flow_optimum"]
    minimum = BASELINE["flow_min"]
    maximum = BASELINE["flow_max"]

    # Ideal operating range
    if minimum <= flow <= maximum:

        deviation = abs(flow - optimum)

        score = 100 - (deviation / optimum) * 20

        return max(80, min(100, score))

    # Below historical operating range
    elif flow < minimum:

        deficit = minimum - flow

        score = 80 - (deficit / minimum) * 80

        return max(20, score)

    # Above historical operating range
    else:

        excess = flow - maximum

        score = 95 - (excess / maximum) * 30

        return max(60, score)
    # ==========================================================
# PRESSURE PERFORMANCE SCORE
# ==========================================================

def calculate_pressure_score(
    suction: float,
    discharge: float
) -> float:
    """
    Evaluate compressor pressure performance
    using station-specific historical baseline.
    """

    if discharge <= suction:
        return 20.0

    pressure_rise = discharge - suction

    optimum = BASELINE["pressure_rise_optimum"]
    minimum = BASELINE["pressure_rise_min"]
    maximum = BASELINE["pressure_rise_max"]

    # Normal operating range
    if minimum <= pressure_rise <= maximum:
        return 100.0

    # Below normal operating range
    if pressure_rise < minimum:
        deviation = minimum - pressure_rise
    else:
        deviation = pressure_rise - maximum

    score = 100 - (deviation / optimum) * 40

    return max(40.0, min(100.0, score))
   
# ==========================================================
# ELECTRICAL PERFORMANCE SCORE
# ==========================================================

def calculate_electrical_score(
    current: float,
    voltage: float
) -> float:
    """
    Evaluate electrical performance of the compressor.

    Parameters
    ----------
    current : float
        Motor current (A)

    voltage : float
        Supply voltage (V)

    Returns
    -------
    float
        Electrical score (0–100)
    """

    score = 100.0

    # -----------------------------
    # Current Evaluation
    # -----------------------------

    optimum_current = BASELINE["current_optimum"]
    warning_current = BASELINE["current_warning"]
    critical_current = BASELINE["current_critical"]

    if current <= optimum_current:

        pass

    elif current <= warning_current:

        score -= (current - optimum_current) * 3

    elif current <= critical_current:

        score -= 20 + (current - warning_current) * 6

    else:

        score -= 50

    # -----------------------------
    # Voltage Evaluation
    # -----------------------------

    nominal_voltage = BASELINE["voltage_nominal"]
    tolerance = BASELINE["voltage_tolerance"]

    voltage_error = abs(voltage - nominal_voltage)

    if voltage_error > tolerance:

        score -= (voltage_error - tolerance) * 2

    return max(20.0, min(100.0, score))
# ==========================================================
# OPERATING EFFICIENCY SCORE
# ==========================================================

def calculate_productivity_score(
    flow: float,
    hmr_hours: float
) -> float:
    """
   Evaluate compressor productivity using
gas delivered per operating hour.

    Parameters
    ----------
    flow : float
        Average gas flow (kg/hr)

    hmr_hours : float
        Compressor operating hours for the day

    Returns
    -------
    float
        Operating efficiency score (0–100)
    """

    # Invalid HMR
    if hmr_hours <= 0:
        return 20.0

    # Gas delivered per operating hour
    productivity = flow / hmr_hours

    # Historical productivity
    reference_productivity = (
        BASELINE["flow_optimum"] /
        BASELINE["hmr_optimum"]
    )

    ratio = productivity / reference_productivity

    if ratio >= 1.00:
        return 100

    elif ratio >= 0.90:
        return 95

    elif ratio >= 0.80:
        return 88

    elif ratio >= 0.70:
        return 78

    elif ratio >= 0.60:
        return 68

    else:
        return 55
    # ==========================================================
# MODEL AGREEMENT SCORE
# ==========================================================

def calculate_model_agreement_score(
    ml_power: float,
    physics_power: float
) -> float:
    """
    Evaluate agreement between the
    Machine Learning model and
    Physics model.

    Parameters
    ----------
    ml_power : float
        Power predicted by ML model (kW)

    physics_power : float
        Power calculated by Physics model (kW)

    Returns
    -------
    float
        Agreement score (0–100)
    """

    # Prevent division by zero
    if physics_power <= 0:
        return 60.0

    percentage_error = (
        abs(ml_power - physics_power)
        / physics_power
    ) * 100

    if percentage_error <= 2:
        return 100

    elif percentage_error <= 4:
        return 96

    elif percentage_error <= 6:
        return 92

    elif percentage_error <= 8:
        return 86

    elif percentage_error <= 10:
        return 80

    elif percentage_error <= 15:
        return 70

    else:
        return 60
    # ==========================================================
# OPERATING CONDITION SCORE
# ==========================================================

def calculate_operating_condition_score(
    flow: float,
    suction: float,
    discharge: float,
    current: float,
    voltage: float,
    hmr_hours: float
):
    """
    Evaluate overall operating condition using
    engineering rules.

    Returns
    -------
    tuple
        (condition_score, engineering_warnings)
    """

    score = 100.0
    warnings = []

    # --------------------------------------------------
    # Rule 1 : Pressure Relationship
    # --------------------------------------------------
    if discharge <= suction:

        score -= 30

        warnings.append(
            "Discharge pressure is not greater than suction pressure."
        )

    # --------------------------------------------------
    # Rule 2 : High Current + Low Flow
    # --------------------------------------------------
    if (
        current > BASELINE["current_warning"]
        and
        flow < BASELINE["flow_min"]
    ):

        score -= 20

        warnings.append(
            "High current with low flow indicates possible compressor wear or valve leakage."
        )

    # --------------------------------------------------
    # Rule 3 : Low Voltage
    # --------------------------------------------------
    if voltage < (
        BASELINE["voltage_nominal"]
        - BASELINE["voltage_tolerance"]
    ):

        score -= 10

        warnings.append(
            "Supply voltage is below the recommended operating range."
        )

    # --------------------------------------------------
    # Rule 4 : Long Operating Hours with Low Flow
    # --------------------------------------------------
    if (
        hmr_hours > BASELINE["hmr_warning"]
        and
        flow < BASELINE["flow_optimum"]
    ):

        score -= 15

        warnings.append(
            "Compressor required longer operating hours for reduced gas delivery."
        )

    score = max(20.0, min(100.0, score))

    return score, warnings
# ==========================================================
# ENGINEERING REASONS
# ==========================================================

def generate_reasons(
    flow_score: float,
    pressure_score: float,
    electrical_score: float,
    productivity_score: float,
    agreement_score: float,
    warnings: list
) -> list:
    """
    Generate engineering explanations for the
    compressor health assessment.
    """

    reasons = []

    # --------------------------------------------------
    # Flow
    # --------------------------------------------------

    if flow_score >= 95:

        reasons.append(
            "Gas flow is within the historical operating range."
        )

    elif flow_score >= 80:

        reasons.append(
            "Gas flow is slightly below the historical operating range."
        )

    else:

        reasons.append(
            "Reduced gas flow indicates possible compressor efficiency loss."
        )

    # --------------------------------------------------
    # Pressure
    # --------------------------------------------------

    if pressure_score >= 95:

        reasons.append(
            "Pressure rise across the compressor is normal."
        )

    elif pressure_score >= 80:

        reasons.append(
            "Pressure rise is slightly below the expected value."
        )

    else:

        reasons.append(
            "Reduced pressure rise indicates poor compression performance."
        )

    # --------------------------------------------------
    # Electrical
    # --------------------------------------------------

    if electrical_score >= 95:

        reasons.append(
            "Motor electrical loading is within the normal range."
        )

    elif electrical_score >= 80:

        reasons.append(
            "Motor current is slightly elevated."
        )

    else:

        reasons.append(
            "High electrical loading indicates increased mechanical resistance."
        )

    # --------------------------------------------------
    # Operating Efficiency
    # --------------------------------------------------

    if productivity_score >= 95:

        reasons.append(
            "Compressor productivity is within the normal operating range."
        )

    elif productivity_score >= 80:

        reasons.append(
            "Compressor productivity is slightly reduced."
        )

    else:

        reasons.append(
            "Lower gas delivery per operating hour indicates reduced compressor productivity."
        )

    # --------------------------------------------------
    # Model Agreement
    # --------------------------------------------------

    if agreement_score >= 95:

        reasons.append(
            "Machine Learning and Physics models show excellent agreement."
        )

    elif agreement_score >= 80:

        reasons.append(
            "Prediction models show acceptable agreement."
        )

    else:

        reasons.append(
            "Prediction models show significant disagreement."
        )

    # --------------------------------------------------
    # Engineering Warnings
    # --------------------------------------------------

    reasons.extend(warnings)

    return reasons
# ==========================================================
# MAINTENANCE RECOMMENDATIONS
# ==========================================================

def generate_recommendations(
    health: float,
    flow_score: float,
    pressure_score: float,
    electrical_score: float,
    productivity_score: float
) -> list:
    """
    Generate maintenance recommendations
    based on compressor health assessment.
    """

    recommendations = []

    # --------------------------------------------------
    # Overall Health
    # --------------------------------------------------

    if health >= EXCELLENT:

        recommendations.append(
            "Continue normal compressor operation."
        )

    elif health >= GOOD:

        recommendations.append(
            "Continue operation and monitor compressor performance."
        )

    elif health >= MODERATE:

        recommendations.append(
            "Increase monitoring frequency and inspect the compressor during the next maintenance window."
        )

    else:

        recommendations.append(
            "Immediate inspection is recommended before prolonged operation."
        )

    # --------------------------------------------------
    # Flow
    # --------------------------------------------------

    if flow_score < 80:

        recommendations.append(
            "Inspect suction and discharge valves for leakage or wear."
        )

    # --------------------------------------------------
    # Pressure
    # --------------------------------------------------

    if pressure_score < 80:

        recommendations.append(
            "Inspect compression efficiency, check valves and pressure transmitters."
        )

    # --------------------------------------------------
    # Electrical
    # --------------------------------------------------

    if electrical_score < 80:

        recommendations.append(
            "Inspect motor current, bearings and electrical supply."
        )

    # --------------------------------------------------
    # Operating Efficiency
    # --------------------------------------------------

    if productivity_score < 80:

        recommendations.append(
            "Investigate low gas delivery per operating hour and inspect compressor performance."
        )

    return recommendations
# ==========================================================
# MASTER HEALTH EVALUATION
# ==========================================================

def evaluate_health(result: Dict) -> Dict:
    """
    Master Health Evaluation Function.

    Combines all engineering modules into one
    final compressor health assessment.
    """

    # --------------------------------------------------
    # INPUT DATA
    # --------------------------------------------------

    inputs = result["inputs"]

    flow = inputs["flow"]
    suction = inputs["suction_pressure"]
    discharge = inputs["discharge_pressure"]
    current = inputs["current"]
    voltage = inputs["voltage"]
    hmr_hours = inputs["hmr_hours"]

    # --------------------------------------------------
    # MODEL OUTPUTS
    # --------------------------------------------------

    ml_power = result["ml_power"]
    physics_power = result["physics_power"]

    # --------------------------------------------------
    # INDIVIDUAL SCORES
    # --------------------------------------------------

    flow_score = calculate_flow_score(flow)

    pressure_score = calculate_pressure_score(
        suction,
        discharge
    )

    electrical_score = calculate_electrical_score(
        current,
        voltage
    )

    productivity_score = calculate_productivity_score(
        flow,
        hmr_hours
    )

    agreement_score = calculate_model_agreement_score(
        ml_power,
        physics_power
    )

    condition_score, warnings = (
        calculate_operating_condition_score(
            flow,
            suction,
            discharge,
            current,
            voltage,
            hmr_hours
        )
    )

    # --------------------------------------------------
    # FINAL HEALTH
    # --------------------------------------------------

    health = (
        0.30 * flow_score +
        0.20 * pressure_score +
        0.20 * electrical_score +
        0.10 * productivity_score +
        0.10 * agreement_score +
        0.10 * condition_score
    )

    health = round(health, 1)

    # --------------------------------------------------
    # HEALTH STATUS
    # --------------------------------------------------

    if health >= EXCELLENT:

        status = "Excellent"

    elif health >= GOOD:

        status = "Healthy"

    elif health >= MODERATE:

        status = "Moderate"

    elif health >= POOR:

        status = "Warning"

    else:

        status = "Critical"

    # --------------------------------------------------
    # ENGINEERING OUTPUT
    # --------------------------------------------------

    reasons = generate_reasons(
        flow_score,
        pressure_score,
        electrical_score,
        productivity_score,
        agreement_score,
        warnings
    )

    recommendations = generate_recommendations(
        health,
        flow_score,
        pressure_score,
        electrical_score,
        productivity_score
    )

    # --------------------------------------------------
    # RETURN RESULTS
    # --------------------------------------------------

    return {

        "health": health,

        "status": status,

        "scores": {

            "flow": round(flow_score, 1),

            "pressure": round(pressure_score, 1),

            "electrical": round(electrical_score, 1),

            "productivity": round(productivity_score, 1),

            "agreement": round(agreement_score, 1),

            "condition": round(condition_score, 1)

        },

        "reasons": reasons,

        "recommendations": recommendations

    }