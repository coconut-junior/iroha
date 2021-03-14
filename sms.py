import os
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import Body, Media, Message, MessagingResponse
import automation
import threading
import json
import stamps
import random

app = Flask(__name__)
print('starting twilio sms server...')

#this will later be pulled from database
phonebook = {}
phonebook['+14843928694'] = 'John'
phonebook['+14843021063'] = 'Jimmy'

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

def getAnswer(text, number):
    global phonebook
    answer = ''
    answers = ['']
    img = ''
    name = phonebook[number]

    #remove apostraphes
    text.replace("'", '')
    #correct texting lingo
    text.replace(' u ', ' you ')
    text.replace(' dat ', ' that ')

    if text.startswith('can you see this'):
        answers = ['Yes i can! 😁', "Well, I can't SEE exactly..."]
    elif text.startswith('hi') or text.startswith('hello') or text.startswith('hey'):
        answers = ['Heyyy', "Hey " + name, "What's up? 😊"]
    elif text.startswith('what is '):
        #look up answer thru api
        answers = ["I'm not sure yet"]
    elif text == 'coming home' or text == 'on my way!':
        answers = ['See u soon 😘']
    elif 'love you' in text or 'love u' in text:
        img = stamps.love
    elif text == "what are u up to?" or ("whats up" in text):
        answers = ['Not much hbu ' + name + '?']
    elif 'laugh' in text:
        sendCmd('laugh', number)
    elif ("im" in text or 'i am' in text) and not 'not' in text and 'happy' in text:
        answer = ''
    elif ("im" in text or 'i am' in text) and not 'not' in text and 'tired' in text:
        answers = ['Ok, goodnight! ❤️', 'Go to bed then silly', 'Goodnight, sleepyhead!']
    else:
        #generic answers
        answers = ['Hmmm', 'Huh']

    answer = answers[random.randint(0,len(answers)-1)]
    print("sending '" + answer + "' to " + name)
    return [answer, img]

@app.route("/sms", methods=['GET', 'POST'])
def reply():
    body = request.values.get('Body', None).lower()
    number = request.values.get('From')
    response = MessagingResponse()
    print(body)

    answer = getAnswer(body, number)
    msg = response.message(answer[0])
    if not answer[1] == '':
        msg.media(answer[1])

    return str(response)

if __name__ == '__main__':
    app.run(debug=True)
    
#lt --port 5000 -s "iroha" 