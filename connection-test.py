import os
import requests
import base64

with open('token', 'r') as file:
    # Read the token from the file
    GPT4V_KEY = file.read().strip()

# IMAGE_PATH = "YOUR_IMAGE_PATH"
# encoded_image = base64.b64encode(open(IMAGE_PATH, 'rb').read()).decode('ascii')
headers = {
    "Content-Type": "application/json",
    "api-key": GPT4V_KEY,
}

# Payload for the request
payload = {
  "messages": [
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "You are an AI assistant that helps people find information."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Who are you?"
        }
      ]
    },
    # {
    #   "role": "assistant",
    #   "content": [
    #     {
    #       "type": "text",
    #       "text": "I am an AI assistant designed to help you find information, answer questions, and provide assistance with various topics. If you have any questions or need help with something specific, feel free to ask!"
    #     }
    #   ]
    # }
  ],
#   "temperature": 0.7,
#   "top_p": 0.95,
#   "max_tokens": 800
}

GPT4V_ENDPOINT = "https://deep-ai-west-us-3.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview"

# Send request
try:
    response = requests.post(GPT4V_ENDPOINT, headers=headers, json=payload)
    response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
except requests.RequestException as e:
    raise SystemExit(f"Failed to make the request. Error: {e}")

# Handle the response as needed (e.g., print or process)
print(response.json())