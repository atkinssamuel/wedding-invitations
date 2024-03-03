import requests
import math
import re
import os

import pandas as pd
import numpy as np

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
    )
    if verbose:
        print(resp.json())
