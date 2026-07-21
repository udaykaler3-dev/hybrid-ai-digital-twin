from ai_engine.engineering_rules import validate_inputs
from ai_engine.anomaly_engine import detect_anomaly

inputs = {

    "suction":180,

    "discharge":250,

    "voltage":418,

    "current":18,

    "flow":700,

    "hmr":2

}

validation = validate_inputs(inputs)

result = detect_anomaly(

    inputs,

    validation.features

)

print(result)