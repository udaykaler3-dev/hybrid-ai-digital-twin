from utils.alarm_engine import generate_alarms

twin = {

    "health": 62,

    "inputs": {

        "current": 24,

        "flow": 220,

        "suction": 75,

        "discharge": 215

    }

}

alarms = generate_alarms(twin)

for alarm in alarms:

    print(alarm)