import streamlit as st

import pandas as pd

import os

from styles.theme import load_theme



def prediction_history():


    # =====================================================
    # LOAD THEME
    # =====================================================

    load_theme()


    # =====================================================
    # PAGE HEADER
    # =====================================================


    st.title(
        "Prediction History"
    )


    st.caption(
        "Historical record of AI Digital Twin compressor predictions."
    )


    st.divider()


    # =====================================================
    # LOAD HISTORY FILE
    # =====================================================


    file_path = "data/prediction_history.csv"


    if not os.path.exists(file_path):


        st.warning(

            "No prediction history available. Run a prediction first."

        )


        return



    history = pd.read_csv(

        file_path

    )
        # =====================================================
    # SUMMARY CARDS
    # =====================================================


    st.subheader(

        "Compressor Prediction Summary"

    )


    total_predictions = len(

        history

    )


    latest_health = history[

        "Health (%)"

    ].iloc[-1]


    average_health = history[

        "Health (%)"

    ].mean()



    col1, col2, col3 = st.columns(3)



    with col1:


        st.metric(

            "Total Predictions",

            total_predictions

        )



    with col2:


        st.metric(

            "Latest Health",

            f"{latest_health:.2f} %"

        )



    with col3:


        st.metric(

            "Average Health",

            f"{average_health:.2f} %"

        )



    st.divider()



    # =====================================================
    # HISTORY TABLE
    # =====================================================


    st.subheader(

        "Prediction Records"

    )


    st.dataframe(

        history,

        use_container_width=True

    )

        # =====================================================
    # DOWNLOAD EXCEL REPORT
    # =====================================================


    st.divider()


    st.subheader(

        "Export Prediction History"

    )


    excel_file = "data/prediction_history.xlsx"


    history.to_excel(

        excel_file,

        index=False

    )


    with open(excel_file, "rb") as file:


        st.download_button(

            label="Download Prediction History Excel",

            data=file,

            file_name="Prediction_History.xlsx",

            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

            use_container_width=True

        )