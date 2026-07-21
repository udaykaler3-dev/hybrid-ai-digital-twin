from utils.compressor_health import *

report = compressor_health(

    suction=82,

    discharge=121,

    current=18,

    flow=333,

    hmr=2,

    predicted_kwh=37,

    actual_kwh=36

)

print(report)

print()

print(health_status(report["Overall Health"]))

print()

print(recommendation(report))