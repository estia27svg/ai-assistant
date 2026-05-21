import streamlit as st
import requests

# API Key i ri që sapo krijove (bëj Paste brenda thonjëzave)
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
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        headers = {"Content-Type": "application/json"}
        payload = {"contents": [{"parts": [{"text": pyetja}]}]}
        
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        data = response.json()
        
        if response.status_code == 200:
            pergjigja_ia = data['candidates'][0]['content']['parts'][0]['text']
        else:
            pergjigja_ia = "Gabim lidhjeje me serverin e Google."
            
    except Exception as e:
        pergjigja_ia = "Ndodhi një gabim gjatë lidhjes."
    
    with st.chat_message("assistant"):
        st.markdown(pergjigja_ia)
    
    st.session_state.messages.append({"role": "assistant", "content": pergjigja_ia})