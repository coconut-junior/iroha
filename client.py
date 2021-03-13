import imaplib
import email
import automation
import time

host = 'imap.gmail.com'

def get_inbox():
    task = None
    mail = imaplib.IMAP4_SSL(host)
    mail.login(automation.username, automation.password)
    mail.select("inbox")
    _, search_data = mail.search(None, 'UNSEEN')
    my_message = []
    for num in search_data[0].split():
        email_data = {}
        _, data = mail.fetch(num, '(RFC822)')
        # print(data[0])
        _, b = data[0]
        email_message = email.message_from_bytes(b)

        subject = email_message['subject']
        if subject.startswith(automation.phone_number):
            cmd = subject.split(':')
            task = cmd[1]

        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                email_data['body'] = body.decode()
            elif part.get_content_type() == "text/html":
                html_body = part.get_payload(decode=True)
                email_data['html_body'] = html_body.decode()
        my_message.append(email_data)
    return task

# print(search_data)