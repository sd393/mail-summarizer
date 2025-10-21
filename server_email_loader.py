import os
import json
import base64
from email.message import EmailMessage
from dotenv import load_dotenv  # <-- IMPORT THIS

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Define scopes (must match server.js)
SCOPES = [
        'https://www.googleapis.com/auth/gmail.insert',
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/userinfo.email', 
        'https://www.googleapis.com/auth/gmail.send'
]

TOKEN_DICT_FILE = "token.json"

def get_emails(email_index):
    """
    Loads credentials from the token.json dictionary,
    then reads and sends an email.
    """
    
    # --- NEW: Load .env file from the root folder ---
    load_dotenv() 

    # --- 1. Load Credentials from our Dictionary ---
    
        # Load the dictionary of all tokens (as you already do)
    with open(TOKEN_DICT_FILE, "r") as token_file:
        all_tokens = json.load(token_file)

    # Check if the dictionary is empty first!
    if not all_tokens:
        print(f"Error: {TOKEN_DICT_FILE} is empty.")
        print("Please log in through the website first.")
        return

    # Get the first key from the dictionary
    USER_EMAIL_TO_USE = list(all_tokens.keys())[email_index]
    print(f"Using credentials for user: {USER_EMAIL_TO_USE}")

    # Now, get the token info for that user
    user_token_info = all_tokens.get(USER_EMAIL_TO_USE)
    
    creds = None
    all_tokens = {}
    
    try:
        with open(TOKEN_DICT_FILE, "r") as token_file:
            all_tokens = json.load(token_file)

        user_token_info = all_tokens.get(USER_EMAIL_TO_USE)
        
        if not user_token_info:
            print(f"Error: Email {USER_EMAIL_TO_USE} not found in {TOKEN_DICT_FILE}")
            print("Please log in through the website first.")
            return

        creds = Credentials.from_authorized_user_info(user_token_info, SCOPES)
    
    except FileNotFoundError:
        print(f"Error: {TOKEN_DICT_FILE} not found.")
        print("Please log in through the website first to create it.")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode {TOKEN_DICT_FILE}. It may be corrupt.")
        return

    try:
        # --- 2. Check if Token Needs Refreshing ---
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("Credentials expired, refreshing...")
                
                # --- MODIFIED BLOCK ---
                # Get client ID and secret from environment variables
                '''
                client_id = os.getenv("CLIENT_ID")
                client_secret = os.getenv("CLIENT_SECRET")
                
                if not client_id or not client_secret:
                    print("Error: GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET not found in .env")
                    return

                creds.client_id = client_id
                creds.client_secret = client_secret '''
                # --- END MODIFIED BLOCK ---
                
                creds.refresh(Request())
                
                all_tokens[USER_EMAIL_TO_USE] = json.loads(creds.to_json())
                with open(TOKEN_DICT_FILE, 'w') as token_file:
                    json.dump(all_tokens, token_file, indent=2)
                print("Token refreshed and saved.")
            else:
                print("Cannot refresh. Please re-authenticate via the website.")
                return

        # --- 3. Build the Gmail Service ---
        service = build("gmail", "v1", credentials=creds)

        # ... (rest of the code for reading/sending email is the same) ...
        # (You can copy/paste it from the previous answer)
        # --- 4. How to Read Emails (Inbox, last 1 day, ALL pages) ---
        print("\n--- Reading Emails (Inbox, last 1 day) ---")

        all_messages = []
        page_token = None
        final_message_summary = ""

        try:
            while True:
                # Make the API call, including the page token if we have one
                results = service.users().messages().list(
                    userId="me",
                    labelIds=["INBOX"],
                    q="newer_than:1d",
                    pageToken=page_token  # For getting the next page
                ).execute()

                messages = results.get("messages", [])
                all_messages.extend(messages)  # Add messages from this page to our full list

                # Check if there's another page of results
                page_token = results.get("nextPageToken")
                if not page_token:
                    break  # No more pages, exit the loop

            if not all_messages:
                print("No messages found in the last 1 day.")
            else:
                print(f"Found {len(all_messages)} total messages from the last 1 day:")
                # Now loop through the full list of messages
                for msg in all_messages:
                    final_message_summary += "Email:\n"
                    # Get the full message details
                    msg_data = service.users().messages().get(
                        userId="me", id=msg["id"]
                    ).execute()
                    
                    # Find the 'Subject' header
                    subject = ""
                    for header in msg_data['payload']['headers']:
                        if header['name'] == 'Subject':
                            subject = header['value']
                            break

                    # Get the body
                    body = get_email_body(msg_data['payload'])

                    final_message_summary += "Subject: " + subject + "\n"
                    final_message_summary += "Body: " + body + "\n"


                    print(f"- Subject: {subject} (ID: {msg['id']})")

        except HttpError as error:
            print(f"An error occurred: {error}")

    except RefreshError as e:
        print(f"Error refreshing token: {e}")
        print("This can happen if the user revoked permission.")
        print("Please delete token.json and log in again via the website.")
    except HttpError as error:
        print(f"An error occurred: {error}")
    
    print(all_messages)
    return USER_EMAIL_TO_USE, service, final_message_summary

import base64 # Make sure this is at the top of gmail_service.py

def get_email_body(payload):
    """
    Recursively search for the plain text part of an email's payload.
    
    Args:
        payload: The payload dictionary from a Gmail message object.
        
    Returns:
        The decoded email body as a string, or an empty string if not found.
    """
    # Check if the payload has 'parts'
    if 'parts' in payload:
        for part in payload['parts']:
            # If the part has a mimeType of text/plain, we found our body
            if part['mimeType'] == 'text/plain':
                # The body data is base64 encoded
                data = part['body'].get('data')
                if data:
                    return base64.urlsafe_b64decode(data).decode('utf-8')
            # If the part is multipart, search its parts recursively
            elif 'parts' in part:
                body = get_email_body(part)
                if body:
                    return body
    # If there are no parts, the body might be in the main payload
    elif 'body' in payload:
        data = payload['body'].get('data')
        if data:
            return base64.urlsafe_b64decode(data).decode('utf-8')
            
    # If no plain text body is found
    return ""

if __name__ == "__main__":
    main()