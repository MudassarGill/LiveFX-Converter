import streamlit as st
import requests
import json

# The URL of the FastAPI Backend
API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(page_title="LiveFX AI Converter", page_icon="💸", layout="centered")

st.title("LiveFX AI Converter")
st.write("Ask natural language questions about currency conversion! For example: `Convert 15 USD to PKR`.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask about exchange rates..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call FastAPI backend
    with st.chat_message("assistant"):
        with st.spinner("Calculating..."):
            try:
                response = requests.post(API_URL, json={"query": prompt})
                if response.status_code == 200:
                    data = response.json()
                    bot_reply = data.get("response", "Error missing response.")
                else:
                    bot_reply = f"Error from backend: HTTP {response.status_code}"
            except requests.exceptions.ConnectionError:
                bot_reply = "Backend error: Could not connect to API. Is the FastAPI server running?"
            except Exception as e:
                bot_reply = f"An unexpected error occurred: {str(e)}"
            
            st.markdown(bot_reply)
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
