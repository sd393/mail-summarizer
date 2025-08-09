import imapclient, imaplib, os, pprint, pyzmail
from datetime import date
from dotenv import load_dotenv

load_dotenv()
email = os.getenv("EMAIL")
app_password = os.getenv("APP_PASSWORD")

imaplib._MAXLINE = 10000000

imapObj = imapclient.IMAPClient('imap.gmail.com', ssl = True)
imapObj.login(email, app_password)

imapObj.select_folder("INBOX", readonly=True)

UIDs = imapObj.search([u'SINCE', date(2025, 8, 8), "UNSEEN"])
#print(UIDs)

raw_messages = imapObj.fetch(UIDs, ['BODY[]'])
#pprint.pprint(raw_messages[23868])
#print(raw_messages[23868][b"BODY"])


messages = []
for i in range(2):
    messages.append(pyzmail.PyzMessage.factory(raw_messages[23868+i][b'BODY[]']))

print(messages[0].get_subject())
print(messages[0].text_part != None)
print(messages[0].text_part.get_payload().decode("utf-8"))
