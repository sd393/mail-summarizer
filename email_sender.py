import os
import smtplib
from dotenv import load_dotenv

load_dotenv()
email = os.getenv("EMAIL")
app_password = os.getenv("APP_PASSWORD")

smtpObj = smtplib.SMTP("smtp.gmail.com", 587)
smtpObj.ehlo()
print(smtpObj.starttls())

smtpObj.login(email, app_password)

smtpObj.sendmail(email, email, "Subject: testEmail \nHere's a summary sdf sdf of your recent emails!")

smtpObj.quit()