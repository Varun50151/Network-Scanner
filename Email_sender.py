import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
def send_email(email_id,subject="Scanning Report", message=None):
    server=smtplib.SMTP("smtp.gmail.com",587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    with open ("password.txt","r") as f:
        password=f.read().strip()

    server.login("businesscategory27@gmail.com",password)
    msg=MIMEMultipart()
    msg["From"]="Anonymous"
    msg["To"]=email_id
    msg["Subject"]=subject
    if message is None:
        with open("message.txt", "r") as f:
            message=f.read()
    msg.attach(MIMEText(message, "plain"))        

    server.sendmail("businesscategory27@gmail.com",email_id,msg.as_string())
    server.quit()
    print(f"Email sent to {email_id}")
