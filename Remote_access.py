from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from pathlib import Path

from string import Template

import smtplib
from email.mime.base import MIMEBase
from email import encoders
import webcam

temp = Template (Path("template.html").read_text ())
subject='Motion Dectector Logs'
message = MIMEMultipart ()
message["From"] = "your_email"
message["To"] = "sender_email"
message["Subject"] = subject

body = temp.substitute ({"Name": "Admin"})
message.attach (MIMEText (body , "html"))
#message.attach (MIMEImage (Path ("Yourimage.JPG").read_bytes ()))
filename='webcam.log'
attachment  =open(filename,'rb')

part = MIMEBase('application','octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition',"attachment; filename= "+filename)

message.attach(part)
text = message.as_string()

with smtplib.SMTP (host="smtp.gmail.com" , port=587) as smtp: 

    print ("Sending Email" ,"To", message["To"],"using",smtp)
    smtp.ehlo ()
    smtp.starttls ()
    smtp.login ("email" , "password")  # dontshare your password
    smtp.send_message (message)
    print("Job Done ")
    smtp.quit()



