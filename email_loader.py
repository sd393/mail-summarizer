import imapclient, os
from datetime import date
import pprint

from dotenv import load_dotenv

load_dotenv()

email = os.getenv("EMAIL")
app_password = os.getenv("APP_PASSWORD")

imapObj = imapclient.IMAPClient('imap.gmail.com', ssl = True)
imapObj.login(email, app_password)

#pprint.pprint(imapObj.list_folders())
imapObj.select_folder("INBOX", readonly=True)

UIDs = imapObj.search([u'SINCE', date(2025, 8, 1), "UNSEEN"])
print(UIDs)
