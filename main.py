import streamlit as st
import google.generativeai as genai
import random

# Set up Google AI API key
API_KEY = "AIzaSyAjUUE5avUriBjIAaCuTmVJ9cKkSR28tBI"  # Replace with your actual Google AI Studio API key
genai.configure(api_key=API_KEY)

# Sample fallback responses (used if API fails)
fallback_responses = {
    "hello": ["Hi there!", "Hello! How can I help you?"],
    "help": ["I can assist with basic questions!", "What do you need help with?"],
    "bye": ["Goodbye!", "See you later!"],
    "default": ["Sorry, I didn't understand.", "Can you rephrase that?"]
}

# Initialize the model (updated to a supported one)
model = genai.GenerativeModel('gemini-1.5-flash')  # Use 'gemini-1.5-pro' if you need more advanced responses

def get_ai_response(user_input):
    try:
        response = model.generate_content(user_input)
        return response.text
    except Exception as e:
        st.error(f"API error: {e}")
        return random.choice(fallback_responses.get(user_input.lower(), fallback_responses["default"]))

# Streamlit app
st.title("AI Chatbot")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        response = get_ai_response(prompt)
        st.write(response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})