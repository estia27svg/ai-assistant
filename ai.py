import streamlit as st
from openai import OpenAI

st.title("🤖 AI Assistant")

api_key = st.text_input("Vendos OpenAI API Key:", type="password")

if api_key:
    client = OpenAI(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Shkruaj mesazhin...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.write(user_input)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages
        )

        reply = response.choices[0].message.content

        with st.chat_message("assistant"):
            st.write(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})

else:
    st.info("Vendos API key për të filluar")
