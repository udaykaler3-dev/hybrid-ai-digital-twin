from utils.model_loader import predict_kwh

prediction = predict_kwh([
    82,
    121,
    418,
    18,
    333,
    2
])

print("Predicted KWH =", prediction)