import os
import time
import speech
import json
from twilio.rest import Client
import stamps
import requests

reminders = []
uptime = 0
iroha_number = '+14842095486'
phone_number = '+14843021063'
username = 'iroha.bot.official@gmail.com' #replace asap to avoid leaking credentials
password = 'scjldizwkyjodvhz'

phonebook = {}
phonebook['+14843928694'] = 'John'
phonebook['+14843021063'] = 'Jimmy'

def execute(task):
    if task == 'laugh':
        print('hahahahahahahaHAHAHAH')

#read write config
def saveConfig():
    global uptime
    global reminders
    global phone_number
    try:
        data = {}
        data['owner'] = speech.owner
        data['name'] = speech.name
        data['uptime'] = uptime
        data['reminders'] = reminders
        data['phone_number'] = phone_number
        with open(os.getenv("HOME") + '/iroha-config.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
    except:
        print('failed to write config file')

def loadConfig():
    global uptime
    global reminders
    global phone_number
    try:
        with open (os.getenv("HOME") + '/iroha-config.json') as json_file:
            data = json.load(json_file)
            speech.owner = data['owner']
            speech.name = data['name']
            uptime = data['uptime']
            reminders = data['reminders']
            phone_number = data['phone_number']
    except:
        print('no config found, creating one...')
        saveConfig()

def createReminder(title, time_date):
    print('setting reminder for ' + title + 'at ' + time_date + '...')

def sendSMS(message, number):
    global iroha_number
    account_sid = 'AC7593ac316047b1a511e6068ec1e7623b'
    auth_token = 'ebe667fb960cc7228f8cfb5f99d32603'
    client = Client(account_sid, auth_token)

    client.messages.create(
        to = number,
        from_ = iroha_number,
        body = message
    )

def getAnswer(text, number):
    global phonebook
    answer = ''
    img = ''
    name = phonebook[number]

    if text == 'can you see this?':
        answer = 'Yes i can! 😁'
    elif text == 'coming home' or text == 'on my way!':
        answer = 'See u soon 😘'
    elif text == 'i love you':
        img = stamps.love
    elif text == "what are u up to?":
        answer = 'not much hbu ' + name + '?'
    else:
        answer = 'Hmmm'

    print("sending '" + answer + "' to " + name)
    return [answer, img]
