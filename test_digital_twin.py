from utils.digital_twin_engine import digital_twin_engine

twin = digital_twin_engine(

    suction=82,

    discharge=121,

    voltage=418,

    current=18,

    flow=333,

    hmr=2,

    actual_kwh=36

)

print()

print("Prediction")

print(twin["prediction"])

print()

print("Health")

print(twin["health"])

print()

print("Status")

print(twin["status"])

print()

print("Recommendation")

print(twin["recommendation"])

print()

print("Alarms")

for alarm in twin["alarms"]:

    print(alarm)