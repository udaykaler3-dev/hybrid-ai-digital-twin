# ==========================================================
# GASONET AI DIGITAL TWIN
# Main Application
# ==========================================================

import streamlit as st

# ==========================================================
# IMPORT APPLICATION MODULES
# ==========================================================

from modules.dashboard import dashboard
from modules.manual_prediction import manual_prediction
from modules.digital_twin import digital_twin
from modules.historical_analysis import historical_analysis
from modules.prediction_history import prediction_history
from modules.reports import reports

# ==========================================================
# IMPORT THEME
# ==========================================================

from styles.theme import load_theme

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Gasonet AI Digital Twin",
    page_icon="assets/gasonet_logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ==========================================================
# LOAD THEME
# ==========================================================

load_theme()


# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.image(
    "assets/gasonet_logo.png",
    width=170
)

st.sidebar.title("Gasonet")

st.sidebar.caption("AI Digital Twin Platform")

st.sidebar.divider()

page = st.sidebar.radio(

    "Navigation",

    [

        "Manual Prediction",

        "Dashboard",

        "Digital Twin",

        "Historical Analysis",

        "Prediction History",

        "Reports"

    ],

    index=0

)

st.sidebar.divider()

st.sidebar.caption(
    "Booster Compressor Health Monitoring"
)
# ==========================================================
# PAGE ROUTING
# ==========================================================

if page == "Manual Prediction":

    manual_prediction()

elif page == "Dashboard":

    dashboard()

elif page == "Digital Twin":

    digital_twin()

elif page == "Historical Analysis":

    historical_analysis()

elif page == "Prediction History":

    prediction_history()

elif page == "Reports":

    reports()