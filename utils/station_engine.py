"""
==================================================
AI DIGITAL TWIN V2
Station Simulation Engine
==================================================
"""


def station_engine(twin):

    prediction = twin["prediction"]

    health = twin["health"]

    inputs = twin["inputs"]

    # ==========================================
    # STORAGE BANK PRESSURES
    # ==========================================

    high_bank = round(

        220 - prediction * 0.05,

        1

    )

    medium_bank = round(

        170 - prediction * 0.03,

        1

    )

    low_bank = round(

        105 + prediction * 0.02,

        1

    )

    # ==========================================
    # STORAGE LEVELS (%)
    # ==========================================

    high_level = round(high_bank / 220 * 100, 1)

    medium_level = round(medium_bank / 170 * 100, 1)

    low_level = round(low_bank / 220 * 100, 1)

    # ==========================================
    # MOBILE CASCADE
    # ==========================================

    if high_level > 30:

        cascade_status = "Available"

    else:

        cascade_status = "Refill Required"

    # ==========================================
    # DISPENSER STATUS
    # ==========================================

    if inputs["flow"] > 200:

        dispenser = "Ready"

    else:

        dispenser = "Low Flow"

    # ==========================================
    # COMPRESSOR STATE
    # ==========================================

    if health >= 90:

        compressor = "Running"

    elif health >= 70:

        compressor = "Running (Warning)"

    elif health >= 50:

        compressor = "Maintenance"

    else:

        compressor = "Shutdown"

    # ==========================================
    # STATION HEALTH
    # ==========================================

    station_health = round(

        (health + high_level + medium_level + low_level) / 4,

        2

    )

    # ==========================================
    # RETURN
    # ==========================================

    return {

        "High Bank Pressure": high_bank,

        "Medium Bank Pressure": medium_bank,

        "Low Bank Pressure": low_bank,

        "High Bank Level": high_level,

        "Medium Bank Level": medium_level,

        "Low Bank Level": low_level,

        "Cascade Status": cascade_status,

        "Dispenser Status": dispenser,

        "Compressor State": compressor,

        "Station Health": station_health

    }