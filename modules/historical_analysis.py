"""
=========================================================
GASONET DIGITAL TWIN
HISTORICAL ANALYSIS
=========================================================
"""

# ==========================================================
# Imports
# ==========================================================

import os
import pandas as pd
import streamlit as st

from styles.theme import load_theme


# ==========================================================
# Historical Analysis
# ==========================================================

def historical_analysis():

    # ------------------------------------------------------
    # Theme
    # ------------------------------------------------------

    load_theme()

    # ------------------------------------------------------
    # Header
    # ------------------------------------------------------

    st.title("Historical Analysis")

    st.caption(
        "Engineering analysis of stored Digital Twin prediction records."
    )

    st.divider()

    # ------------------------------------------------------
    # Prediction History File
    # ------------------------------------------------------

    HISTORY_FILE = "data/prediction_history.csv"

    if not os.path.exists(HISTORY_FILE):

        st.warning("Prediction history not found.")

        return

    history = pd.read_csv(HISTORY_FILE)

    # Remove accidental spaces from column names
    history.columns = history.columns.str.strip()

    if history.empty:

        st.warning("Prediction history is empty.")

        return

    # Latest Prediction
    latest = history.iloc[-1]
        # ==========================================================
    # OVERALL PERFORMANCE SUMMARY
    # ==========================================================

    st.subheader("Overall Performance Summary")

    total_predictions = len(history)

    average_health = history["Health (%)"].mean()

    average_power = history["Hybrid Power (kW)"].mean()

    average_energy = history["Predicted Energy (kWh)"].mean()

    col1, col2, col3, col4 = st.columns(4)
    with col1:

        with st.container(border=True):

            st.metric(
                "Total Predictions",
                total_predictions
            )
    with col2:

        with st.container(border=True):

            st.metric(
                "Average Health",
                f"{average_health:.1f}%"
            )
    with col3:

        with st.container(border=True):

            st.metric(
                "Average Hybrid Power",
                f"{average_power:.2f} kW"
            )
    with col4:

        with st.container(border=True):

            st.metric(
                "Average Energy",
                f"{average_energy:.2f} kWh"
            )
        st.divider()
            # ==========================================================
    # COMPRESSOR HEALTH SUMMARY
    # ==========================================================

    st.subheader("Compressor Health Summary")

    highest_health = history["Health (%)"].max()

    lowest_health = history["Health (%)"].min()

    latest_health = latest["Health (%)"]

    average_health = history["Health (%)"].mean()

    col1, col2, col3, col4 = st.columns(4)
    with col1:

        with st.container(border=True):

            st.metric(
                "Highest Health",
                f"{highest_health:.1f}%"
            )
    with col2:

        with st.container(border=True):

            st.metric(
                "Lowest Health",
                f"{lowest_health:.1f}%"
            )
    with col3:

        with st.container(border=True):

            st.metric(
                "Latest Health",
                f"{latest_health:.1f}%"
            )
    with col4:

        with st.container(border=True):

            st.metric(
                "Average Health",
                f"{average_health:.1f}%"
            )
        st.divider()
        # ==========================================================
    # LATEST PREDICTION SUMMARY
    # ==========================================================

    st.subheader("Latest Prediction Summary")

    col1, col2 = st.columns(2)
    with col1:

        with st.container(border=True):

            st.markdown("### Prediction Information")

            st.write(
                f"**Timestamp :** {latest['Timestamp']}"
            )

            st.write(
                f"**Health :** {latest['Health (%)']:.1f}%"
            )

            st.write(
                f"**Hybrid Power :** {latest['Hybrid Power (kW)']:.2f} kW"
            )

            st.write(
                f"**Predicted Energy :** {latest['Predicted Energy (kWh)']:.2f} kWh"
            )
    with col2:

        with st.container(border=True):

            st.markdown("### Model Performance")

            st.write(
                f"**ML Power :** {latest['ML Power (kW)']:.2f} kW"
            )

            st.write(
                f"**Physics Power :** {latest['Physics Power (kW)']:.2f} kW"
            )

            st.write(
                f"**Model Difference :** {latest['Model Difference (kW)']:.2f} kW"
            )

            # Determine Status
            if latest["Health (%)"] >= 90:

                st.success("🟢 HEALTHY")

            elif latest["Health (%)"] >= 75:

                st.warning("🟡 NEEDS ATTENTION")

            else:

                st.error("🔴 CRITICAL")
    st.divider()

    st.success("Historical Analysis Loaded Successfully")