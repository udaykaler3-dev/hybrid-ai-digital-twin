import streamlit as st


# ==========================================
# MOBILE CASCADE
# ==========================================

def draw_mobile_cascade():

    st.markdown(
        """
<div style="
background:#1565C0;
color:white;
padding:18px;
border-radius:12px;
text-align:center;
font-size:22px;
font-weight:bold;">

🚛 MOBILE CASCADE

<br><br>

Gas Available

</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================
# BOOSTER COMPRESSOR
# ==========================================

def draw_compressor(

    health,
    prediction,
    status,
    current,
    flow

):

    if health >= 90:

        color = "#2E7D32"

        running = "🟢 RUNNING"

    elif health >= 70:

        color = "#F9A825"

        running = "🟡 WARNING"

    elif health >= 50:

        color = "#EF6C00"

        running = "🟠 MAINTENANCE"

    else:

        color = "#C62828"

        running = "🔴 SHUTDOWN"

    st.markdown(

        f"""

<div style="
background:{color};
color:white;
padding:20px;
border-radius:12px;
text-align:center;
font-size:20px;
font-weight:bold;">

⚙ BOOSTER COMPRESSOR

<br><br>

{running}

<br>

Health : {health:.2f} %

<br>

Status : {status}

<br>

Power : {prediction:.2f} KWH

<br>

Current : {current} A

<br>

Flow : {flow} SCM/hr

</div>

""",

        unsafe_allow_html=True

    )


# ==========================================
# STORAGE BANKS
# ==========================================

def draw_storage_banks(

    high,

    medium,

    low

):

    c1, c2, c3 = st.columns(3)

    with c1:

        st.success(f"""

### HIGH BANK

Pressure

{high} Bar

""")

    with c2:

        st.success(f"""

### MEDIUM BANK

Pressure

{medium} Bar

""")

    with c3:

        st.success(f"""

### LOW BANK

Pressure

{low} Bar

""")


# ==========================================
# DISPENSER
# ==========================================

def draw_dispenser():

    st.markdown(
        """
<div style="
background:#424242;
color:white;
padding:18px;
border-radius:10px;
text-align:center;
font-size:20px;
font-weight:bold;">

⛽ DISPENSER

<br><br>

READY

</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================
# EQUIPMENT TABLE
# ==========================================

def draw_equipment_table(

    health,

    running

):

    equipment = {

        "Equipment": [

            "Mobile Cascade",

            "Booster Compressor",

            "High Bank",

            "Medium Bank",

            "Low Bank",

            "Dispenser"

        ],

        "Status": [

            "Online",

            running,

            "Online",

            "Online",

            "Online",

            "Ready"

        ],

        "Health (%)": [

            100,

            round(health, 2),

            100,

            100,

            100,

            100

        ]

    }

    st.dataframe(

        equipment,

        use_container_width=True

    )


# ==========================================
# ALARM PANEL
# ==========================================

def draw_alarm_panel(

    alarms

):

    active = [

        alarm

        for alarm in alarms

        if alarm["Severity"] != "NORMAL"

    ]

    if len(active) == 0:

        st.success(

            "✅ No Active Alarm"

        )

    else:

        for alarm in active:

            if alarm["Severity"] == "CRITICAL":

                st.error(

                    f"{alarm['Code']} : {alarm['Message']}"

                )

            elif alarm["Severity"] == "HIGH":

                st.error(

                    f"{alarm['Code']} : {alarm['Message']}"

                )

            elif alarm["Severity"] == "MEDIUM":

                st.warning(

                    f"{alarm['Code']} : {alarm['Message']}"

                )

            else:

                st.info(

                    f"{alarm['Code']} : {alarm['Message']}"

                )