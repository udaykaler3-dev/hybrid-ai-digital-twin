"""
====================================================
AI DIGITAL TWIN V2
Compressor Health Engine
====================================================
"""

# ====================================================
# NORMAL OPERATING VALUES
# (Obtained from validated dataset)
# ====================================================

NORMAL = {

    "Suction": 82.24,
    "Discharge": 121.35,
    "Current": 17.77,
    "Flow": 332.84,
    "HMR": 1.97

}


# ====================================================
# ACCEPTABLE DEVIATIONS
# ====================================================

TOLERANCE = {

    "Suction": 40,
    "Discharge": 30,
    "Current": 4,
    "Flow": 100,
    "HMR": 2

}


# ====================================================
# Generic Health Score
# ====================================================

def calculate_score(actual, normal, tolerance):

    deviation = abs(actual - normal)

    score = 100 - (deviation / tolerance) * 100

    score = max(0, min(100, score))

    return round(score, 2)


# ====================================================
# Energy Health Score
# ====================================================

def energy_score(predicted, actual):

    if predicted <= 0:
        return 0

    error = abs(predicted - actual)

    score = 100 - (error / predicted) * 100

    score = max(0, min(100, score))

    return round(score, 2)


# ====================================================
# Compressor Health Engine
# ====================================================

def compressor_health(

    suction,
    discharge,
    current,
    flow,
    hmr,
    predicted_kwh,
    actual_kwh

):

    suction_score = calculate_score(
        suction,
        NORMAL["Suction"],
        TOLERANCE["Suction"]
    )

    discharge_score = calculate_score(
        discharge,
        NORMAL["Discharge"],
        TOLERANCE["Discharge"]
    )

    current_score = calculate_score(
        current,
        NORMAL["Current"],
        TOLERANCE["Current"]
    )

    flow_score = calculate_score(
        flow,
        NORMAL["Flow"],
        TOLERANCE["Flow"]
    )

    hmr_score = calculate_score(
        hmr,
        NORMAL["HMR"],
        TOLERANCE["HMR"]
    )

    energy = energy_score(
        predicted_kwh,
        actual_kwh
    )

    overall = (

        energy * 0.35 +

        current_score * 0.20 +

        flow_score * 0.15 +

        suction_score * 0.10 +

        discharge_score * 0.10 +

        hmr_score * 0.10

    )

    overall = round(overall, 2)

    return {

        "Overall Health": overall,

        "Energy Score": energy,

        "Current Score": current_score,

        "Flow Score": flow_score,

        "Suction Score": suction_score,

        "Discharge Score": discharge_score,

        "Running Hour Score": hmr_score

    }


# ====================================================
# Health Status
# ====================================================

def health_status(health):

    if health >= 95:
        return "Excellent"

    elif health >= 85:
        return "Healthy"

    elif health >= 70:
        return "Warning"

    elif health >= 50:
        return "Maintenance Required"

    else:
        return "Critical"


# ====================================================
# Recommendation Engine
# ====================================================

def recommendation(report):

    scores = {

        "Energy": report["Energy Score"],

        "Current": report["Current Score"],

        "Flow": report["Flow Score"],

        "Suction": report["Suction Score"],

        "Discharge": report["Discharge Score"],

        "Running Hours": report["Running Hour Score"]

    }

    weakest = min(scores, key=scores.get)

    recommendations = {

        "Energy":
            "Inspect compressor efficiency and check for gas leakage.",

        "Current":
            "Inspect motor current, bearings and electrical loading.",

        "Flow":
            "Inspect compressor valves and pipeline restrictions.",

        "Suction":
            "Inspect suction filter and inlet pressure.",

        "Discharge":
            "Inspect discharge valve and downstream pressure.",

        "Running Hours":
            "Schedule preventive maintenance."

    }

    return recommendations[weakest]