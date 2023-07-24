import requests
import os
import openai
import logging

# Set up logging
logging.basicConfig(filename='app.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def generate_response(email_body, model, max_tokens, prompt_template):
    prompt = prompt_template.format(email_body=email_body)

    try:
        if os.getenv('USE_LOCAL', 'false').lower() == 'true':
            # Send a POST request to the local server
            response = requests.post(
                "http://localhost:1234/v1/chat/completions",
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant that composes professional and appropriate responses to emails."},
                        {"role": "user", "content": prompt}
                    ]
                }
            )
        else:
            # Use OpenAI API
            openai.api_key = os.getenv('OPENAI_API_KEY')
            response = openai.Completion.create(
              engine=model,
              prompt=prompt,
              max_tokens=max_tokens
            )

        # Extract the generated response
        response_content = response.json()["choices"][0]["message"]["content"]
        return response_content
    except Exception as e:
        logging.error(f'An error occurred: {e}')
        return None
