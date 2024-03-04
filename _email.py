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
<body>
    <img 
        src="cid:image1" 
        style="
            display: block;
            margin: 0 auto;
            width: 50%;
            border: 2px solid grey;
            margin-bottom: 20px;
        "
    />
    
    <p
      style="
        font-family: 'Arial', sans-serif;
        font-size: 20px;
        line-height: 1.6;
        display: block;
        margin: 0 auto;
        width: 90%;
      "
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
    <a href="https://www.zola.com/wedding/samuelandtheodora" target="_blank">
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
    guest_df = pd.read_csv("guests.csv")

    contacted_groups = []

    for i in range(guest_df.shape[0]):
        guest = guest_df.iloc[i]
        
        if not pd.isna(guest.group) and not pd.isna(guest.email):
            print(f"Group: {guest.group}, Recipient Email: {guest.email}")
            message = get_wedding_message(guest.group, guest.email)
            if send_custom_email(message):
                contacted_groups.append(guest.group)
            else:
                print(f"FAILED TO CONTACT {guest.group.upper()}")

    
    pd.DataFrame.from_dict({"contacted_email": contacted_groups}).to_csv("contacted_email.csv", index=False)
        