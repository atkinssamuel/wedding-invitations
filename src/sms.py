import requests
import os

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("SMS_KEY")

def send_sms(recipient: str, message: str, verbose: bool = False):
    if verbose:
        print(f"Sending message to {recipient}.")
        print(f"Message content: \"{message}\"")
    
    resp = requests.post(
        "https://textbelt.com/text",
        {
            "phone": recipient,
            "message": message,
            "key": api_key,
        },
    ).json()
    if verbose:
        print(resp)

    return resp["success"]