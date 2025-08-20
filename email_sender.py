import os
import smtplib
from dotenv import load_dotenv
import markdown
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()
email = os.getenv("EMAIL")
app_password = os.getenv("APP_PASSWORD")

def send_email(message):
    #Define message container
    message_container = MIMEMultipart('alternative')
    message_container['Subject'] = "Your email summary for this week"
    message_container["From"] = email
    message_container["To"] = email 

    #Create text part of message
    text_part = MIMEText(message, 'text')

    #Create HTML part of message
    html_output = markdown.markdown(message)
    html_part = MIMEText(html_output, 'html')

    #Attach to container
    message_container.attach(text_part)
    message_container.attach(html_part)

    #Start server
    smtpObj = smtplib.SMTP("smtp.gmail.com", 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(email, app_password)

    #Send email
    smtpObj.sendmail(email, email, message_container.as_string())

    #Quit connection
    smtpObj.quit()

if __name__ == "__main__":
    pass
    

    