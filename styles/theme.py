# ==========================================================
# GASONET AI DIGITAL TWIN
# THEME
# ==========================================================

import streamlit as st


def load_theme():

    st.markdown(
        """
        <style>

        /* =====================================
           FONT
        ===================================== */

        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

        html,
        body,
        [class*="css"] {

            font-family: 'Poppins', sans-serif;

        }


        /* =====================================
           MAIN CONTENT SPACING
        ===================================== */

        .block-container{

            padding-top:1rem;

            padding-bottom:2rem;

            padding-left:2rem;

            padding-right:2rem;

        }
                /* =====================================
           SIDEBAR
        ===================================== */

        section[data-testid="stSidebar"]{

            background-color:#f8f9fa;

            border-right:1px solid #e6e6e6;

        }


        section[data-testid="stSidebar"] img{

            display:block;

            margin:auto;

            margin-top:10px;

            margin-bottom:10px;

        }


        section[data-testid="stSidebar"] h1{

            text-align:center;

            font-size:26px;

            font-weight:700;

        }


        section[data-testid="stSidebar"] p{

            text-align:center;

            color:#666666;

            font-size:14px;

        }


        section[data-testid="stSidebar"] hr{

            margin-top:15px;

            margin-bottom:15px;

        }
                /* =====================================
           BUTTONS
        ===================================== */

        .stButton > button{

            width:100%;

            border-radius:8px;

            font-weight:600;

            border:1px solid #d0d7de;

            padding:0.55rem;

        }


        .stButton > button:hover{

            border-color:#1f77b4;

        }



        /* =====================================
           INPUT BOXES
        ===================================== */

        .stNumberInput input{

            border-radius:8px;

        }


        .stTextInput input{

            border-radius:8px;

        }


        .stSelectbox div[data-baseweb="select"]{

            border-radius:8px;

        }


        .stTextArea textarea{

            border-radius:8px;

        }



        /* =====================================
           SLIDERS
        ===================================== */

        .stSlider{

            padding-top:0.5rem;

        }
                /* =====================================
           HEADINGS
        ===================================== */

        h1{

            font-size:2.1rem !important;

            font-weight:700 !important;

            margin-bottom:0.25rem !important;

        }

        h2{

            font-size:1.7rem !important;

            font-weight:650 !important;

            margin-top:1rem !important;

            margin-bottom:0.5rem !important;

        }

        h3{

            font-size:1.35rem !important;

            font-weight:600 !important;

            margin-top:0.75rem !important;

            margin-bottom:0.4rem !important;

        }

        h4{

            font-size:1.15rem !important;

            font-weight:600 !important;

        }

        hr{

            margin-top:0.5rem;

            margin-bottom:1rem;

        }
                /* =====================================
           METRIC CARDS
        ===================================== */

        div[data-testid="stMetric"]{

            background-color:#ffffff;

            border:1px solid #e5e7eb;

            border-radius:10px;

            padding:15px;

            box-shadow:0 1px 4px rgba(0,0,0,0.08);

        }


        div[data-testid="stMetricLabel"]{

            font-size:14px;

            font-weight:600;

            color:#555555;

        }


        div[data-testid="stMetricValue"]{

            font-size:32px;

            font-weight:700;

            color:#222222;

        }


        div[data-testid="stMetricDelta"]{

            font-size:14px;

        }

        </style>
        """,
        unsafe_allow_html=True
    )