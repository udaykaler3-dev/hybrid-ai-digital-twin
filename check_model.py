import joblib

model = joblib.load("models/compressor_model_v3.pkl")

print(type(model))

print(model)