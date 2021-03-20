# -*- coding: utf-8 -*-
import automation
import stamps
import random
import weather

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

    #remove punctuation
    text.replace("'", "")
    text.replace('?', '')
    text.replace('!', '')
    #correct texting lingo
    #also if text.endswith()
    text.replace(' u ', ' you ')
    text.replace(' dat ', ' that ')
    text.replace(' wat ', ' what ')
    text.replace('pls', 'please')
    text.replace('prolly', 'probably')

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
            answers = ['Not bad']
    elif ('remind me' in text) or ('set' in text and 'reminder' in text):
        automation.createReminder(text) #only use for testing on local machine
        #sendCmd('remind:' + text, number)
    elif text.startswith('what is '):
        #look up answer thru api
        answers = ["I'm not sure yet"]
    elif text == 'coming home' or text == 'on my way':
        answers = ['See u soon 😘']
    elif 'love you' in text or 'love u' in text:
        img = stamps.love
    elif 'hate you' in text or 'hate u' in text:
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
        answers = ["I'm not ur pet!! 😤"]
    elif text == 'whats that':
        answers = ['Your mom', "It's a chungus!"]
    else:
        #generic answers
        answers = ['Hmmm', 'Huh']

    answer = answers[random.randint(0,len(answers)-1)]
    print("sending '" + answer + "' to " + name)
    return [answer, img]