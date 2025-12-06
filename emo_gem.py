import streamlit as st
import google.generativeai as genai
from transformers import pipeline

st.set_page_config(page_title="Emotion Analyzer",
                   layout="centered")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
gemini = genai.GenerativeModel('gemini-2.0-flash')

classifier = pipeline(
    "text-classification",
    model="SamLowe/roberta-base-go_emotions",
    top_k=None,
    device=-1
)

st.markdown("<h1 style='color: green;'>Emotion Analyzer</h1>", unsafe_allow_html=True)
st.markdown("*Understand your emotions through journaling*")
st.divider()

journal_entry = st.text_area("How are you feeling today?",
                             height=150)

if st.button("Analyze Emotions",
             use_container_width=True):

    if len(journal_entry.strip()) < 5:
        st.warning("Please write a bit more (at least 5 characters).")
    else:
        try:
            with st.spinner("Analyzing..."):
                clarify_prompt = f"""Rewrite this journal entry to make the TRUE emotions explicit and clear.

Rules:
- Identify what the person is feeling
- Rewrite using clear emotional language
- Simplify sarcasm, negations, and misleading phrases
- Keep it similar length to original
- Write in first person
- Be objective, try to not overthink what the person is saying, if there is
sarcasm or contextual meaning involved then simplify it but don't always assume
there will be some hidden meaning. Sometimes there could be no hidden meaning
and sometimes there is. Try your best to simplify considering all this and reflect
the persons feelings.

Only output the rewritten text, nothing else.

Journal entry: {journal_entry}"""

                response = gemini.generate_content(clarify_prompt)
                clarified_text = response.text.strip()

                raw_results = classifier(clarified_text)[0]

                sorted_results = sorted(raw_results,
                                        key=lambda x: x['score'],
                                        reverse=True)

            with st.expander("How I interpreted your entry"):
                st.write(clarified_text)

            st.divider()

            dominant = sorted_results[0]
            st.subheader(f"Dominant Emotion: {dominant['label'].capitalize()}")

            if dominant['score'] < 0.30:
                st.caption("(Low confidence)")

            st.divider()
            st.subheader("Emotion Breakdown")

            for emotion in sorted_results[:6]:
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.progress(emotion['score'], text=emotion['label'].capitalize())

                with col2:
                    st.write(f"{emotion['score']:.1%}")

        except Exception as e:
            st.error(f"Error: {str(e)}")
