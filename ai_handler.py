import requests
import logging

# Set up logging
logging.basicConfig(filename='app.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def generate_response_local(email_body, model):
    prompt = f"I have received an email with the following content: \"{email_body}\". How should I draft a response?"

    try:
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

        response_content = response.json()["choices"][0]["message"]["content"]
        return response_content
    except Exception as e:
        logging.error(f'An error occurred: {e}')
        return None
