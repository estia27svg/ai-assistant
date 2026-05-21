import streamlit as st
import requests

# Vendos çelësin tënd të Groq (gsk_...) brenda thonjëzave:
API_KEY = "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" 

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
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": pyetja}]
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        data = response.json()
        
        if response.status_code == 200:
            pergjigja_ia = data['choices'][0]['message']['content']
        else:
            pergjigja_ia = f"Gabim nga serveri: {response.status_code}"
            
    except Exception as e:
        pergjigja_ia = "Ndodhi një gabim gjatë lidhjes. Ju lutem provojeni përsëri."
    
    with st.chat_message("assistant"):
        st.markdown(pergjigja_ia)
    
    st.session_state.messages.append({"role": "assistant", "content": pergjigja_ia})
