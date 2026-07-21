import streamlit as st

st.set_page_config(
    page_title="Sidebar Test",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("TEST SIDEBAR")

st.title("Main Page")
st.write("If you can see the sidebar, your project is fine.")