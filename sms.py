import os
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import Body, Media, Message, MessagingResponse
import automation

app = Flask(__name__)
print('starting twilio sms server...')

@app.route("/sms", methods=['GET', 'POST'])
def reply():
    body = request.values.get('Body', None).lower()
    response = MessagingResponse()
    print(body)

    answer = automation.getAnswer(body)
    msg = response.message(answer[0])
    if not answer[1] == '':
        msg.media(answer[1])

    return str(response)

if __name__ == '__main__':
    app.run(debug=True)

#ngrok http 5000 to start server
#webhook http://d74445561bcb.ngrok.io/sms