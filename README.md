# Multilingual Chatbot with Text-to-Speech

A Streamlit-based chatbot application that supports Yorùbá and French languages with text-to-speech capabilities, powered by Together AI's API.

## Features

- **Multilingual Support**: Chat in Yorùbá and French languages
- **Text-to-Speech**: Listen to the chatbot's responses with language-appropriate voice settings
- **Simple UI**: Easy-to-use interface with language selection
- **Streaming Responses**: Messages appear in real-time as they are generated

## Prerequisites

- Python 3.8 or higher
- Together AI API key ([Get one here](https://together.ai))
- Internet connection for API calls
- Speakers or headphones for audio playback

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Ayodeji90/MultiLingual_Chatbot.git
   cd MultiLingual_Chatbot
   ```

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root directory and add your Together AI API key:
   ```
   TOGETHERAI_API_KEY=your_api_key_here
   ```

## Local Development

To run the application locally:

```
streamlit run streamlit_app.py
```

This will start the Streamlit server and open the application in your web browser.

## Deployment to Streamlit Cloud

1. **Push your code to GitHub** (already done)

2. **Set up Streamlit Cloud deployment**:
   - Go to [Streamlit Cloud](https://streamlit.io/cloud)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository, branch, and the main file (`streamlit_app.py`)
   - In Advanced Settings, add your Together AI API key as a secret:
     - Key: `TOGETHERAI_API_KEY`
     - Value: your_api_key_here

3. **Deploy and share**:
   - Click "Deploy"
   - Once deployed, Streamlit will provide a URL you can share with your test users

## Configuration

The application supports configuration through the `config.py` file:

- Language settings for Yorùbá and French
- TTS settings for each language
- UI strings and translations

## Usage

1. Select your preferred language from the sidebar
2. Type your message in the chat input box
3. The chatbot will respond in the selected language
4. Click the sound icon to listen to the response

## Troubleshooting

- **TTS Issues**: If text-to-speech doesn't work, ensure your system has audio capabilities and the necessary TTS engines installed
- **API Issues**: Check your API key and internet connection
- **Language Support**: The application currently only supports Yorùbá and French languages

## License

This project is licensed under the MIT License - see the LICENSE file for details.

