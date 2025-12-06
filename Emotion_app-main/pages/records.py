import streamlit as st

st.set_page_config(page_title="Records", layout="centered")

st.markdown("<h1 style='color: red;'>Records</h1>", unsafe_allow_html=True)
st.page_link("emo_gem.py", label="Back to Home")

# Add your records content here
st.write("Your emotion records will appear here.")
