import os
import time
import speech
import json
from twilio.rest import Client

reminders = []
uptime = 0
phone_number = '4843021063'
iroha_number = '+14842095486'

#read write config
def saveConfig():
    global uptime
    global reminders
    try:
        data = {}
        data['owner'] = speech.owner
        data['name'] = speech.name
        data['uptime'] = uptime
        data['reminders'] = reminders
        with open(os.getenv("HOME") + '/iroha-config.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
    except:
        print('failed to write config file')

def loadConfig():
    global uptime
    global reminders
    try:
        with open (os.getenv("HOME") + '/iroha-config.json') as json_file:
            data = json.load(json_file)
            speech.owner = data['owner']
            speech.name = data['name']
            uptime = data['uptime']
            reminders = data['reminders']
    except:
        print('no config found, creating one...')
        saveConfig()

def createReminder(title, time_date):
    print('setting reminder for ' + title + 'at ' + time_date + '...')

def sendSMS(message):
    global phone_number
    global iroha_number
    account_sid = 'AC7593ac316047b1a511e6068ec1e7623b'
    auth_token = 'ebe667fb960cc7228f8cfb5f99d32603'
    client = Client(account_sid, auth_token)

    client.messages.create(
        to = phone_number,
        from_ = iroha_number,
        body = message
    )