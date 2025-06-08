import streamlit as st
from chatbot import generate_response_stream  # Import the streaming function from chatbot.py
import pyttsx3
import os
import tempfile
from config import (
    SUPPORTED_LANGUAGES,
    UI_STRINGS,
    TTS_CONFIG,
    LANGUAGE_DISPLAY_TO_CODE,
    DEFAULT_LANGUAGE
)

# Function to handle language change
def handle_language_change():
    """Reset chat history when language is changed"""
    if "current_language" in st.session_state and \
       st.session_state.current_language != st.session_state.language_code:
        # Clean up audio files before clearing chat
        for message in st.session_state.messages:
            if "audio_path" in message:
                try:
                    os.unlink(message["audio_path"])
                except:
                    pass
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

# Function to generate and save audio file using pyttsx3
def text_to_speech(text, language):
    """
    Convert text to speech using pyttsx3 with enhanced error handling
    and language-specific settings.
    """
    if not text or len(text.strip()) == 0:
        st.warning(f"Cannot generate audio for empty text")
        return None
        
    try:
        # Initialize pyttsx3 engine
        engine = pyttsx3.init()
        
        # Get language-specific TTS settings
        tts_settings = TTS_CONFIG.get(language, TTS_CONFIG[DEFAULT_LANGUAGE])
        
        # Set properties based on language
        engine.setProperty("rate", tts_settings["rate"])
        engine.setProperty("volume", tts_settings["volume"])
        
        # Try to set language-specific voice if available
        voices = engine.getProperty('voices')
        voice_found = False
        
        if language == "french":
            # Try to find a French voice
            french_voice = next((v for v in voices if "french" in v.name.lower()), None)
            if french_voice:
                engine.setProperty('voice', french_voice.id)
                voice_found = True
        
        # If we didn't find a specific voice, log it but continue with default
        if not voice_found and language != DEFAULT_LANGUAGE:
            st.info(f"No specific voice found for {SUPPORTED_LANGUAGES[language]['name']}. Using default voice.")
        
        # Create a temporary file for the audio (using WAV for pyttsx3)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            audio_path = temp_audio.name
            # Save the text as audio
            engine.save_to_file(text, audio_path)
            engine.runAndWait()
            
            # Verify the file exists and has content
            if os.path.exists(audio_path) and os.path.getsize(audio_path) > 0:
                return audio_path
            else:
                st.error(f"Audio file was created but appears to be empty")
                return None
                
    except Exception as e:
        st.error(f"{UI_STRINGS[language]['error']}: {e}")
        return None

# Display chat history
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Add playback button for assistant messages with audio
        if message["role"] == "assistant" and "audio_path" in message:
            col1, col2 = st.columns([1, 20])
            with col1:
                if st.button("🔊", key=f"play_audio_{idx}", help=f"Play audio message {idx+1}"):
                    with col2:
                        st.audio(message["audio_path"])

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
        
        # Generate audio for the full response
        audio_path = text_to_speech(full_response, current_lang)
        
        # Add the complete response and audio path to chat history
        message_data = {"role": "assistant", "content": full_response, "language": current_lang}
        if audio_path:
            message_data["audio_path"] = audio_path
            # Display play button for the latest audio response
            st.info("🔊 Audio response is available")
            col1, col2 = st.columns([1, 20])
            with col1:
                if st.button("🔊", key="play_latest_audio", help="Play latest audio response"):
                    with col2:
                        st.audio(audio_path)
        
        # Add message to session state
        st.session_state.messages.append(message_data)

# Add a clear chat button with language-specific text and better feedback
clear_col1, clear_col2 = st.columns([1, 5])
with clear_col1:
    if st.button("🗑️", help=UI_STRINGS[current_lang]["clear_chat"]):
        # Show feedback
        with clear_col2:
            st.info("Clearing conversation...")
            
        # Clean up audio files
        deleted_count = 0
        error_count = 0
        for message in st.session_state.messages:
            if "audio_path" in message and message["audio_path"]:
                try:
                    os.unlink(message["audio_path"])
                    deleted_count += 1
                except Exception as e:
                    error_count += 1
                    st.warning(f"Could not delete audio file: {e}")
        
        # Reset messages and refresh the page
        st.session_state.messages = []
        st.rerun()
