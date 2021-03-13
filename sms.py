import os
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import Body, Media, Message, MessagingResponse
import automation
import threading
import json

app = Flask(__name__)
print('starting twilio sms server...')

def sendCmd(cmd, number):
    import smtplib
    from email.mime.text import MIMEText

    smtp_ssl_host = 'smtp.gmail.com'
    smtp_ssl_port = 465
    sender = automation.username
    targets = [automation.username]

    msg = MIMEText('')
    msg['Subject'] = number + ':' + cmd
    msg['From'] = sender
    msg['To'] = ', '.join(targets)

    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    server.login(automation.username, automation.password)
    server.sendmail(sender, targets, msg.as_string())
    server.quit()

@app.route("/sms", methods=['GET', 'POST'])
def reply():
    body = request.values.get('Body', None).lower()
    number = request.values.get('From')
    response = MessagingResponse()
    print(body)

    if 'laugh' in body:
        sendCmd('laugh', number)

    answer = automation.getAnswer(body, number)
    msg = response.message(answer[0])
    if not answer[1] == '':
        msg.media(answer[1])

    return str(response)

if __name__ == '__main__':
    app.run(debug=True)
    
#lt --port 5000 -s "iroha" 