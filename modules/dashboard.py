"""
=========================================================
GASONET DIGITAL TWIN
MAIN DASHBOARD
=========================================================

Displays:

• Compressor Health
• Live Operating Parameters
• Power Prediction
• Engineering Scores
• AI Analysis
• Engineering Alarms

Author : Uday Kaler
=========================================================
"""

# ==========================================================
# IMPORTS
# ==========================================================

import streamlit as st
import plotly.graph_objects as go
from styles.theme import load_theme





# ==========================================================
# MAIN DASHBOARD
# ==========================================================

def dashboard():

    # ------------------------------------------------------
    # Load Theme
    # ------------------------------------------------------

    load_theme()

    # ------------------------------------------------------
    # Prediction Validation
    # ------------------------------------------------------

    if "twin" not in st.session_state:

        st.info(
            "Run a Manual Prediction to start the Digital Twin."
        )

        return

    twin = st.session_state["twin"]

    if not twin.get("valid", False):

        st.error(
            "Prediction data is invalid."
        )

        return
        # ------------------------------------------------------
    # HEADER
    # ------------------------------------------------------

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.image(
    "assets/gasonet_logo.png",
    use_container_width=True
)

    st.title(
        "Gasonet Booster Compressor Digital Twin"
    )

    st.caption(
        "AI-Based Condition Monitoring & Predictive Maintenance"
    )

    st.divider()
        # ==========================================================
    # COMPRESSOR HEALTH
    # ==========================================================

    st.subheader("Compressor Health Overview")

    health = twin["health"]

    status = twin["status"]

    col1, col2 = st.columns([2, 1])
    with col1:

        with st.container(border=True):

            st.markdown("### Overall Compressor Health")

            st.metric(
                label="Health",
                value=f"{health:.1f}%"
            )

            st.progress(
                min(health / 100, 1.0)
            )
    with col2:

        with st.container(border=True):

            st.markdown("### Health Status")

            if health >= 90:

                st.success(f"🟢 {status}")

            elif health >= 75:

                st.warning(f"🟡 {status}")

            else:

                st.error(f"🔴 {status}")

            st.write("")

            st.write(
                f"**Predicted Power:** "
                f"{twin['predicted_power']:.2f} kW"
            )

            st.write(
                f"**Predicted Energy:** "
                f"{twin['predicted_energy']:.2f} kWh"
            )
    st.divider()
     # ==========================================================
    # LIVE OPERATING PARAMETERS
    # ==========================================================

    st.subheader("Live Operating Parameters")

    inputs = twin["inputs"]

    col1, col2, col3 = st.columns(3)
    with col1:

        with st.container(border=True):

            st.markdown("### Gas Parameters")

            st.metric(
                "Compressor Delivery Flow",
                f"{inputs['flow']:.2f} kg/hr"
            )

            st.metric(
                "Suction Pressure",
                f"{inputs['suction']:.2f} bar"
            )
    with col2:

        with st.container(border=True):

            st.markdown("### Compressor")

            st.metric(
                "Discharge Pressure",
                f"{inputs['discharge']:.2f} bar"
            )

            st.metric(
                "Operating Hours",
                f"{inputs['hmr']:.2f} hr"
            )
    with col3:

        with st.container(border=True):

            st.markdown("### Electrical")

            st.metric(
                "Current",
                f"{inputs['current']:.2f} A"
            )

            st.metric(
                "Voltage",
                f"{inputs['voltage']:.2f} V"
            )
    st.divider()
        # ==========================================================
    # HYBRID POWER PREDICTION
    # ==========================================================

    st.subheader("Hybrid Power Prediction")

    col1, col2, col3, col4 = st.columns(4)
    with col1:

        with st.container(border=True):

            st.metric(
                label="ML Power",
                value=f"{twin['ml_power']:.2f} kW"
            )
    with col2:

        with st.container(border=True):

            st.metric(
                label="Physics Power",
                value=f"{twin['physics_power']:.2f} kW"
            )
    with col3:

        with st.container(border=True):

            st.metric(
                label="Hybrid Power",
                value=f"{twin['predicted_power']:.2f} kW"
            )
    with col4:

        with st.container(border=True):

            st.metric(
                label="Predicted Energy",
                value=f"{twin['predicted_energy']:.2f} kWh"
            )
    st.divider()
        # ==========================================================
    # ENGINEERING HEALTH SCORES
    # ==========================================================

    st.subheader("Engineering Health Assessment")

    scores = twin["health_scores"]

    col1, col2, col3 = st.columns(3)
    with col1:

        with st.container(border=True):

            st.markdown("### Hydraulic Performance")

            st.metric(
                "Flow Score",
                f"{scores['flow']:.1f}%"
            )

            st.metric(
                "Pressure Score",
                f"{scores['pressure']:.1f}%"
            )
    with col2:

        with st.container(border=True):

            st.markdown("### Electrical Performance")

            st.metric(
                "Electrical Score",
                f"{scores['electrical']:.1f}%"
            )

            st.metric(
                "Productivity Score",
                f"{scores['productivity']:.1f}%"
            )
    with col3:

        with st.container(border=True):

            st.markdown("### AI & Operating Condition")

            st.metric(
                "Operating Condition",
                f"{scores['condition']:.1f}%"
            )

            st.metric(
                "Model Difference",
                f"{twin['model_difference']:.2f} kW"
            )
    st.divider()
        # ==========================================================
    # ENGINEERING PERFORMANCE SCORE CHART
    # ==========================================================

    st.subheader("Engineering Performance Score Analysis")

    labels = [
        "Flow",
        "Pressure",
        "Electrical",
        "Productivity",
        "Condition"
    ]

    values = [
        scores["flow"],
        scores["pressure"],
        scores["electrical"],
        scores["productivity"],
        scores["condition"]
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=labels,
            y=values,
            text=[f"{v:.1f}%" for v in values],
            textposition="outside"
        )
    )

    fig.update_layout(
        title="Engineering Performance Scores",
        yaxis=dict(range=[0, 100]),
        xaxis_title="Engineering Parameters",
        yaxis_title="Score (%)",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Hybrid AI Power Prediction Comparison")

    fig2 = go.Figure()

    # Physics Model
    fig2.add_trace(
        go.Bar(
            name="Physics Model",
            x=["Power Prediction"],
            y=[twin["physics_power"]],
            text=[f'{twin["physics_power"]:.2f} kW'],
            textposition="outside",
            marker_color="#1f77b4"
        )
    )

    # Machine Learning Model
    fig2.add_trace(
        go.Bar(
            name="Machine Learning",
            x=["Power Prediction"],
            y=[twin["ml_power"]],
            text=[f'{twin["ml_power"]:.2f} kW'],
            textposition="outside",
            marker_color="#2ca02c"
        )
    )

    # Hybrid Prediction
    fig2.add_trace(
        go.Bar(
            name="Hybrid AI",
            x=["Power Prediction"],
            y=[twin["predicted_power"]],
            text=[f'{twin["predicted_power"]:.2f} kW'],
            textposition="outside",
            marker_color="#ff7f0e"
        )
    )

    fig2.update_layout(

        barmode="group",

        title="Hybrid AI Power Prediction Comparison",

        yaxis_title="Power (kW)",

        xaxis_title="Prediction Model",

        legend_title="Prediction Method",

        height=450
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.caption(
        f"Hybrid Prediction = "
        f"{twin['ml_weight']*100:.0f}% Machine Learning + "
        f"{twin['physics_weight']*100:.0f}% Physics Model"
    )

    st.divider()
 
    # ==========================================================
    # AI ENGINEERING ANALYSIS
    # ==========================================================

    st.subheader("AI Engineering Analysis")

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.markdown("### Engineering Observations")

            if len(twin["reasons"]) == 0:

                st.success(
                    "No abnormal operating conditions detected."
                )

            else:

                for reason in twin["reasons"]:

                    st.write(f"• {reason}")

    with col2:

        with st.container(border=True):

            st.markdown("### Maintenance Recommendations")

            if len(twin["recommendations"]) == 0:

                st.success(
                    "Continue normal compressor operation."
                )

            else:

                for rec in twin["recommendations"]:

                    st.info(rec)

    st.divider()

    # ==========================================================
    # DIGITAL TWIN SUMMARY
    # ==========================================================

    st.subheader("Digital Twin Summary")

    with st.container(border=True):

        st.write(
            f"**Overall Compressor Health :** "
            f"{twin['health']:.1f}%"
        )

        st.write(
            f"**Current Status :** "
            f"{twin['status']}"
        )

        st.write(
            f"**Hybrid Predicted Power :** "
            f"{twin['predicted_power']:.2f} kW"
        )

        st.write(
            f"**Predicted Energy Consumption :** "
            f"{twin['predicted_energy']:.2f} kWh"
        )

        st.write(
            f"**Physics vs ML Difference :** "
            f"{twin['model_difference']:.2f} kW"
        )

        if len(twin["recommendations"]) > 0:

            st.write(
                f"**Recommended Action :** "
                f"{twin['recommendations'][0]}"
            )

        else:

            st.write(
                "**Recommended Action :** Continue Normal Operation"
            )