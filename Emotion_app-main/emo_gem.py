import streamlit as st
import plotly.graph_objects as go
from api_code import (
    groq,
    sheet,
    load_model,
    clarify_text,
    emotions,
    saving_entry,
    suggestion
)
#setting title of the website , layout
st.set_page_config(page_title="Emotion Analzer",
                   layout="centered",
                   initial_sidebar_state="expanded")

#connection to groq , object which makes requests to groq api
client = groq()

#adress/object pointing to the google sheet
sheet = sheet()

#setting classifier , loads roberta model
model = load_model()

# creates a navigation menu in the sidebar
st.sidebar.title("Navigation")
st.sidebar.page_link("emo_gem.py", label="Home")
st.sidebar.page_link("pages/records.py", label="Records")


#styled title
st.markdown("""
    <h1 style='text-align: center; color: #FFFFFF; font-size: 3.5em; font-weight: bold;
               text-shadow: 2px 2px 4px rgba(0,0,0,0.3); margin-bottom: 0;'>
        Reflectify
    </h1>
    <p style='text-align: center; color: #E8E8E8; font-style: italic; font-size: 1.2em;
              margin-top: 10px; border-bottom: 2px solid #667EEA; padding-bottom: 20px;'>
        Understand your emotions through journaling
    </p>
""", unsafe_allow_html=True)

st.divider()

#takes user input from the text area box
user_input = st.text_area("How are you feeling today?", height=150)


#creates button of full width 
#button_pressed takes value true/false when button is pressed / not pressed
button_pressed = st.button("Analyze Emotions", use_container_width=True)


if button_pressed:

    #checks for sufficient entry
    if len(user_input.strip()) < 5:
        st.warning("please write a bit more (at least 5 characters)")
    else:
        #if the text is too small , it is not processed by the api
        #goes directly to roberta model , to avoid overexplanation of the api when faced with little context
        if len(user_input.split()) <= 6:
            clean_text = user_input
        else:
            #if the text is big enough give it to the api so it can simplify it
            clean_text = clarify_text(client, user_input)

        #gives the simplified text to roberta model 
        #emotions_list stores the sorted emotions outputed from the model
        emotions_list = emotions(model, clean_text)

        #showcase of api s interpretation of the text
        st.text("How I interpreted your entry:")
        st.write(clean_text)

        st.divider()


        #show the dominant emotion(the one at the top of the sorted list)
        top_emotion = emotions_list[0]
        st.subheader(f"Dominant Emotion: {top_emotion["label"]}")


        st.divider()

   
        total = 0
        
        #calculate sum of the emotion values
        for e in emotions_list[:6]:
            total = total + e["score"]

        #creates 2 column-like containers
        col_left, col_right = st.columns(2)



        #progress bar 
        with col_left:
            st.subheader("Emotion Breakdown")

            for item in emotions_list[:6]:
                #calculating percentage of each emotion by dividing its score with the total sum of all scores
                pct = item["score"] / total

                #creates 2 column-like containers but the firt one takes up 75% of the space
                c1, c2 = st.columns([3, 1])
                with c1:
                    #creates progress bar 
                    st.progress(pct, text=item["label"])
                with c2:
                    #writes percentage
                    st.write(f"{pct:.1%}")



        #pie chart
        with col_right:
            st.subheader("Emotion Distribution")
            names = []
            scores = []

            for e in emotions_list[:6]:
                  
                #creates a list of the emotions
                names.append(e["label"])

                pct = (e["score"] / total) * 100
                 
                #creates list of percentafes
                scores.append(pct)
            

            #creates a pie chart using plotly , with data from labels and values
            chart = go.Figure(data=[go.Pie(labels=names, values=scores)])
            
            #shows the chart on the page , sets full width for it
            st.plotly_chart(chart, use_container_width=True)

        st.divider()
        st.subheader("Suggestion")

        #another api request is made for ai to generate a sugestion for improving the users mood
        tip = suggestion(client, top_emotion["label"], user_input)
        st.info(tip)

        #saves the journal entry to your Google Sheet
        saving_entry(sheet, top_emotion["label"], f"{top_emotion["score"]:.1%}", user_input)
