import json
import email_handler
import oauth2
import ai_handler
import time
import sys
import logging

# Set up logging
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def load_config():
    try:
        with open("settings.json") as config_file:
            config = json.load(config_file)
        return config
    except Exception as e:
        logging.error(f"Error loading config: {e}")
        return None

def main():
    try:
        # Load config
        config = load_config()
        if config is None:
            sys.exit(1)

        # Connect to Gmail
        gmail_service = oauth2.get_gmail_service(config)
        if gmail_service is None:
            sys.exit(1)

        while True:
            try:
                # Get unread emails
                emails = email_handler.get_unread_emails(gmail_service)
                if emails is None:
                    continue

                # Loop through emails and generate drafts
                for email in emails:
                    try:
                        # Extract the email content
                        email_body = email_handler.parse_email_content(gmail_service, email)
                        if email_body is None:
                            continue

                        # Generate a draft response using the local AI
                        draft_response = ai_handler.generate_response_local(email_body, config["ai_model"])
                        if draft_response is None:
                            continue

                        # Create a draft in Gmail
                        email_handler.create_draft(gmail_service, email, draft_response)
                    except Exception as e:
                        logging.error(f"Error processing email: {e}")
            except Exception as e:
                logging.error(f"Error fetching emails: {e}")
            # Sleep for a given period (e.g., 1 hour = 3600 seconds)
            time.sleep(3600)
    except Exception as e:
        logging.error(f"Error in main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
