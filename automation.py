import os
import time
import speech
import json
from twilio.rest import Client
import requests
import random
import datetime
from datetime import date
from calendar import isleap

reminders = []
uptime = 0
iroha_number = '+14842095486'
iroha_birthday = '2021-03-12 21:04:01.326550'
phone_number = '+14843021063'
username = 'iroha.bot.official@gmail.com' #replace asap to avoid leaking credentials
password = 'scjldizwkyjodvhz'

morning_hr = 10
morning_min = random.randint(0,30)
morning_greetings = ['Good morning ' + speech.owner + ' did u sleep well?', 
'Sleep well, ' + speech.owner + '?', 'Rise and shine ' + speech.owner + ' ☺️']

def execute(task):
    if task == 'laugh':
        print('hahahahahahahaHAHAHAH')
    elif task.startswith('remind:'):
        args = task.split(':')
        createReminder(args[1])

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

def add_years(d, years):
    new_year = d.year + years
    try:
        return d.replace(year=new_year)
    except ValueError:
        if (d.month == 2 and d.day == 29 and # leap day
            isleap(d.year) and not isleap(new_year)):
            return d.replace(year=new_year, day=28)
        raise

def createReminder(text):
    print('setting reminder...')

    text=text.replace('please', "")
    text=text.replace('reminder', "")
    text=text.replace('remind', "")
    text=text.replace('can you', "")
    text=text.replace(' to ', " ")
    text=text.replace(' me ', " ")
    text=text.replace(' in ', " ")
    text=text.replace(' at ', " ")
    text=text.replace(' my ', ' your ')
    text=text.replace(' a ', ' ')
    text=text.replace('next','')
    text=text.replace('from now', '')

    #remove double spaces
    text=text.replace('  ', ' ')

    times = ['am','pm','oclock']
    am_pm = 'AM'
    hr = 0
    mn = 0
    target_date = datetime.date.today()
    msg = ''

    for t in times:
        try:

            if t in text:
                if t == 'pm':
                    am_pm = 'PM'
                    text=text.replace('pm','')
                elif t == 'am':
                    text=text.replace('am','')

                #remove non-numbers
                numbers = [':','0','1','2','3','4','5','6','7','8','9']
                for c in text:
                    if not c in numbers:
                        text=text.replace(c,'')
                        msg += c

                print(msg)

                args = text.split(t)

                if ':' in text:
                    exact_time = args[0].split(':')
                    hr = int(exact_time[0])
                    mn = int(exact_time[1])
                else:
                    hr = int(args[0])
                    mn = 0

                print(str(hr) + ':' + str(mn) + am_pm)
                #convert to 24hr
                if am_pm == 'PM':
                    hr += 12

        except Exception as e:
            print(e)
            pass

    #push time to specific day
    try:
        if 'today' in msg:
            msg = msg.replace('today', '')
        elif 'tomorrow' in msg:
            msg=msg.replace('tomorrow','')
            target_date = datetime.date.today() + datetime.timedelta(days=1)
        elif 'week' in msg and not 'weeks' in msg:
            msg=msg.replace('week','')
            target_date = datetime.date.today() + datetime.timedelta(weeks=1)
        elif 'month' in msg and not 'months' in msg:
            msg=msg.replace('month','')
            target_date = datetime.date.today() + datetime.timedelta(months=1)
        elif 'year' in msg and not 'years' in msg:
            msg=msg.replace('year','')
            target_date = add_years(datetime.date.today(), 1)
    except:
        print('could not figure out exact date')

    if not hr == 0:
        msg = msg.strip()
        print('reminder set for ' + str(target_date) + ' at ' + str(hr)+':'+str(mn))
        reminders.append(str(target_date) + ':' + msg)

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


