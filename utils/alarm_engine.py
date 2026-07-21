"""
====================================================
AI DIGITAL TWIN V2
Industrial Alarm Engine
====================================================
"""

from datetime import datetime


def generate_alarms(twin):

    alarms = []

    inputs = twin["inputs"]

    health = twin["health"]

    # ==========================================
    # High Motor Current
    # ==========================================

    if inputs["current"] > 22:

        alarms.append({

            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            "Code": "ALM001",

            "Severity": "HIGH",

            "Equipment": "Booster Compressor",

            "Message": "High Motor Current",

            "Action": "Inspect motor current, bearings and electrical loading."

        })

    # ==========================================
    # Low Gas Flow
    # ==========================================

    if inputs["flow"] < 250:

        alarms.append({

            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            "Code": "ALM002",

            "Severity": "MEDIUM",

            "Equipment": "Booster Compressor",

            "Message": "Low Gas Flow",

            "Action": "Inspect compressor valves and pipeline restriction."

        })

    # ==========================================
    # Low Suction Pressure
    # ==========================================

    if inputs["suction"] < 80:

        alarms.append({

            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            "Code": "ALM003",

            "Severity": "MEDIUM",

            "Equipment": "Booster Compressor",

            "Message": "Low Suction Pressure",

            "Action": "Inspect suction filter and inlet pressure."

        })

    # ==========================================
    # High Discharge Pressure
    # ==========================================

    if inputs["discharge"] > 200:

        alarms.append({

            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            "Code": "ALM004",

            "Severity": "HIGH",

            "Equipment": "Booster Compressor",

            "Message": "High Discharge Pressure",

            "Action": "Inspect discharge valve and downstream pressure."

        })

    # ==========================================
    # Compressor Health
    # ==========================================

    if health < 70:

        alarms.append({

            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            "Code": "ALM005",

            "Severity": "CRITICAL",

            "Equipment": "Booster Compressor",

            "Message": "Compressor Health Critical",

            "Action": "Shutdown compressor and perform complete inspection."

        })

    # ==========================================
    # No Alarm
    # ==========================================

    if len(alarms) == 0:

        alarms.append({

            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            "Code": "ALM000",

            "Severity": "NORMAL",

            "Equipment": "Booster Compressor",

            "Message": "No Active Alarm",

            "Action": "Continue normal operation."

        })

    return alarms