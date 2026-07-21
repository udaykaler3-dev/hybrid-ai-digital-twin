import streamlit as st


def apply_theme():

    st.markdown(
        """
        <style>

        /* ================================
           Main App
        ================================= */

        .stApp{
            background-color:#F5F7FA;
        }

        /* ================================
           Sidebar
        ================================= */

        section[data-testid="stSidebar"]{
            background:#1E293B;
        }

        section[data-testid="stSidebar"] *{
            color:white;
        }

        /* ================================
           KPI Cards
        ================================= */

        div[data-testid="metric-container"]{

            background:white;

            border-radius:12px;

            padding:12px;

            border:1px solid #D6D6D6;

            box-shadow:0px 2px 8px rgba(0,0,0,0.08);

        }

        /* ================================
           Buttons
        ================================= */

        .stButton>button{

            width:100%;

            border-radius:10px;

            font-weight:bold;

        }

        /* ================================
           Tables
        ================================= */

        .stDataFrame{

            border-radius:10px;

        }

        /* ================================
           Headings
        ================================= */

        h1,h2,h3{

            color:#0F172A;

        }

        </style>
        """,
        unsafe_allow_html=True
    )