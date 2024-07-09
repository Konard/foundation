import sys
import os
import requests

# Function to write response to markdown file
def write_to_markdown(file_path, data):
    with open(file_path, 'w') as file:
        file.write(data)

# Check if there are enough arguments
if len(sys.argv) < 2:
    raise SystemExit("Usage: python cli.py <message> [optional_output_file]")

# Retrieve input arguments
message = sys.argv[1]
output_file = sys.argv[2] if len(sys.argv) > 2 else None

# Print the message for debugging
# print(f"Message: {message}")

# Read the token from the provided file
token_file_path = 'token'
try:
    with open(token_file_path, 'r') as file:
        GPT4V_KEY = file.read().strip()
except FileNotFoundError:
    raise SystemExit(f"Token file not found: {token_file_path}")

# Set up the headers for the request
headers = {
    "Content-Type": "application/json",
    "api-key": GPT4V_KEY,
}

# Payload for the request
payload = {
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": message
        }
      ]
    },
  ],
}

GPT4V_ENDPOINT = "https://deep-ai-west-us-3.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview"

# Send the request
try:
    response = requests.post(GPT4V_ENDPOINT, headers=headers, json=payload)
    response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
except requests.RequestException as e:
    raise SystemExit(f"Failed to make the request. Error: {e}")

# Handle and print the response
response_data = response.json()

# Convert response to a string formatted as markdown
response_markdown = response_data['choices'][0]['message']['content'];

# Output to the specified file or print to console
if output_file:
    write_to_markdown(output_file, response_markdown)
    print(f"Response written to {output_file}")
else:
    print(response_markdown)