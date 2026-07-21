from dataclasses import dataclass
import math

# ==========================================================
# COMPRESSOR SPECIFICATIONS
# ==========================================================

RATED_SUCTION = 180.0
RATED_DISCHARGE = 250.0

MAX_FLOW = 750.0

RATED_MOTOR_POWER = 22.0

VOLTAGE_MIN = 380
VOLTAGE_MAX = 440

CURRENT_MIN = 0
CURRENT_MAX = 40

POWER_FACTOR = 0.85


@dataclass
class ValidationResult:

    valid: bool

    warnings: list

    features: dict


# ==========================================================
# ENGINEERING VALIDATION
# ==========================================================

def validate_inputs(inputs):

    warnings = []

    suction = inputs["suction"]
    discharge = inputs["discharge"]
    voltage = inputs["voltage"]
    current = inputs["current"]
    flow = inputs["flow"]
    hours = inputs["hmr"]

    valid = True

    # ---------------------------------------------
    # Pressure
    # ---------------------------------------------

    if suction <= 0:

        valid = False
        warnings.append("Invalid suction pressure.")

    if discharge <= 0:

        valid = False
        warnings.append("Invalid discharge pressure.")

    if discharge <= suction:

        warnings.append(
            "Outlet pressure is not greater than inlet pressure."
        )

    # ---------------------------------------------
    # Voltage
    # ---------------------------------------------

    if voltage < VOLTAGE_MIN:

        warnings.append(
            "Voltage below operating limit."
        )

    if voltage > VOLTAGE_MAX:

        warnings.append(
            "Voltage above operating limit."
        )

    # ---------------------------------------------
    # Current
    # ---------------------------------------------

    if current < CURRENT_MIN:

        valid = False
        warnings.append(
            "Negative current detected."
        )

    if current > CURRENT_MAX:

        warnings.append(
            "Motor current unusually high."
        )

    # ---------------------------------------------
    # Flow
    # ---------------------------------------------

    if flow < 0:

        valid = False
        warnings.append(
            "Negative flow detected."
        )

    if flow > MAX_FLOW:

        warnings.append(
            "Flow exceeds compressor rating."
        )

    # ---------------------------------------------
    # Running Hours
    # ---------------------------------------------

    if hours <= 0:

        valid = False
        warnings.append(
            "Running hours must be greater than zero."
        )

     # ==========================================================
    # ENGINEERING FEATURES
    # ==========================================================

    pressure_difference = discharge - suction

    pressure_ratio = discharge / suction

    electrical_load = (
        math.sqrt(3)
        * voltage
        * current
        * POWER_FACTOR
    ) / 1000

    flow_utilization = flow / MAX_FLOW

    load_index = current * pressure_ratio

    motor_loading = electrical_load / RATED_MOTOR_POWER

    pressure_utilization = discharge / RATED_DISCHARGE

    features = {

        "Pressure_Difference": pressure_difference,

        "Pressure_Ratio": pressure_ratio,

        "Electrical_Load": electrical_load,

        "Flow_Utilization": flow_utilization,

        "Load_Index": load_index,

        "Motor_Loading": motor_loading,

        "Pressure_Utilization": pressure_utilization

    }

    return ValidationResult(

        valid,

        warnings,

        features

    )