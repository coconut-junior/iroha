import os
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import Body, Media, Message, MessagingResponse

app = Flask(__name__)
print('starting twilio sms server...')

@app.route("/sms", methods=['GET', 'POST'])
def reply():
    body = request.values.get('Body', None)
    response = MessagingResponse()
    print(body)

    if (body == 'Can you see this?'):
        response.message('yes i can! 😁')
        
    return str(response)

if __name__ == '__main__':
    app.run(debug=True)

#webhook http://d74445561bcb.ngrok.io/sms