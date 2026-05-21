import streamlit as st
from google import genai

# API Key yt i saktë
API_KEY = "AIzaSyB8sMBHzHqQnwnfvu6aVNQOMr6H4N5Y1WY"

st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="centered")

st.markdown("<h1 style='text-align: center; color: #4A90E2;'>🤖 AI Chat Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #777;'>Pyetni çfarë të dëshironi dhe AI do t'ju përgjigjet!</p>", unsafe_allow_html=True)
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if pyetja := st.chat_input("Shkruaj diçka këtu..."):
    with st.chat_message("user"):
        st.markdown(pyetja)
    
    st.session_state.messages.append({"role": "user", "content": pyetja})
    
    try:
        # Lidhja zyrtare përmes librarisë Google GenAI
        client = genai.Client(api_key=API_KEY)
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=pyetja,
        )
        pergjigja_ia = response.text
            
    except Exception as e:
        pergjigja_ia = f"Ndodhi një gabim gjatë lidhjes: {str(e)}"
    
    with st.chat_message("assistant"):
        st.markdown(pergjigja_ia)
    
    st.session_state.messages.append({"role": "assistant", "content": pergjigja_ia})