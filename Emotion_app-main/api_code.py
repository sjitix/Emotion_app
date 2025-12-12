import streamlit as st
from groq import Groq
from transformers import pipeline
import gspread
from google.oauth2.service_account import Credentials
import time


def groq():

    #get groq api key from secrets
    my_key = st.secrets["GROQ_API_KEY"]

    return Groq(api_key=my_key)

#get authenticated googl sheet for records
#keys are in streamlit's secrets
def sheet():
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    )
    #uses gspread library for the spreadsheets and uses the credentials to create a client
    client1 = gspread.authorize(creds)
    
    #open the spreadsheet and get its first sheet (sheet1)
    sheet1 = client1.open("EmotionRecords").sheet1
    return sheet1

#the tag "@.." makes sure the model isnt loaded everytime
@st.cache_resource

#loads the model for text classification from the pipeline
def load_model():
    model = pipeline("text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)
    return model

#api simplifies jounrnal entry
def clarify_text(client, entry):
    my_prompt = f"""Rewrite this journal entry to make the TRUE emotions explicit and clear.

Rules:
- Identify what the person is feeling
- Rewrite using clear emotional language
- Simplify sarcasm, negations, and misleading phrases
- Keep it similar length to original
- Write in first person
- be objective, try to not overthink what the person is saying, if there is
sarcasm or contextual meaning involved then simplify it but don't always assume
there will be some hidden meaning. Sometimes there could be no hidden meaning
and sometimes there is. Try your best to simplify considering all this and reflect
the persons feelings.
-the simplified code you give cannot be longer than the original
-in fact it has to be as simplified , direct and clear as possible.
-if the entry is shorter than 6 words do not change it.
I reapeat:do not change it if its smaller or equal to 6 words!
your output should be the exact same as the original entry if its smaller than 6 words

Only output the rewritten text, nothing else.

Journal entry: {entry}"""
   
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": my_prompt}],
        max_tokens=500
    )
    result = response.choices[0].message.content.strip()
    return result
    
#sorts emotions based on score from the models output
def emotions(model, text):
    results = model(text)[0]
    sorted_list = sorted(results, key=lambda x: x["score"], reverse=True)
    return sorted_list


#saves entry and all the data needed for that entry

def saving_entry(sheet, emotion, score, entry):
    #gets the current dat and time and formats it as a string
    current_date = time.strftime("%Y-%m-%d %H:%M")
    sheet.append_row([current_date, emotion, score, entry])



#api generates suggestion for mood 
#based on given prompt
def suggestion(client, emotion, entry):
    my_prompt = f"""Based on this journal entry and the detected emotion "{emotion}", give a brief, helpful suggestion.

Journal entry: {entry}

Rules:
keep it to 2-3 sentences max
be warm and supportive , friendly
give one practical tip they can try right now
don't repeat what they wrote


Only output the suggestion, nothing else."""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": my_prompt}],
        max_tokens=150
    )
    result = response.choices[0].message.content.strip()
    return result
