import pandas as pd
import numpy as np
import re

from src.sms import send_sms


if __name__ == "__main__":
    guest_df = pd.read_csv("remaining.csv")

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

    contacted_groups = []
    contacted_numbers = []

    for group, contact_options in zip(groups, contacts):
        message = (
            f"Dear {group},\n\nYou are cordially invited to celebrate the marriage of Samuel Atkins and Theodora Bors."
        )
        messages = ["Welcome to Samuel & Theodora's Wedding Alert System!", message, f"RSVP: {url}"]

        print(f'Group: {group}, Contacts: {contact_options}')
        success = False
        for contact in contact_options:
            success_count = 0

            for message in messages:
                if send_sms(contact, message, False):
                    success_count += 1
            
            if success_count == 3:
                success = True

        if success:
            contacted_groups.append(group)
            contacted_numbers.append(contact_options)
        else:
            print(f"FAILED TO CONTACT {group.upper()}")

    pd.DataFrame.from_dict({"contacted_sms": contacted_groups, "numbers": contacted_numbers}).to_csv("contacted_sms.csv", index=False)
