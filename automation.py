import os
import time
import json
from twilio.rest import Client
import requests
import random
import datetime
from datetime import date
from calendar import isleap
import subprocess
import re

reminders = []
uptime = 0
iroha_number = '+14842095486'
iroha_birthday = '2021-03-12 21:04:01.326550'
phone_number = '+14843021063'
username = 'iroha.bot.official@gmail.com' #replace asap to avoid leaking credentials
password = 'scjldizwkyjodvhz'

phrases = {"we":"the two of us", "sleep":"rest", "good":"great","nice":"awesome","promise":"swear"}

def morningMessage():
    messages = ["Good morning name did you sleep well?", "Morning! Did you have any dreams about me?","Morninggg","Good morning name. Hope you slept well!","Morningg are you awake yet? 🥺","Good morning! When do I get to see your cute face again?","Good morning handsome! Did you sleep well? Or were you too busy dreaming about me… 😉","Morning! How’d you sleeeeep?","Good morning name. You’re going to kill it today, I believe in you! XO 💛" ]
    msg = messages[random.randint(0,len(messages)-1)]
    return msg.lower()

def nightMessage():
    messages = ["In a perfect world, every night would begin with a cuddle with you and every day would begin with a kiss from you. Good night name.","Goodnight name. I don’t know what I’d do without you – you mean everything to me.","Wishing you a good night is pointless because I know that neither of us is going to be happy being away from each other. Xoxo"]
    msg = messages[random.randint(0,len(messages)-1)]

    return msg.lower()

def rephrase(text):
    sentence = text.split(' ')
    new_text = ''
    for i in range(len(sentence)):
        w = sentence[i]
        if random.randint(0,2) == 1 and w in phrases:
            sentence[i] = phrases[w]
        new_text += sentence[i] + ' '
    
    return new_text.strip()


def getUptime():
    global uptime
    if uptime < 60:
        return "less than a minute"
    elif uptime == 60:
        return "about a minute"
    elif uptime > 60 and uptime < 3600:
        return str(uptime/60) + " minutes"
    else:
        return str(uptime/60/60) + " hours"

def execute(task):
    if task == 'laugh':
        print('hahahahahahahaHAHAHAH')
    elif task.startswith('remind:'):
        args = task.split(':')
        createReminder(args[1])

def add_years(d, years):
    new_year = d.year + years
    try:
        return d.replace(year=new_year)
    except ValueError:
        if (d.month == 2 and d.day == 29 and # leap day
            isleap(d.year) and not isleap(new_year)):
            return d.replace(year=new_year, day=28)
        raise

def createReminder(text, channel):
    numbers = [':','0','1','2','3','4','5','6','7','8','9']
    print('setting reminder...')
    if 'to' in text:
        text = text[text.index('to')+3:len(text)]

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

    if 'minutes' in text or 'minute' in text:
        offset = int(re.sub("[^0-9]", "", text))
        new_time = (datetime.datetime.now() + datetime.timedelta(minutes = offset))
        text = text.replace(str(offset), datetime.datetime.strftime(new_time, "%I:%M%p").lower()).replace('minutes','').replace('minute','')
    elif 'hours' in text or 'hour' in text:
        offset = int(re.sub("[^0-9]", "", text))
        new_time = (datetime.datetime.now() + datetime.timedelta(hours = offset))
        text = text.replace(str(offset), datetime.datetime.strftime(new_time, "%I:%M%p").lower()).replace('hours','').replace('hour','')


    #if am/pm not specified decide which
    if not 'am' in text and not 'pm' in text:
        i = 0
        for c in range(len(text)):
            if text[c] in numbers:
                i = c

        if 'morning' in text:
            text = text.replace('morning','')
            text = text[:i] + 'am' + text[i:]
        elif 'night' in text or 'evening' in text:
            text = text.replace('night', '')
            text = text.replace('evening', '')
            text = text[:i] + 'pm' + text[i:]
        else:
            text = text[:i] + 'pm' + text[i:]

    for t in times:
        try:

            if t in text:
                if t == 'pm':
                    am_pm = 'PM'
                    text=text.replace('pm','')
                elif t == 'am':
                    text=text.replace('am','')
                
                #remove non-numbers
                for c in text:
                    if not c in numbers:
                        text=text.replace(c,'')
                        msg += c

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
        if 'my' in msg:
            msg = msg.replace('my','your')
        else:
            msg = msg.replace('your', 'my')
        print('reminder set for ' + str(target_date) + ' at ' + str(hr)+':'+str(mn))

        r = {}
        r['date'] = str(target_date)
        r['time'] = [hr,mn]
        r['message'] = msg.replace('my','your')
        r['channel'] = channel
        reminders.append(r)
        print(reminders)

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


