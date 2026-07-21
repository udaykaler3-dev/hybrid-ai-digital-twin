import streamlit as st

from styles.theme import load_theme



def digital_twin():


    # =====================================================
    # LOAD THEME
    # =====================================================

    load_theme()



    # =====================================================
    # HEADER
    # =====================================================


    left, center, right = st.columns(
        [1,2,1]
    )


    with center:

       st.image(
    "assets/gasonet_logo.png",
    use_container_width=True
)


    st.title(
        "DIGITAL TWIN"
    )


    st.subheader(
        "Real-Time Booster Compressor Analysis"
    )


    st.caption(
        "Hybrid AI based compressor health monitoring and predictive maintenance system."
    )


    st.divider()



    # =====================================================
    # CHECK PREDICTION DATA
    # =====================================================


    if "twin" not in st.session_state:


        st.warning(
            "Run Manual Prediction before opening Digital Twin."
        )


        return



    twin = st.session_state["twin"]



    if not twin.get(
        "valid",
        False
    ):


        st.error(
            "Invalid prediction data."
        )


        return
        # =====================================================
    # CURRENT COMPRESSOR STATUS
    # =====================================================


    st.subheader(
        "Current Compressor Status"
    )


    health = twin.get(
        "health",
        0
    )



    col1 = st.columns(1)[0]



    with col1:


        st.metric(

            "Equipment Health",

            f"{health:.1f}%"

        )


    st.divider()



    # =====================================================
    # HEALTH INTERPRETATION
    # =====================================================


    if health >= 90:


        st.success(

            "Compressor operating under healthy conditions."

        )


    elif health >= 75:


        st.warning(

            "Compressor performance requires monitoring."

        )


    else:


        st.error(

            "Critical compressor condition detected. Maintenance inspection required."

        )


    st.divider()
        # =====================================================
    # HYBRID AI ANALYSIS
    # =====================================================


    st.subheader(
        "Hybrid AI Analysis"
    )


    ml_power = twin.get(
        "ml_power",
        0
    )


    physics_power = twin.get(
        "physics_power",
        0
    )


    model_difference = twin.get(
        "model_difference",
        0
    )

    hybrid_power = twin.get(
        "predicted_power",
        0
    )



    col1, col2, col3, col4 = st.columns(4)



    # -----------------------------------------------------
    # MACHINE LEARNING MODEL
    # -----------------------------------------------------


    with col1:


        with st.container(border=True):


            st.metric(

                "Machine Learning Prediction",

                f"{ml_power:.2f} kW"

            )


            st.caption(
                "Power prediction from trained AI model."
            )



    # -----------------------------------------------------
    # PHYSICS MODEL
    # -----------------------------------------------------


    with col2:


        with st.container(border=True):


            st.metric(

                "Physics-Based Prediction",

                f"{physics_power:.2f} kW"

            )


            st.caption(
                "Engineering model based prediction."
            )



    # -----------------------------------------------------
    # MODEL VALIDATION
    # -----------------------------------------------------


    with col3:


        with st.container(border=True):


            st.metric(

                "Model Difference",

                f"{model_difference:.2f} kW"

            )


            if model_difference <= 1:


                st.success(
                    "Excellent model agreement."
                )


            elif model_difference <= 3:


                st.warning(
                    "Minor prediction deviation."
                )


            else:


                st.error(
                    "Large deviation detected."
                )
        # -----------------------------------------------------
    # HYBRID DIGITAL TWIN OUTPUT
    # -----------------------------------------------------


    with col4:


        with st.container(border=True):


            st.metric(

                "Hybrid Predicted Power",

                f"{hybrid_power:.2f} kW"

            )


            st.caption(
                "Final AI + Physics corrected prediction."
            )            



    st.divider()
        # =====================================================
    # LIVE OPERATING CONDITIONS
    # =====================================================


    st.subheader(
        "Live Operating Conditions"
    )


    inputs = twin.get(
        "inputs",
        {}
    )



    col1, col2 = st.columns(
        2,
        gap="large"
    )



    # -----------------------------------------------------
    # PRESSURE PARAMETERS
    # -----------------------------------------------------


    with col1:


        with st.container(border=True):


            st.metric(

                "Suction Pressure",

                f"{inputs.get('suction',0):.2f} bar"

            )


            st.metric(

                "Discharge Pressure",

                f"{inputs.get('discharge',0):.2f} bar"

            )


            st.metric(
    "Compressor Delivery Flow",
    f"{inputs.get('flow',0):.2f} kg/hr"
)



    # -----------------------------------------------------
    # ELECTRICAL PARAMETERS
    # -----------------------------------------------------


    with col2:


        with st.container(border=True):


            st.metric(

                "Voltage",

                f"{inputs.get('voltage',0):.2f} V"

            )


            st.metric(

                "Current",

                f"{inputs.get('current',0):.2f} A"

            )


            st.metric(

                "HMR Difference",

                inputs.get(
                    "hmr_input",
                    "00:00:00"
                )

            )



    st.divider()
        # =====================================================
    # ENGINEERING PARAMETERS
    # =====================================================


    st.subheader(
        "Engineering Parameters"
    )


    features = twin.get(
        "features",
        {}
    )



    col1, col2 = st.columns(
        2,
        gap="large"
    )



    # -----------------------------------------------------
    # PRESSURE AND FLOW PARAMETERS
    # -----------------------------------------------------


    with col1:


        with st.container(border=True):


            st.metric(

                "Pressure Difference",

                f"{features.get('Pressure_Difference',0):.2f} bar"

            )


            st.metric(

                "Pressure Ratio",

                f"{features.get('Pressure_Ratio',0):.2f}"

            )


            st.metric(
    "Compressor Capacity Utilization",
    f"{features.get('Flow_Utilization',0)*100:.1f}%"
)


            st.metric(

                "Pressure Utilization",

                f"{features.get('Pressure_Utilization',0):.2f}"

            )



    # -----------------------------------------------------
    # LOAD PARAMETERS
    # -----------------------------------------------------


    with col2:


        with st.container(border=True):


            st.metric(

                "Electrical Load",

                f"{features.get('Electrical_Load',0):.2f}"

            )


            st.metric(

                "Load Index",

                f"{features.get('Load_Index',0):.2f}"

            )


            


            st.metric(

                "Motor Loading",

                f"{features.get('Motor_Loading',0):.2f}"

            )



    st.divider()
        # =====================================================
    # ENGINEERING ALARMS
    # =====================================================


    st.subheader(
        "Engineering Alarms"
    )


    alarms = twin.get(
        "warnings",
        []
    )


    if len(alarms) == 0:


        st.success(
            "No active engineering alarms detected."
        )


    else:


        for i, alarm in enumerate(
            alarms,
            start=1
        ):


            st.error(

                f"ALM-{i:03d} | {alarm}"

            )



    st.divider()



    # =====================================================
    # MAINTENANCE RECOMMENDATIONS
    # =====================================================


    st.subheader(
        "Maintenance Recommendations"
    )


    recommendations = twin.get(
        "recommendations",
        []
    )


    if len(recommendations) == 0:


        st.success(
            "No maintenance action required."
        )


    else:


        for recommendation in recommendations:


            st.info(
                recommendation
            )



    st.divider()



    # =====================================================
    # FINAL DIGITAL TWIN ASSESSMENT
    # =====================================================


    st.subheader(
        "Final Digital Twin Assessment"
    )


    if health >= 90:


        st.success(

            """
Digital Twin Status: NORMAL

The booster compressor is operating within healthy limits.

No immediate maintenance action is required.
            """

        )


    elif health >= 75:


        st.warning(

            """
Digital Twin Status: MONITORING REQUIRED

Compressor performance is acceptable but preventive monitoring is recommended.
            """

        )


    else:


        st.error(

            """
Digital Twin Status: CRITICAL

Compressor health is below acceptable operating limits.

Maintenance inspection is recommended.
            """

        )



    st.divider()