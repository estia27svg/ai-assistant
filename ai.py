import streamlit as st
import requests

# Vendos API Key-in tënd të ri këtu brenda thonjëzave
API_KEY = "AIzaSyD1mxaiK4UEBDFPAjSmSlchAoIIWj6MzIM"

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
        # URL dhe struktura zyrtare e saktë
        url = f# URL e saktë e përditësuar pa v1beta
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": pyetja}
                    ]
                }
            ]
        }
        
        response = requests.post(url, json=payload, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            pergjigja_ia = data['candidates'][0]['content']['parts'][0]['text']
        else:
            # Nëse ka gabim, na tregon fiks çfarë thotë Google që ta shohim
            pergjigja_ia = f"Gabim nga Google ({response.status_code}): {response.text}"
            
    except Exception as e:
        pergjigja_ia = f"Ndodhi një gabim gjatë lidhjes: {str(e)}"
    
    with st.chat_message("assistant"):
        st.markdown(pergjigja_ia)
    
    st.session_state.messages.append({"role": "assistant", "content": pergjigja_ia})