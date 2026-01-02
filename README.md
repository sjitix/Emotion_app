!! The site can be accessed  by using this url https://emotionapp-lcyligtgivazbf3jcuxcha.streamlit.app/  !!
Due to inactivity , the app may temporarily shut down. Click on the button "get this app back up" and wait a few minutes and then it will work as intended.




General outline:
Reflectify is a journaling web application that analyzes the emotional content of user
entries. The app takes a journal entry as input and outputs the detected emotions with their intensity
scores, an interpretation of the entry , and a suggestion for improving your mood.
How it works The user writes a journal entry in a text area. When they click "Analyze", the app first sends
the text to the Groq API (Llama 3.1 model) which simplifies the entry by removing sarcasm, misleading
phrases, and indirect expressions. This preprocessing step eliminates noise and transforms the text into a
direct form of expressing emotions, making detection more accurate.The simplified text is then passed to
a roBERTa emotion classification model from HuggingFace. The model analyzes each word and
increases the numerical values of emotions stored within it. It outputs a dictionary of emotions with their
confidence scores. This dictionary is sorted in descending order, and the top 6 dominant emotions are
displayed to the user as progress bars and a pie chart. In the records page the entry, along with the
dominant emotion and its score are displayed as a usage history of the app , which can be also
visualised through the chart above this history log.


Data storage:
All journal entries are stored in google sheets.We created a google cloud service account
with access to the sheets API. The service account has secret credentials (API keys and private keys)
stored in a local secrets file and in the secrets specifications of the app on the streamlit cloud. These
credentials authenticate the app and grant permission to read and write to the spreadsheet
Code structure The project is split into three files:

emo_gem.py - The main streamlit app that handles the user interface, displays results, and coordinates
the other components

api_code.py - Contains all backend functions: loading models, connecting to APIs, analyzing emotions,
and saving data

records.py -(found in pages folder) - A separate page that displays past journal entries

Libraries used:

● streamlit - web application framework for building the interactive user interface

● groq - API client for connecting to the Llama 3.1 model

● transformers - HuggingFace library for loading and running the RoBERTa model

● torch - machine learning backend required by the transformers library

● gspread - allows Python to read and write data from the Google sheets

● google-auth - handles authentication with Google Cloud using the service account credentials

● plotly - creates the pie chart visualization of emotion scores

Design summary:
The app uses streamlit's sidebar to create a navigation menu where users can switch
between the main analysis page and the records page. Results are displayed using streamlit's built in
progress bars for individual emotions, while plotly generates a pie chart showing the emotion distribution.
The layout uses streamlit columns to place the chart and text side by side for an organized look
