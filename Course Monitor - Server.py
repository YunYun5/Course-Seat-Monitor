from bs4 import BeautifulSoup
import requests
import time
import smtplib
import config

classes = {"Data Science 100 (Python)": "https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-section&dept=DSCI&course=100&section=100", 
           "Data Science 010 (MF)": "https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-section&dept=DSCI&course=100&section=010",
           "CPSC LAB L2Q (Wednesday)": "https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-section&dept=CPSC&course=210&section=L2Q",
           "CPSC LAB L2B (Tuesday Early)": "https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-section&dept=CPSC&course=210&section=L2B",
           "CPSC LAB L2N (Tuesday Late)": "https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-section&dept=CPSC&course=210&section=L2N",
           "CPSC LAB L2S (Monday)": "https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-section&dept=CPSC&course=210&section=L2S",
           "test": "https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-section&dept=ARCL&course=103&section=002"}

# Email credentials
email_user = config.email_user
email_password = config.email_password

# Carrier's email to SMS gateway domain
carrier_gateway = config.carrier_gateway

# Recipient's phone number
to_number = config.to_number

# Tracking whether a message has been sent for each class
message_sent = {class_name: False for class_name in classes}

def check_seat(classes):
    for key, value in classes.items():
        try:
            response = requests.get(value)
            time.sleep(5)  # wait for the page to load

            soup = BeautifulSoup(response.text, 'html.parser')

            text = soup.find_all('table', "'table")

            if not text:
                print(f"No table found for {key}. Skipping.")
                continue

            text_full = text[0].text
            text = text_full.split("\n")[4]
            count = int(text.split(":")[1])

            if count > 0 and not message_sent[key]:
                send_message(f"{key} has open seats")
                message_sent[key] = True
                print(f"{key} has open {count} seats")
            elif count == 0:
                message_sent[key] = False
                print(f"{key} does not have open seats")

        except Exception as e:
            print(f"An error occurred for {key}: {e}")

def send_message(message):
    # Setting up the SMTP server
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(email_user, email_password)

        # Creating the message
        formated_message = 'Subject: {}\n\n{}'.format('Seat Open', message)

        # Sending the email
        server.sendmail(email_user, f'{to_number}@{carrier_gateway}', formated_message)

while True:
    check_seat(classes)
    print("Completed Class Search")
    time.sleep(300)
        