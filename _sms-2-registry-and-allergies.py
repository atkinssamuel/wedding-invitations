import pandas as pd
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

    registry_url = "https://www.zola.com/wedding/samuelandtheodora/registry"

    contacted_groups = []
    contacted_numbers = []

    messages = [
        f"""
Hello everyone!

21 days left until the big day! We are so excited to celebrate with all of you.

A few housekeeping items: 

1. For the people inquiring about a registry, we put one together: {registry_url}

2. For the reception guests, we are finalizing the menu this week. If you require special accomodation or have severe \
allergies, please notify us at s.m.atkins73@gmail.com or 604-355-1998.

See you soon, 
Samuel and Theodora
"""
    ]

    for group, contact_options in zip(groups, contacts):
        print(f"Group: {group}, Contacts: {contact_options}")
        success = False
        for contact in contact_options:
            success_count = 0

            for message in messages:
                if send_sms(contact, message, False):
                    success_count += 1

            if success_count == 1:
                success = True

        if success:
            contacted_groups.append(group)
            contacted_numbers.append(contact_options)
        else:
            print(f"FAILED TO CONTACT {group.upper()}")

    pd.DataFrame.from_dict(
        {"contacted_sms": contacted_groups, "numbers": contacted_numbers}
    ).to_csv("contacted_sms.csv", index=False)
