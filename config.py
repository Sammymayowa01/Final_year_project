"""
Configuration file for bilingual chatbot application
Contains language settings, system prompts, and UI strings
"""

# Language configurations including model settings and system prompts
SUPPORTED_LANGUAGES = {
    "yoruba": {
        "name": "Yorùbá",
        "code": "yoruba",
        "model": "deepseek-ai/DeepSeek-V3",
        "system_prompt": (
            "You are a friendly and intelligent chatbot. "
            "You MUST respond ONLY in Yorùbá language. "
            "Do NOT use English or any other language. "
            "Respond to the user's message in Yorùbá, "
            "even if they write to you in another language."
        )
    },
    "french": {
        "name": "Français",
        "code": "french",
        "model": "deepseek-ai/DeepSeek-V3",
        "system_prompt": (
            "You are a friendly and intelligent chatbot. "
            "You MUST respond ONLY in French language. "
            "Do NOT use English or any other language. "
            "Respond to the user's message in French, "
            "even if they write to you in another language."
        )
    }
}

# UI strings for different languages
UI_STRINGS = {
    "yoruba": {
        "title": "Yorùbá Chatbot",
        "welcome": "Kí ni mo lè ṣe fún ẹ? (What can I do for you?)",
        "input_placeholder": "Ṣe ìbéèrè rẹ níbí (Enter your query here)",
        "clear_chat": "Kọ Ìtàn Ìkọ̀rọ̀ (Clear Chat)",
        "loading": "Ń gbéjáde... (Loading...)",
        "error": "Àṣìṣe wáyé (An error occurred)",
        "language_selector": "Yan Èdè (Select Language)"
    },
    "french": {
        "title": "Assistant Conversationnel",
        "welcome": "Que puis-je faire pour vous? (What can I do for you?)",
        "input_placeholder": "Posez votre question ici (Enter your query here)",
        "clear_chat": "Effacer la conversation (Clear Chat)",
        "loading": "Chargement... (Loading...)",
        "error": "Une erreur est survenue (An error occurred)",
        "language_selector": "Choisir la langue (Select Language)"
    }
}

# Language mapping between display name and code
LANGUAGE_DISPLAY_TO_CODE = {
    "Yorùbá": "yoruba",
    "Français": "french"
}

# Default language
DEFAULT_LANGUAGE = "yoruba"