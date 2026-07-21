from ai_engine.prediction_engine import predict

inputs = {
    "suction": 180,
    "discharge": 250,
    "voltage": 418,
    "current": 18,
    "flow": 700,
    "hmr": 2
}

result = predict(inputs)

print("\n===== PREDICTION RESULT =====")
print(result)