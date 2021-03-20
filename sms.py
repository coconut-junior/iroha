import os
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import Body, Media, Message, MessagingResponse
import automation
import threading
import json
import random
import logic

app = Flask(__name__)
print('starting twilio sms server...')

@app.route("/sms", methods=['GET', 'POST'])
def reply():
    body = request.values.get('Body', None).lower()
    number = request.values.get('From')
    response = MessagingResponse()
    print(body)

    answer = logic.getAnswer(body, number)
    msg = response.message(answer[0])
    if not answer[1] == '':
        msg.media(answer[1])

    return str(response)

if __name__ == '__main__':
    app.run(debug=True)
    
#lt --port 5000 -s "iroha" 