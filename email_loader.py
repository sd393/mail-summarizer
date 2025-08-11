import imapclient, imaplib, os, pprint, pyzmail
from datetime import date
from dotenv import load_dotenv

load_dotenv()
email = os.getenv("EMAIL")
app_password = os.getenv("APP_PASSWORD")

def get_recent_emails():
        imaplib._MAXLINE = 10000000

        imapObj = imapclient.IMAPClient('imap.gmail.com', ssl = True)
        imapObj.login(email, app_password)

        imapObj.select_folder("INBOX", readonly=True)

        UIDs = imapObj.search([u'SINCE', date(2025, 8, 11), "UNSEEN"])
        #print(UIDs)

        raw_messages = imapObj.fetch(UIDs, ['BODY[]'])
        #pprint.pprint(raw_messages[23868])
        #print(raw_messages[23868][b"BODY"])



        messages = []
        for i in range(len(UIDs)):

            total_message_info = pyzmail.PyzMessage.factory(raw_messages[UIDs[i]][b'BODY[]'])

            email_info = []
            email_info.append(total_message_info.get_subject())
            email_info.append("")

            if (total_message_info.text_part != None):
                email_info[1] += total_message_info.text_part.get_payload().decode("utf-8")
            
            if (total_message_info.html_part != None):
                email_info[1] += total_message_info.html_part.get_payload().decode(total_message_info.html_part.charset)
            
            messages.append(email_info)

        imapObj.logout()

        return messages

def format_email_info():
    message = ""

    email_list = get_recent_emails()
    for email in email_list:
        message += "EMAIL:\n"
        message += "SUBJECT: " + email[0] + "\n"
        message += "BODY: " + email[1] + "\n"
        message += "END OF EMAIL\n"

    return message

if __name__ == "__main__":
    
    """ 
    print(messages[0].get_subject())
    print(messages[0].text_part != None)
    print(messages[0].text_part.get_payload().decode("utf-8"))
    print(messages[0].html_part.get_payload().decode(messages[0].html_part.charset))
    """

    #print(format_email_info())