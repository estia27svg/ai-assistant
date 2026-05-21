import streamlit as st
import requests

# API Key yt i saktë
API_KEY = "AIzaSyB08yOyu_FH0adF53y1j11xbZ0bmzGtd0c"

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
        # Përdorim modelin 1.5-flash që është 100% i përshtatshëm me këtë strukturë
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        
        payload = {
            "contents": [{
                "parts": [{"text": pyetja}]
            }]
        }
        
        response = requests.post(url, json=payload, timeout=15)
        data = response.json()
        
        if response.status_code == 200:
            pergjigja_ia = data['candidates'][0]['content']['parts'][0]['text']
        else:
            # Nëse ka gabim, na tregon fiks çfarë thotë Google
            error_details = data.get('error', {}).get('message', 'Gabim i panjohur')
            pergjigja_ia = f"Gabim ({response.status_code}): {error_details}"
            
    except Exception as e:
        pergjigja_ia = f"Ndodhi një gabim gjatë lidhjes: {str(e)}"
    
    with st.chat_message("assistant"):
        st.markdown(pergjigja_ia)
    
    st.session_state.messages.append({"role": "assistant", "content": pergjigja_ia})
