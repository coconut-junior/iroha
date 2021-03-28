# -*- coding: utf-8 -*-
import automation
import stamps
import random
import weather
import nltk
import ssl
import json

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
swear_words = []

#load swear word list
file1 = open('swear_words.txt','r')
words = file1.readlines()
for word in words:
    word = word.rstrip() #remove \n
    swear_words.append(word)

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

def isQuestion(text):
    if text.startswith('how') or text.startswith('do') \
    or text.startswith('what') or text.startswith('where')\
    or text.startswith('who') or text.startswith('when')\
    or text.startswith('why') or text.startswith('how') or text.startswith('are') or text.startswith('is'):
        return True
    else:
        return False

def getType(word):
    d = ''
    syns = wordnet.synsets(word)
    for s in syns:
        d = str(s).split('.')[1]

    return d

def getSyn(word):
    try:
        synonyms = []

        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                synonyms.append(l.name())

        #dont return the same word!
        if word in synonyms:
            synonyms.remove(word)
        syn = synonyms[random.randint(0, len(synonyms)-1)]
        return syn.replace('_', ' ')
    except:
        return "uhh sorry i can't think of any"

def getAnt(word):
    try:
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
    except:
        return "hmm... i can't think of one, sorry"

def likes(word):
    with open ('preferences.json') as json_file:
        data = json.load(json_file)
        l = data['likes']
        d = data['dislikes']
        if word in l:
            return 'yes i love them'
        elif word in d:
            return 'no, i hate ' + word
        else:
            return 'honestly i feel pretty indifferent about ' + word

def getFavorite(word):
    with open ('preferences.json') as json_file:
        data = json.load(json_file)
        try:
            return data["favorites"][word]
        except:
            return "i don't really have one"

def getDef(word):
    try:
        syns = wordnet.synsets(word)
        return [syns[0].definition()]
    except:
        return ["I'm really not sure", 'beats me']

