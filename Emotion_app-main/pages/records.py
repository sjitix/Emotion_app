import streamlit as st
from api_code import sheet

#page name(in tab) and display
st.set_page_config(page_title="Records",
                   layout="wide",
                   initial_sidebar_state="expanded")

#sheet holds a reference to our googl spreadsheet
sheet = sheet()

# creates custom navigation 
st.sidebar.title("Navigation")
st.sidebar.page_link("emo_gem.py", label="Home")
st.sidebar.page_link("pages/records.py", label="Records")

st.markdown("<h1 style='color: #FFFFFF;'>Emotion Records</h1>", unsafe_allow_html=True)

#all_data stores a nested list where each inner list is a row from google sheets
all_data = sheet.get_all_values()


if len(all_data) > 1: 
    my_records = [] 
    for row in all_data[1:]:
        if len(row) >= 4 and row[0]:
             #converts each row into a dictionary
             #and adds it to the list my_records
            my_records.append({
                "date": row[0],
                "emotion": row[1],
                "score": row[2],
                "entry": row[3]
            })

    #count how many times each emotion appears
    #stores it into a dictionary
    emotion_counts = {}
    for item in my_records:
        emotion = item["emotion"]
        if emotion in emotion_counts:
            emotion_counts[emotion] += 1
        else:
            emotion_counts[emotion] = 1

    st.subheader("Emotion Counts")

    #creates a chart based on the emotion_counts dictionary
    st.bar_chart(emotion_counts)

    st.divider()

    st.subheader("Journal Entries")
    st.caption("Click on an entry to expand it")

    #reverse the order of the entries so that it starts with the latest one
    my_records.reverse()

    #for each entry desplay date , main emotion , and score + entry itself
    for item in my_records:
        with st.expander(f"**{item['date']} | {item['emotion']} | {item['score']}**"):
            st.write(item["entry"])
else:
    st.write("No records yet")
