import streamlit as st


# ==========================================
# KPI CARD
# ==========================================

def kpi_card(title, value):

    st.metric(
        label=title,
        value=value
    )


# ==========================================
# STATION SUMMARY
# ==========================================

def station_summary(station):

    st.subheader("🏭 Station Summary")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Station Health",
            f"{station['Station Health']}%"
        )

    with c2:
        st.metric(
            "Compressor",
            station["Compressor State"]
        )

    with c3:
        st.metric(
            "Cascade",
            station["Cascade Status"]
        )

    with c4:
        st.metric(
            "Dispenser",
            station["Dispenser Status"]
        )


# ==========================================
# PRESSURE BAR
# ==========================================

def pressure_bar(title, pressure, maximum):

    percent = pressure / maximum

    st.write(f"### {title}")

    st.progress(percent)

    st.caption(f"{pressure} Bar")


# ==========================================
# STORAGE LEVELS
# ==========================================

def storage_levels(station):

    st.subheader("🏦 Storage Banks")

    c1, c2, c3 = st.columns(3)

    with c1:

        pressure_bar(
            "High Bank",
            station["High Bank Pressure"],
            220
        )

    with c2:

        pressure_bar(
            "Medium Bank",
            station["Medium Bank Pressure"],
            170
        )

    with c3:

        pressure_bar(
            "Low Bank",
            station["Low Bank Pressure"],
            105
        )


# ==========================================
# ALARM SUMMARY
# ==========================================

def alarm_summary(alarms):

    active = [
        a
        for a in alarms
        if a["Severity"] != "NORMAL"
    ]

    st.subheader("🚨 Alarm Summary")

    if len(active) == 0:

        st.success("No Active Alarm")

    else:

        st.error(
            f"Active Alarms : {len(active)}"
        )