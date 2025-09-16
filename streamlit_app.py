import streamlit as st
from chatbot import generate_response_stream  # Import the streaming function from chatbot.py
import os
from config import (
    SUPPORTED_LANGUAGES,
    UI_STRINGS,
    LANGUAGE_DISPLAY_TO_CODE,
    DEFAULT_LANGUAGE
)

# Function to handle language change
def handle_language_change():
    """Reset chat history when language is changed"""
    if "current_language" in st.session_state and \
       st.session_state.current_language != st.session_state.language_code:
        # Reset messages
        st.session_state.messages = []
    # Update current language
    st.session_state.current_language = st.session_state.language_code

# Initialize session state for language and chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_language" not in st.session_state:
    st.session_state.current_language = DEFAULT_LANGUAGE

# Streamlit app configuration with sidebar
st.set_page_config(page_title="Bilingual Chatbot", page_icon="🤖", layout="wide")

# Language selector in sidebar with better accessibility
st.sidebar.title("Language / Èdè / Langue")
st.sidebar.markdown("### Select your preferred language for the chatbot:")
language_display = st.sidebar.radio(
    "Chatbot language",
    list(LANGUAGE_DISPLAY_TO_CODE.keys()),
    key="language_display",
    on_change=lambda: setattr(st.session_state, "language_code", 
                             LANGUAGE_DISPLAY_TO_CODE[st.session_state.language_display])
)

# Set language code from display name
if "language_code" not in st.session_state:
    st.session_state.language_code = LANGUAGE_DISPLAY_TO_CODE[language_display]

# Call the handler to check if language was changed
handle_language_change()

# Get current language code
current_lang = st.session_state.current_language

# Title and description in selected language
st.title(UI_STRINGS[current_lang]["title"])
st.write(UI_STRINGS[current_lang]["welcome"])

# Display chat history
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field for user message
# Use the current language from session state
if prompt := st.chat_input(UI_STRINGS[current_lang]["input_placeholder"]):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Stream the assistant's response
    with st.chat_message("assistant"):
        response_container = st.empty()  # Placeholder for streaming response
        full_response = ""  # Accumulate the streamed response
        
        # Show loading message in the appropriate language
        response_container.markdown(UI_STRINGS[current_lang]["loading"])
        
        # Stream the response from the chatbot with the selected language
        for chunk in generate_response_stream(prompt, current_lang):
            full_response += chunk
            response_container.markdown(full_response)  # Update the UI with each chunk
        
        # Add the complete response to chat history
        message_data = {"role": "assistant", "content": full_response, "language": current_lang}
        st.session_state.messages.append(message_data)

# Add a clear chat button with language-specific text and better feedback
clear_col1, clear_col2 = st.columns([1, 5])
with clear_col1:
    if st.button("🗑️", help=UI_STRINGS[current_lang]["clear_chat"]):
        # Show feedback
        with clear_col2:
            st.info("Clearing conversation...")
            
        # Reset messages and refresh the page
        st.session_state.messages = []
        st.rerun()