import csv
import os
from datetime import datetime

CSV_FILE = "data/historical_data.csv"


def generate_report_id():

    today = datetime.now().strftime("%Y%m%d")

    if not os.path.exists(CSV_FILE):
        return f"RPT-{today}-0001"

    with open(CSV_FILE, "r", encoding="utf-8") as file:

        rows = list(csv.reader(file))

        if len(rows) <= 1:
            return f"RPT-{today}-0001"

        last_id = rows[-1][0]

        try:
            number = int(last_id.split("-")[-1]) + 1
        except:
            number = 1

        return f"RPT-{today}-{number:04d}"


def highest_severity(alarms):

    priority = {

        "NORMAL": 0,
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3,
        "CRITICAL": 4

    }

    highest = "NORMAL"

    for alarm in alarms:

        if priority[alarm["Severity"]] > priority[highest]:

            highest = alarm["Severity"]

    return highest


def save_prediction(twin):

    report_id = generate_report_id()

    file_exists = os.path.isfile(CSV_FILE)

    with open(
        CSV_FILE,
        mode="a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        if not file_exists or os.path.getsize(CSV_FILE) == 0:

            writer.writerow([

                "Report_ID",
                "Timestamp",
                "Station",
                "Equipment",
                "Compressor_ID",

                "Suction",
                "Discharge",
                "Voltage",
                "Current",
                "Flow",
                "HMR",

                "Actual_KWH",
                "Predicted_KWH",

                "Overall_Health",
                "Status",

                "Recommendation",

                "Alarm_Count",
                "Highest_Severity"

            ])

        inputs = twin["inputs"]

        writer.writerow([

            report_id,

            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            "Harrison CNG Station",

            "Booster Compressor",

            "BC-01",

            inputs["suction"],
            inputs["discharge"],
            inputs["voltage"],
            inputs["current"],
            inputs["flow"],
            inputs["hmr"],

            inputs["actual_kwh"],

            round(twin["prediction"], 2),

            round(twin["health"], 2),

            twin["status"],

            twin["recommendation"],

            len(twin["alarms"]),

            highest_severity(twin["alarms"])

        ])