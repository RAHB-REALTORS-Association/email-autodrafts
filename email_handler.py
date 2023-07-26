from googleapiclient.errors import HttpError
import base64
import logging
from email.mime.text import MIMEText

# Set up logging
logging.basicConfig(filename='app.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def get_unread_emails(service):
    try:
        # Get the list of drafts
        drafts = service.users().drafts().list(userId='me').execute().get('drafts', [])

        # Extract the thread IDs of the drafts
        draft_thread_ids = [draft['message']['threadId'] for draft in drafts]
        logging.info(f'Draft thread IDs: {draft_thread_ids}')

        # Fetch all unread emails
        results = service.users().messages().list(userId='me', q='is:unread').execute()
        all_unread_emails = results.get('messages', [])
        all_unread_email_ids = [email['threadId'] for email in all_unread_emails]
        logging.info(f'All unread email IDs: {all_unread_email_ids}')

        # Filter out the unread emails that belong to threads with drafts
        filtered_unread_emails = [email for email in all_unread_emails if email['threadId'] not in draft_thread_ids]
        filtered_unread_email_ids = [email['threadId'] for email in filtered_unread_emails]
        logging.info(f'Filtered unread email IDs: {filtered_unread_email_ids}')

        return filtered_unread_emails
    except Exception as e:
        logging.error(f'An error occurred: {e}')
        return None

def parse_email_content(service, email, user_email_address):
    try:
        message = service.users().messages().get(userId='me', id=email['id']).execute()
        payload = message['payload']
        headers = payload.get("headers")
        parts = payload.get("parts")

        data = parts[0]
        data_bytes = data['body']['data']
        decoded_data = base64.urlsafe_b64decode(data_bytes)
        str_data = decoded_data.decode('utf-8')

        # Extract the 'To', 'From', 'Reply-to', 'List-Unsubscribe', and 'Subject' fields from headers
        email_data = {
            'Body': str_data,
            'To': next((header['value'] for header in headers if header['name'] == 'To'), None),
            'From': next((header['value'] for header in headers if header['name'] == 'From'), None),
            'Reply-to': next((header['value'] for header in headers if header['name'] == 'Reply-to'), None),
            'List-Unsubscribe': next((header['value'] for header in headers if header['name'] == 'List-Unsubscribe'), None),
            'Subject': next((header['value'] for header in headers if header['name'] == 'Subject'), None),
            'ThreadId': message['threadId']  # Add the ThreadId
        }

        # Create a copy of the email data for logging, excluding the body
        log_email_data = {k: v for k, v in email_data.items() if k != 'Body'}

        # Skip emails that are not directly addressed to the user
        if user_email_address not in (email_data['To'] or ''):
            logging.info(f"Skipping email not directly addressed to the user. Email data: {log_email_data}")
            return None

        # Skip emails that have a List-Unsubscribe header
        if email_data['List-Unsubscribe']:
            logging.info(f"Skipping email with a List-Unsubscribe header. Email data: {log_email_data}")
            return None

        # Skip emails from or reply-to a noreply or donotreply address
        if any((substring in (email_data.get('From') or '') for substring in ['noreply@', 'no-reply@', 'donotreply@', 'do-not-reply@'])) or \
                any((substring in (email_data.get('Reply-to') or '') for substring in ['noreply@', 'no-reply@', 'donotreply@', 'do-not-reply@'])):
            logging.info(f"Skipping email from or reply-to a noreply or donotreply address. Email data: {log_email_data}")
            return None

        return email_data
    except HttpError as error:
        logging.error(f'An error occurred: {error}')
        return None

def create_draft(service, user_id, draft_response):
    try:
        # Construct an RFC 2822 message
        message = MIMEText(draft_response['Body'])
        message['to'] = draft_response['To']
        message['from'] = draft_response['To']  # Set 'From' as the 'To' field of the original message
        message['subject'] = draft_response['Subject']
        message['In-Reply-To'] = draft_response['ThreadId']
        message['References'] = draft_response['ThreadId']
        raw_message = base64.urlsafe_b64encode(message.as_string().encode('utf-8'))

        # Create the draft
        message_body = {
            'message': {
                'raw': raw_message.decode('utf-8'),
                'threadId': draft_response['ThreadId']  # Add the ThreadId
            }
        }
        draft = service.users().drafts().create(userId=user_id, body=message_body).execute()
        logging.info(f'Draft id: {draft["id"]} created.')
    except HttpError as error:
        logging.error(f'An error occurred: {error}')
