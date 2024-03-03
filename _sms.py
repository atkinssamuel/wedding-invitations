import pandas as pd
import re

from src.sms import send_sms


guest_df = pd.read_csv("guests.csv")

groups = []
contacts = []


for i in range(guest_df.shape[0]):
    person = guest_df.iloc[i]
    if not person.group:
        continue

    numbers = [
        re.sub("-", "", val)
        for val in [person.phone_1, person.phone_2, person.phone_3]
        if not pd.isna(val)
    ]
    if len(numbers) == 0:
        continue

    groups.append(person.group)
    contacts.append(numbers)

url = "https://www.zola.com/wedding/samuelandtheodora"

for group, contact_options in zip(groups, contacts):
    message = (
        f"Dear {group}, you are cordially invited to celebrate the marriage of Samuel Atkins and Theodora Bors."
    )
    messages = ["Welcome to Samuel & Theodora's Wedding Alerts!", message, url]

    for contact in contact_options:
        print(f'\nContact: {contact}\nMessages: "{messages}"')
        # send_sms(contact, message, True)

message = (
    f"Dear Samuel & Theodora, you are cordially invited to celebrate the marriage of Samuel Atkins and Theodora Bors.",
)
messages = ["Welcome to Samuel & Theodora's Wedding Alerts!", message, url]

for message in messages:
    send_sms("6047198954", message, True)
    send_sms("6043551998", message, True)
