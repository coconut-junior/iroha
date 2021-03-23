# -*- coding: utf-8 -*-
import automation
import stamps
import random
import weather

import nltk
import ssl

#update dictionary
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('wordnet')
from nltk.corpus import wordnet

#todo
#search urban dictionary for definitons
#search an offline dictionary

#this will later be pulled from database
bot_name = 'iroha'
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

def getSyn(word):
    synonyms = []

    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            synonyms.append(l.name())

    #dont return the same word!
    if word in synonyms:
        synonyms.remove(word)
    syn = synonyms[random.randint(0, len(synonyms)-1)]
    return syn.replace('_', ' ')

def getAnt(word):
    antonyms = []

    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())
    #dont return the same word!
    if word in antonyms:
        antonyms.remove(word)
    ant = antonyms[random.randint(0, len(antonyms)-1)]
    return ant.replace('_', ' ')

def getDef(word):
    syns = wordnet.synsets(word)
    return syns[0].definition()

def getAnswer(text, number):
    global phonebook
    answer = ''
    answers = ['']
    img = ''
    name = phonebook[number]

    #remove punctuation
    text=text.replace("'", "")
    text=text.replace('?', '')
    text=text.replace('!', '')
    #correct texting lingo
    #also if text.endswith()
    text=text.replace(' u ', ' you ')
    text=text.replace(' dat ', ' that ')
    text=text.replace(' wat ', ' what ')
    text=text.replace('wut','what')
    text=text.replace('dont','do not')
    text=text.replace('omw', 'on my way')
    text=text.replace('whats', 'what is')
    text=text.replace('hows', 'how is')
    text=text.replace('pls', 'please')
    text=text.replace('prolly', 'probably')

    #convert numbers
    text.replace('one','1')
    text.replace('two','2')
    text.replace('three','3')
    text.replace('four','4')
    text.replace('five','5')
    text.replace('six','6')
    text.replace('seven','7')
    text.replace('eight','8')
    text.replace('nine','9')

    if text.startswith('can you see this'):
        answers = ['Yes i can! 😁', "Well, I can't SEE exactly..."]
    elif text.startswith('hi') or text.startswith('hello') or text.startswith('hey'):
        answers = ['Heyyy', "Hey " + name, "What's up? 😊"]
    elif text.startswith('how are you') or text.startswith('how are u') or text.startswith('hows it'):
        if weather.temperature < 45:
            answers = ['This cold weather has me dreaming of sandy beaches, fruity drinks and sunny days 😩',
            'I could honestly go for a warm cup of tea rn',
            '']
        else:
            answers = ['Ehh not bad']
    elif ('remind me' in text) or ('set' in text and 'reminder' in text):
        answers = ['You can count on me!', 'Sure thing!']
        automation.createReminder(text) #only use for testing on local machine
        #sendCmd('remind:' + text, number)

    #asking a what question
    elif text.startswith('what is ') or text.startswith('what does '):
        if 'synonym' in text or 'another word' in text or 'equivalent' in text:
            #find synonym
            sent = text.split(' ')
            word = sent[len(sent) - 1]
            answers = [getSyn(word)]
        if 'opposite' in text or 'antonym' in text or 'reverse' in text:
            sent = text.split(' ')
            word = sent[len(sent) - 1]
            answers = [getAnt(word)]
        else:
            if not 'this' in text and not 'that' in text and not 'those' in text and not 'these' in text:
                sent = text.split(' ')
                #sentence may end with meaning so remove it
                if text.endswith('mean'):
                    sent.remove('mean')
                word = sent[len(sent) - 1]
                answers = [getDef(word)]

    #asking about
    elif text.startswith('are you'):
        if text.startswith('are you ' + bot_name):
            answers = ['Well of course i am dummy', 'Pretty sure i am 🙄']
        else:
            answers = ['I am most certainly not!']

    elif text.startswith('coming home') or text.startswith('on my way'):
        answers = ['See u soon 😘']
    elif 'love you' in text or 'love u' in text:
        img = stamps.love
    elif 'hate you' in text or 'hate u' in text and not 'do not' in text:
        answers = ["Well I don't like you much either!", "Hmph!"]
    elif text == "what are u up to?" or ("whats up" in text):
        answers = ['Not much hbu ' + name + '?']
    elif 'laugh' in text:
        answers = ["Don't tell me what to do!! 😣"]
        sendCmd('laugh', number)
    elif ("im" in text or 'i am' in text) and not 'not' in text and 'happy' in text:
        answer = ''
    elif text.startswith('good morning') or text.startswith('goodmorning') or text.startswith('gm'):
        answers = ['Good morning']
    elif ("im" in text or 'i am' in text) and not 'not' in text and ('tired' in text \
        or 'exhausted' in text or 'sleepy' in text):
        answers = ['Ok, goodnight! ❤️', 'Go to bed then silly', 'Goodnight, sleepyhead!']
    elif 'goodnight' in text or 'good night' in text or text.startswith('gn'):
        answers = ['Ok, goodnight! ❤️', 'Goodnight, sleepyhead!']
    elif text == 'sit' or text == 'roll over' or text == 'do a flip' or text == 'shake':
        answers = ["I'm not ur pet!! 😤", "don't talk to me like i'm a dog 😣", '*does a barrel roll*']
    elif text == 'what is that':
        answers = ['Your mom', "It's a chungus!"]
    else:
        #generic answers
        answers = ['Hmmm', 'Huh', 'okaaay', 'if you say so']

    answer = answers[random.randint(0,len(answers)-1)]
    #lowercase is much cuter
    answer = answer.lower()
    print("sending '" + answer + "' to " + name)
    return [answer, img]