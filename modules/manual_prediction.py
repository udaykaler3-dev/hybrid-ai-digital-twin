import streamlit as st

from styles.theme import load_theme

from ai_engine.prediction_engine import predict
import pandas as pd
import os
from datetime import datetime


def manual_prediction():

    # =====================================================
    # LOAD APPLICATION THEME
    # =====================================================

    load_theme()

    # =====================================================
    # HEADER
    # =====================================================

    left, center, right = st.columns([1, 2, 1])

    with center:

       st.image(
    "assets/gasonet_logo.png",
    use_container_width=True
)

    st.title("MANUAL PREDICTION")

    st.subheader("Booster Compressor Operating Parameters")

    st.caption(
        "Enter the operating conditions of the booster compressor to generate a new AI Digital Twin prediction."
    )

    st.divider()
        # =====================================================
    # COMPRESSOR OPERATING PARAMETERS
    # =====================================================

    st.subheader("Compressor Operating Parameters")

    left_col, right_col = st.columns(2)

    # -----------------------------------------------------
    # LEFT COLUMN
    # -----------------------------------------------------

    with left_col:

        suction = st.number_input(
            "Suction Pressure (bar)",
            min_value=0.0,
            value=180.0,
            step=1.0
        )

        discharge = st.number_input(
            "Discharge Pressure (bar)",
            min_value=0.0,
            value=250.0,
            step=1.0
        )

        voltage = st.number_input(
            "Voltage (V)",
            min_value=0.0,
            value=418.0,
            step=1.0
        )

    # -----------------------------------------------------
    # RIGHT COLUMN
    # -----------------------------------------------------

    with right_col:

        current = st.number_input(
            "Current (A)",
            min_value=0.0,
            value=18.0,
            step=0.5
        )

        flow = st.number_input(
        "Compressor Delivery Flow(kg/hr)",
    min_value=0.0,
    value=300.0,
    step=10.0
)
        
        hmr_input = st.text_input(

            "HMR Difference (HH:MM:SS)",

            value="00:00:00"

        )


        # Convert HH:MM:SS into hours


        try:


            h, m, s = map(

                int,

                hmr_input.split(":")

            )


            hmr = (
                h
                +
                (m / 60)
                +
                (s / 3600)
            )


        except:


            hmr = 0


            st.warning(

                "Enter HMR Difference in HH:MM:SS format"

            )

    st.divider()
        # =====================================================
    # RUN AI PREDICTION
    # =====================================================

    if st.button(
        "Predict Compressor Health",
        use_container_width=True
    ):

        # ---------------------------------------------
        # CREATE INPUT DICTIONARY
        # ---------------------------------------------

        inputs = {

    "suction": suction,

    "discharge": discharge,

    "voltage": voltage,

    "current": current,

    "flow": flow,

    "hmr": hmr,

    "hmr_input": hmr_input

}

        # ---------------------------------------------
        # RUN AI ENGINE
        # ---------------------------------------------

        with st.spinner("Running AI Digital Twin Analysis..."):

            twin = predict(inputs)
                    # ============================================
            # SAVE PREDICTION HISTORY
            # ============================================

            log_data = {

                "Timestamp": datetime.now(),

                "Suction Pressure (bar)": suction,

                "Discharge Pressure (bar)": discharge,

                "Voltage (V)": voltage,

                "Current (A)": current,

                "Flow Rate": flow,

                "HMR Difference": hmr_input,

                "ML Power (kW)": twin["ml_power"],


                "Physics Power (kW)": twin["physics_power"],


                "Hybrid Power (kW)": twin["predicted_power"],

                "Model Difference (kW)": twin.get(
                    "model_difference",
                    0
                ),

                "Predicted Energy (kWh)": twin.get(
                    "predicted_energy",
                    0
                ),

                "Health (%)": twin.get(
                    "health",
                    0
                )
            }


            file_path = "data/prediction_history.csv"


            if os.path.exists(file_path):

                old_data = pd.read_csv(file_path)

                new_data = pd.DataFrame([log_data])

                final_data = pd.concat(

                    [
                        old_data,
                        new_data
                    ],

                    ignore_index=True

                )


            else:

                final_data = pd.DataFrame(

                    [log_data]

                )


            final_data.to_csv(

                file_path,

                index=False

            )

        # ---------------------------------------------
        # VALIDATE PREDICTION
        # ---------------------------------------------

        if not twin["valid"]:

            st.error("Invalid operating conditions.")

            for warning in twin["warnings"]:

                st.warning(warning)

            return

        # ---------------------------------------------
        # SAVE RESULT
        # ---------------------------------------------

        st.session_state["twin"] = twin
        st.session_state["inputs"] = inputs
                # =====================================================
        # PREDICTION COMPLETED
        # =====================================================

                # =====================================================
        # PREDICTION COMPLETED
        # =====================================================

        st.success(
            "AI Digital Twin analysis completed successfully."
        )

        st.markdown("### Next Steps")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.info(
                """
Dashboard

View the latest compressor
health and overall system
status.
                """
            )

        with col2:

            st.info(
                """
Digital Twin

Review engineering
analysis and Hybrid AI
prediction.
                """
            )

        with col3:

            st.info(
                """
Reports

Generate and export
the complete engineering
report.
                """
            )

        st.divider()

        st.success(
            "Prediction has been stored successfully. Navigate using the sidebar to continue your analysis."
        )