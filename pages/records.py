import streamlit as st

st.set_page_config(page_title="Records", layout="centered",
                   initial_sidebar_state="expanded")

# Hide default streamlit page navigation
st.markdown("""
<style>
    [data-testid="stSidebarNav"] {display: none;}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("Navigation")
st.sidebar.page_link("emo_gem.py", label="Home")
st.sidebar.page_link("pages/records.py", label="Records")

st.markdown("<h1 style='color: red;'>Records</h1>", unsafe_allow_html=True)

# Add your records content here
st.write("Your emotion records will appear here.")
