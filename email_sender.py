import os
import smtplib
from dotenv import load_dotenv

load_dotenv()
email = os.getenv("EMAIL")
app_password = os.getenv("APP_PASSWORD")

def send_email(message):
    message = message.encode("utf-8")
    message = message.decode("utf-8")
    smtpObj = smtplib.SMTP("smtp.gmail.com", 587)
    smtpObj.ehlo()
    smtpObj.starttls()

    smtpObj.login(email, app_password)

    smtpObj.sendmail(email, email, "Subject: This Week's Inbox Summary \n" + message)

    smtpObj.quit()
if __name__ == "__main__":
    #send_email("hello \n sdf *")
    pass
    

    