import base64
from email.message import EmailMessage
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError
from googleapiclient.discovery import build


def insert_message_into_inbox(service, user_email, subject, body_text):
    """
    Creates and inserts a new email message into the user's inbox.

    Args:
        service: Authorized Gmail API service instance.
        user_email: The user's email address (for 'To' and 'From').
        subject: The subject line of the email.
        body_text: The plain text content of the email.
    
    Returns:
        The sent message object if successful, otherwise None.
    """
    try:
        # 1. Create the EmailMessage object
        message = EmailMessage()
        message.set_content(body_text)

        # 2. Set the 'To' and 'From' fields to the user's own email
        message["To"] = user_email
        message["From"] = user_email
        message["Subject"] = subject

        # 3. Encode the message in URL-safe base64
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # 4. Create the request body for the API
        create_message_request = {"raw": encoded_message}

        # 5. Call the messages.send API to "insert" the message
        send_message = (
            service.users()
            .messages()
            .send(userId="me", body=create_message_request)
            .execute()
        )
        print(f"Message successfully inserted! Message ID: {send_message['id']}")
        return send_message

    except HttpError as error:
        print(f"An error occurred while inserting the message: {error}")
        return None