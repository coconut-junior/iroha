import os
import time
import speech
import json
from twilio.rest import Client
import requests
import random

reminders = []
uptime = 0
iroha_number = '+14842095486'
phone_number = '+14843021063'
username = 'iroha.bot.official@gmail.com' #replace asap to avoid leaking credentials
password = 'scjldizwkyjodvhz'

morning_hr = 9
morning_min = random.randint(0,15)
morning_greetings = ['Good morning ' + speech.owner + ' did u sleep well?', 
'Sleep well, ' + speech.owner + '?', 'Rise and shine ' + speech.owner + ' ☺️']

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


