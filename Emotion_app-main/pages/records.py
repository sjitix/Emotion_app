import streamlit as st

st.set_page_config(page_title="Records", layout="centered")

st.sidebar.title("Navigation")
if st.sidebar.button("Home"):
    st.switch_page("emo_gem.py")

st.markdown("<h1 style='color: red;'>Records</h1>", unsafe_allow_html=True)

# Add your records content here
st.write("Your emotion records will appear here.")
