import requests
from dotenv import load_dotenv
import os
import json
from config import SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE

# Load environment variables from .env file
load_dotenv()

# Together AI API configurations
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
TOGETHER_API_KEY = os.getenv("TOGETHERAI_API_KEY")

# Ensure API key is loaded
if not TOGETHER_API_KEY:
    raise ValueError("TOGETHERAI_API_KEY not found in .env file")

# Set headers for the API request
headers = {
    "Authorization": f"Bearer {TOGETHER_API_KEY}",
    "Content-Type": "application/json"
}

def generate_response_stream(message: str, language: str = DEFAULT_LANGUAGE):
    """
    Generate a streaming response using the DeepSeek model via Together AI's Inference API.
    Yields chunks of the response as they are received.
    
    Args:
        message (str): The user's message to respond to
        language (str): Language code ('yoruba' or 'french') for response
    """
    # Validate language and use default if not supported
    if language not in SUPPORTED_LANGUAGES:
        language = DEFAULT_LANGUAGE
        yield f"Warning: Unsupported language requested. Using {SUPPORTED_LANGUAGES[DEFAULT_LANGUAGE]['name']} instead."
    
    try:
        # Get language config from supported languages
        language_config = SUPPORTED_LANGUAGES[language]
        
        # Define the payload with stream enabled
        payload = {
            "model": language_config["model"],
            "messages": [
                {
                    "role": "system",
                    "content": language_config["system_prompt"]
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            "max_tokens": 1000,  # Adjust as needed
            "temperature": 0.7,  # Adjust for creativity vs. determinism
            "stream": True  # Enable streaming
        }
        
        # Make the POST request with streaming enabled
        with requests.post(TOGETHER_API_URL, headers=headers, json=payload, stream=True) as response:
            response.raise_for_status()  # Raise an error if the request fails
            
            # Process the streaming response line by line
            for line in response.iter_lines():
                if line:  # Ignore empty lines
                    # Decode the line and remove the "data: " prefix
                    decoded_line = line.decode('utf-8').strip()
                    if decoded_line.startswith("data: "):
                        data = decoded_line[6:]  # Remove "data: " prefix
                        
                        # Check for stream end signal
                        if data == "[DONE]":
                            break
                        
                        # Parse the JSON chunk
                        try:
                            chunk = json.loads(data)
                            if "choices" in chunk and len(chunk["choices"]) > 0:
                                delta = chunk["choices"][0].get("delta", {})
                                content = delta.get("content", "")
                                if content:
                                    yield content  # Yield each chunk of content
                        except json.JSONDecodeError:
                            continue  # Skip malformed chunks

    except requests.exceptions.RequestException as e:
        error_detail = e.response.text if e.response is not None else "No response body"
        yield f"Error communicating with the Together AI API: {e}\nDetails: {error_detail}"

# Example usage with streaming
if __name__ == "__main__":
    language_choice = input("Select language (yoruba/french): ").lower()
    user_message = input("Enter your query: ")
    print("Streaming response:")
    for chunk in generate_response_stream(user_message, language_choice):
        print(chunk, end='', flush=True)  # Print each chunk as it arrives
    print()  # Newline at the end