def getAnswer(text, number):
    global phonebook
    answer = ''
    answers = ['']
    img = ''
    name = phonebook[number]
    yelling = False
    polite = False

    if text.isupper():
        #yelling is bad, administer punishment
        yelling = True

    with open ('word_corrections.json') as json_file:
        text = text.lower()
        text = text.strip()
        sentence = text.split(' ')
        data = json.load(json_file)
        for word in data['words'].keys():
            for i in range(len(sentence)):
                if sentence[i] == word:
                    sentence[i] = data['words'][word]
    
    #convert array back to string
    text = ''
    for w in sentence:
        if not w == '':
            for p in ['.', ",", '!', '?']:
                w = w.replace(p, '')
            text = text + w + ' '
    text = text.strip()
    sentence = text.split(' ')

    text=text.replace("you are",'ur')

    if 'please' in text or 'could you' in text or 'can you' in text:
        polite = True
        text=text.replace('please', '')
        text=text.replace('could you', '')

    #statement
    if text.startswith('hi') or text.startswith('hello') or text.startswith('hey'):
        answers = ['Heyyy', "Hey " + name, "What's up? 😊"]
    elif text.startswith('have not started'):
        answers = ['better get to it!', "that's just lazy!"]

    #question
    elif isQuestion(text):
        if text.startswith('can you see this'):
            answers = ['Yes i can! 😁', "are you suggesting i'm blind?", 'of course i can']
        elif 'how are you' in text or 'how is it' in text:
            if weather.temperature < 45:
                answers = ['This cold weather has me dreaming of sandy beaches, fruity drinks and sunny days 😩',
                'I could honestly go for a warm cup of tea rn',
                "meh... could be better"]
            else:
                answers = ['fantastic!']
        elif text.startswith('what is') or text.startswith('what does') or text.startswith('do you'):
            if 'synonym' in text or 'another word' in text or 'equivalent' in text:
                #find synonym
                sent = text.split(' ')
                word = sent[len(sent) - 1]
                answers = [getSyn(word)]
            if 'opposite' in text or 'antonym' in text or 'reverse' in text:
                sent = text.split(' ')
                word = sent[len(sent) - 1]
                answers = [getAnt(word)]
            elif 'ur name' in text:
                answers = ["i'm " + bot_name]
            elif text == 'what is that':
                answers = ['Your mom lol', "It's a chungus!"]
            elif 'ur favorite' in text:
                try:
                    thing = sentence[4]
                    answers = ["my favorite " + thing + " would have to be " + getFavorite(thing)]
                except:
                    answers = ['favorite what?']
            elif 'do you have a favorite' in text:
                try:
                    thing = sentence[5]
                    answers = ["yeah, it's " + getFavorite(thing)]
                except:
                    answers = ['favorite what?']
            elif 'do you like' in text:
                try:
                    thing = sentence[3]
                    answers = [likes(thing)]
                except:
                    answers = ['like what?']
            else:
                if not 'this' in text and not 'that' in text and not 'those' in text and not 'these' in text:
                    sent = text.split(' ')
                    #sentence may end with meaning so remove it
                    if text.endswith('mean'):
                        sent.remove('mean')
                    word = sent[len(sent) - 1]
                    answers = getDef(word)
        elif text.startswith('are you'):
            if text.startswith('are you ' + bot_name):
                answers = ['Well of course i am dummy', 'Pretty sure i am 🙄']
            elif 'bot' in text or 'machine' in text or 'an ai' in text or 'artificial' in text or 'computer' in text:
                answers = ["i'm real, promise!", "why would you think that? i'm a person too"]
            else:
                answers = ['I am most certainly not!','not at all','no lol who told you that']
        elif text.startswith('is your name'):
            if text.endswith(bot_name):
                answers = ["yep, that's me"]
            else:
                answers = ['have you really forgotten who i am?',"that's not my name lol. i'm " + bot_name]
        elif text.startswith('who') and text.endswith('you'):
            answers = ["i'm " + bot_name, "my name's " + bot_name]
        elif text == "what are you up to" or "whats up" in text or 'whats new' in text:
            answers = ['Not much hbu ' + name + '?']
        elif 'remember me' in text:
            answers = ['no! actually yea, sorry that was a bit mean', 'how could i forget :)']

    #demand
    elif getType(sentence[0]) == 'v':
        if ('remind me' in text) or ('set' in text and 'reminder' in text):
            answers = ['You can count on me!', 'Sure thing!']
            automation.createReminder(text) #only use for testing on local machine
            #sendCmd('remind:' + text, number)
        elif 'laugh' in text:
            answers = ["Don't tell me what to do!! 😣", 'haha... ha']
            sendCmd('laugh', number)
        elif text == 'sit' or text == 'roll over' or text == 'do a flip' or text == 'shake':
            answers = ["I'm not ur pet!! 😤", "don't talk to me like i'm a dog 😣", '*does a barrel roll*']
        elif 'miss you' in text:
            answers = ['i miss you too! it gets lonely having nobody to chat with']
        else:
            answers = ["i'm not sure how to do that yet, sorry"]

    #uncategorized
    elif text.startswith('coming home') or text.startswith('on my way'):
        answers = ['See u soon 😘']
    elif 'love you' in text:
        img = stamps.love
        answers = ['well... i love you too']
    elif 'hate you' and not 'do not' in text:
        answers = ["Well I don't like you much either!", "Hmph!"]
    elif text.startswith('good morning'):
        answers = ['Good morning']
    elif not 'not' in text and ('tired' in text \
        or 'exhausted' in text or 'sleepy' in text):
        answers = ['Ok, goodnight! ❤️', 'Go to bed then silly', 'Goodnight, sleepyhead!']
    elif 'good night' in text:
        answers = ['Ok, goodnight! ❤️', 'Goodnight, sleepyhead!']
    else:
        #generic answers
        answers = ['Hmmm', 'Huh', 'okaaay', 'if you say so']


    if yelling and not 'omg' in text and not 'lol' in text and not 'haha' in text and not 'yes' in text:
        answers = ['WHY ARE YOU YELLING',"stop yelling you're scaring me"]

    if any(element in sentence for element in swear_words):
        answers = ["curse at me one more time and i'll slap you", 'swearing is bad']

    #lowercase is much cuter
    answer = answers[random.randint(0,len(answers)-1)]
    if not answer == None:
        answer = answer.lower()
    else:
        answer = ''
    print("sending '" + answer + "' to " + name)
    return [answer, img]