from server_email_loader import get_emails
from server_email_sender import insert_message_into_inbox
from summarizer import get_summary

def main():
    """
    Main function to run the email summarizer tasks.
    """
    # 1. Get the authenticated Gmail service and user email
    # All the complex authentication logic is now hidden in this one function call.
    user_email, service, raw_body = get_emails(1)

    # If authentication fails, service will be None.
    if not service:
        print("Could not connect to Gmail. Exiting.")
        return

    # 3. Insert a summary message into the user's inbox
    print("\n--- Inserting a summary message ---")
    
    email_subject = "Your Daily Summary is Ready"
    email_body = get_summary(raw_body)
    
    insert_message_into_inbox(service, user_email, email_subject, email_body)


# This makes the script runnable from the command line
if __name__ == "__main__":
    main()
