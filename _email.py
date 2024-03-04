import os
import pandas as pd

from src.email import send_custom_email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv

load_dotenv()

from_email = os.getenv("FROM_EMAIL")

def get_wedding_message(name, email):
    message = MIMEMultipart('related')

    message['from'] = from_email
    message["to"] = email
    message['subject'] = "Wedding Invitation: Samuel and Theodora - July 20th, 2024"
    
    image_path = 'invitation.png'

    html_content = f'''
<!DOCTYPE html>
<html>
<head><title>Wedding Invitation</title></head>
<body style="margin: 40px;">
    <h1 style="margin-left:20px">Samuel and Theodora are Getting Married!</h1>
    
    <div style="display: inline-block; text-align: center;">
        <img src="cid:image1" width="700" style="display: block; margin: 0 auto;">
    </div>
    
    <p style="
        font-family: 'Arial', sans-serif;
        font-size: 16px;
        line-height: 1.6;"
    >
    <i>Dear {name},</i>

    <br>
    <br>
        You are cordially invited to celebrate the eternal union of Samuel Atkins and 
        Theodora Bors in marriage. We look forward to seeing you there!
    <br>
    <br>
    
    <b>
    RSVP: 
    <a href="https://www.zola.com/wedding/samuelandtheodora" target="_blank">\
        https://www.zola.com/wedding/samuelandtheodora
    </a>
    </b>

    </p>

</body>
</html>

    '''
    message.attach(MIMEText(html_content, 'html'))

    with open(image_path, 'rb') as img_file:
        img_data = img_file.read()

    img = MIMEImage(img_data, name=os.path.basename(image_path))
    img.add_header('Content-ID', '<image1>')
    img.add_header('Content-Disposition', 'inline', filename=os.path.basename(image_path))
    message.attach(img)

    return message

if __name__ == "__main__":
    message = get_wedding_message("Samuel & Theodora", "theo.c.bors@gmail.com")

    send_custom_email(message)