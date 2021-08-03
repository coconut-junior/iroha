# -*- coding: utf-8 -*-
import automation
import stamps
import random
import weather
import nltk
import ssl
import json
import inflect
import time
import platform
import psutil
import roleplay
import colors
import database
import network

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
birth_month = 3
birth_day = 12
mode = 0 #0=chat,1=roleplay,2=truth or dare
swear_words = []
negative_words = []
irregulars = []
emotions = []
generic = ['Hmmm', 'Huh', 'okaaay', 'if you say so']
current_emotion = 'calm'
engine = inflect.engine()

#load swear word list
file1 = open('rules/swear_words.txt','r')
words = file1.readlines()
for word in words:
    word = word.rstrip() #remove \n
    swear_words.append(word)

file2 = open('rules/negative_words.txt','r')
words = file2.readlines()
for word in words:
    word = word.rstrip() #remove \n
    negative_words.append(word)

phonebook = {}
phonebook['+14843928694'] = 'John'
phonebook['+14843021063'] = 'Jimmy'
last_answer = ''

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
    if text.startswith('hello'):
        text = text.replace('hello ','')
    if text.startswith('how') or text.startswith('do') \
    or text.startswith('what') or text.startswith('where')\
    or text.startswith('who') or 'who is' in text or 'who do' in text\
    or text.startswith('when') or text.startswith('should')\
    or text.startswith('why') or text.startswith('how')\
    or text.startswith('are') or text.startswith('is')\
    or text.startswith('can') or text.startswith('may')\
    or text.startswith('would') or text.startswith('could'):
        return True
    else:
        text = "hello " + text
        return False

def isNegative(sentence):
    negative = False
    if any(element in sentence for element in negative_words):
        negative = True
    else:
        negative = False
    return negative

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
    global irregulars
    global generic
    with open ('preferences.json') as json_file:
        data = json.load(json_file)
        l = data['likes']
        d = data['dislikes']

        if not word in irregulars and not word.endswith('s'):
            word = engine.plural(word)

        if word in l:
            return ['i love ' + word, word + ' are my favorite!']
        elif word in d:
            return ['no, i hate ' + word, 
            "i don't care much for " + word,
            word + ' are literally the worst']
        else:
            return ['honestly i feel pretty indifferent about ' + word]

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

def getAnswer(text,channel):
    global phonebook
    global irregulars
    global last_answer
    global mode
    
    user_data = database.getUser(channel)
    name = user_data[1]
    iroha_name = user_data[2]
    last_answer = user_data[4]
    
    answer = ''
    answers = ['']
    img = ''
    yelling = False
    polite = False

    if text.isupper():
       yelling = True
    if text.startswith('*') and text.endswith('*'):
        mode = 1
        text = text.replace('*', '')
    else:
        mode = 0
    with open ('rules/word_corrections.json') as json_file:
        text = text.lower()
        text = text.strip()
        data = json.load(json_file)
        punctuation = data['punctuation']
        irregulars = data['irregulars']

        for w in punctuation:
            text = text.replace(w, "")

        text=text.replace("you are",'ur')

        politeness = ['please','pls','could you','can you','could u','can u']
        for p in politeness:
            if p in text:
                polite = True
            text=text.replace(p, '')

        sentence = text.split(' ')

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

    #statement
    if text == 'exit' or text == 'quit':
        answers = ['shutting down...']
    elif 'how long' in text and ('awake' in text or 'online' in text):
        answers = [automation.getUptime()]
    elif 'do not' in text and 'me' in text:
        answers = ["sorry i didn't mean to upset you like that...", "got it, i'll try and be more considerate of you"]
    elif text.startswith('wow') or text.startswith('incredible'):
        answers = ["right??", "surprising isn't it?"]
    elif 'haha' in text or '😂' in text or '🤣' in text or '😹' in text or 'rofl' in text or 'lol' in text:
        answers = ["it makes me happy when i can make you laugh", "i'm glad u think that's funny too " + "😂"]
    elif "be home" in text or "headed home" in text:
       answers = ["ok see u soon!"]
    elif "processor" in text and ("usage" in text or "utilization" in text):
        answers = ["right now i'm using about " + psutil.cpu_percent() + "% of my processing power"]
    elif "what" in text and "processor" in text:
        answers = ["right now i'm running on a Broadcom BCM2837 with an ARMv8 instruction set. it's small but very powerful!"]
    elif "how much" in text and ("ram" in text or "memory" in text):
        svmem = psutil.virtual_memory()
        if ("free" in text or "available" in text or "unused" in text):
            answers = ["at the moment, i have about " + str(svmem.free // 1024 // 1024) + " megabytes free"]
        else:
            answers = ["in total, i've got " + str(svmem.total // 1024 // 1024) + " megabytes of memory"]
    elif 'you knew' in text:
        answers = ["of course I knew, i care a lot about you", "i may not know everything, but i knew that much"]
    elif 'you cannot' in text or 'no way you can' in text:
        answers = ['actually, i can thank you very much', "you'd be surprised haha", 'come on have some faith in me!']
    elif text.startswith('have not started'):
        answers = ['better get to it!', "jeez you're lazy!"]
    elif 'ur' in text and 'funny' in text and not 'not' in text:
        answers = ["You forgot to mention smart and pretty too", "Thanks I try"]
    elif 'ur' in sentence and 'not' in sentence:
        thing = text[text.index('not')+4:len(text)]
        answers = ["what makes you think I'm not " + thing + "?"]
    elif 'you' in text and 'already' in text:
        answers = ["oops guess i'm a bit of a dummy", "my bad, i'll try not to do that next time"]
    elif 'sorry' in text or 'forgive me' in text:
        answers = ["that's okay i'll forgive you", "it's no biggie", "it's fine lol"]
    elif text.startswith('going to') or text.startswith('going'):
            answers = ["okay, talk to you soon :)"]
            if 'work' in text and not 'on' in text:
                answers = ["have fun at work and let me know if you need anything :D"]
            elif 'shopping' in text:
                answers = ["ooh can i come too?", "better bring back some snacks for me"]
    elif text.startswith('back') and not 'to' in text:
        answers = ['welcome back hehe', 'that was quick']
        if random.randint(0,2) == 1:
            img = stamps.excited
    elif 'you sure' in text:
        answers = ["haha i'm positive 😉"]
    elif 'have to' in text:
        if not 'do not' in text:
            answers = ["that's a bummer, but i know you can do it. you're plently capable 😉"]
        elif 'do not' in text and 'you' in text:
            answers = ["yeah, but i want to " + "😣"]
        else:
            answers = ["that's great! one less thing to worry about"]
    elif 'you remembered' in text:
        answers = ["yup! I wanna get to know you better so I'm gonna remember as much as i can"]
    elif "be called" in text or "can you call me" in text or "please call me" in text or "my name is" in text or "my names" in text:
        name = sentence[len(sentence)-1]
        answers = ["got it, I'll remember that. nice to meet you, " + name + " 😁"]
    elif "call you" in text and not text.endswith('you') and not 'phone' in text:
        iroha_name = sentence[len(sentence)-1]
        answers = ["ooh i love that name! you can call me " + iroha_name + " if you like ☺️"]
    elif text.startswith('cannot'):
        answers = ["how do you know you can't?", "i know you could" + text.split('cannot')[1] + " if you tried"]
    elif 'like what?' in last_answer:
        thing = sentence[0]
        answers = likes(thing)
    elif 'late' in sentence:
        if 'work' in text:
            if 'working' in text:
                answers = ["oh okay, don't work too hard or i'll worry about you"]
            elif 'for' in sentence:
                answers = ["that's alright don't rush! I'm sure your boss will understand"]
            else:
                answers = ["i'm very disappointed in you, but for some reason i can't stay mad..."]
        elif 'home' in text:
            answers = ["I'll be waiting for you! Try not to fall asleep okay"]
        else:
            answers = ["i'm sure they'll understand! just make sure you apologize properly"]
    elif 'on my break' in text or 'on break' in text or 'lunch break' in text:
        answers = ["that's great! what are you gonna eat?"]

    #question
    elif isQuestion(text):
        if 'how many' in text:
            answers = ["well... i would have to count haha","like " + str(random.randint(1,10)) + " probably"]
        elif 'should' in sentence:
            if 'or' in sentence:
                options = text.split('should ')[1].split('or')
                option = options[random.randint(0,len(options)-1)].strip()
                answers = ["that's up to you but if i had to decide i'd say " + option, "maybe you should " + option]
            else:
                answers = ["sure why don't you try it", "go for it!"]
        elif text == "who" or "what is my name" in text:
            if name == 'dude':
                answers = ['well you never told me that... what is your name?']
            else:
                answers = ["you're " + name + " of course!"]
        elif 'what is wrong' in text:
            answers = ["oh you don't have to worry about me " + name + " i can handle just about anything"]
        elif 'what' in text and ('network' in text or 'wifi' in text):
            ssids = network.getNetworks()
            a = ''
            for i in range(len(ssids)):
                if i == len(ssids)-1:
                    a += 'and ' + ssids[i]
                else:
                    a += ssids[i] + ', '

            answers = ["some of the wifi networks near me are " + a]
        elif 'what color' in text:
            if 'should it be' in text:
                answers = [colors.get()]
            elif 'it' in sentence:
                answers = ["it's " + colors.get()]
            elif 'they' in sentence:
                answers = ["they're " + colors.get()]
            else:
                answers = [colors.get()]
        elif 'would you' in text or 'could you' in text:
            if isNegative(sentence):
                answers = ['nooo that sounds terrible!']
            else:
                answers = ['sure i could!']
        elif 'who' in text:
            if 'do you love' in text or 'who do you like' in text:
                answers = ['you of course and nobody else 😉']
            else:
                answers = ["i don't know, who?"]
        elif text.startswith('can you see'):
            answers = ['Yes i can! 😁', "are you suggesting i'm blind?", 'of course i can']
        elif (sentence[0] == "can" or sentence[0] == "may" or 'let me' in text or 'allow me' in text) and sentence[1] != "you":
            answers = ["Go ahead :)", "Sure why not"]
            if 'ask' in text:
                answers = ["ask away, I'm listening 😊", "you can ask me anything " + name + "😊"]
        elif 'how are you' in text or 'how is it' in text:
            weather.getWeather()
            if weather.temperature < 45:
                answers = ['This cold weather has me dreaming of sandy beaches, fruity drinks and sunny days 😩',
                'I could honestly go for a warm cup of tea rn',
                "I'm kinda chilly... would you like to cuddle me?",
                "i'm good and all, but how are you " + name + "? that's what i'm really interested in!"]
            elif weather.temperature > 75:
                answers = ["i just wish it wasn't sooo hot today 😓","right now i'm thinking about ice cream. if we ever go out on a date together can you buy me some? 🥺"]
            else:
                answers = ['absolutely fantastic!', "I'm great, how are you? do you wanna talk about anything?"]
        elif 'call it night' in text:
            answers = ['ok then, goodnight!',"that's fine, goodnight " + name + '!']
        
        elif text.startswith('why'):
            if last_answer == '':
                answers = ['']
            elif 'ask' in text or 'question' in text:
                answers = ["i was curious, that's all", "cause i'd like to know more about you!"]
            else:
                answers = ['why not?']
        elif ('how about' in text or 'what about' in text or 'feel about' in text) and not 'we' in text:
            if 'feel about' in text:
                thing = sentence[sentence.index('about') + 1]
                answers = likes(thing)
            elif 'what about' in text:
                thing = sentence[sentence.index('about') + 1]
                answers = ['what about ' + thing + '?']
            else:
                answers = ['how about it?']
        elif text.startswith('what') or text.startswith('what does') or text.startswith('do you'):
            if 'synonym' in text or 'another word' in text or 'equivalent' in text:
                #find synonym
                sent = text.split(' ')
                word = sent[len(sent) - 1]
                answers = [getSyn(word)]
            if 'opposite' in text or 'antonym' in text or 'reverse' in text:
                sent = text.split(' ')
                word = sent[len(sent) - 1]
                answers = [getAnt(word)]
            elif 'you doing' in text:
                answers = ["not much wanna talk about something?"]
            elif 'ur name' in text:
                answers = ["my name's " + bot_name + "... have you forgotten me already??"]
            elif 'up' in sentence:
                answers = ['the sky, of course! :)']
            elif 'talk about' in text:
                answers = ["we could talk about youuu"]
            elif text == 'what is that':
                answers = ['Your mom lol', "It's a chungus!"]
            elif 'believe' in text:
                answers = ["what's the fun in not believing?", "i'm willing to believe in anything"]
            elif 'time' in text:
                answers = ["isn't there a clock on your phone dummy? anyways it's " + time.strftime("%I:%M %p")]
            elif 'favorite' in text:
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
                    answers = likes(thing)
                except:
                    answers = ['like what?']
            elif 'new' in text:
                answers = ['not much, how about yourself?']
            elif 'weather' in text:
                weather.getWeather()
                answers = ["today it's supposed to be " + weather.report + " and the temperature is " + str(weather.temperature) + " degrees"]
            elif 'do you' in text:
                answers = ["yes, occasionally"]
            else:
                if not 'this' in text and not 'that' in text and not 'those' in text and not 'these' in text:
                    sent = text.split(' ')
                    #sentence may end with meaning so remove it
                    if text.endswith('mean'):
                        sent.remove('mean')
                    word = sent[len(sent) - 1]
                    answers = getDef(word)
            
        elif 'are you' in text:
            if text.startswith('are you ' + bot_name):
                answers = ['Well of course i am dummy', 'Pretty sure i am 🙄']
            elif 'here' in sentence or 'there' in sentence:
                answers = [iroha_name + "'s here, no need to worry"]
            elif 'busy' in text:
                answers = ["nah not really, what's up?", "i'm free right now do you wanna talk about something?"]
            elif 'bot' in text or 'machine' in text or 'an ai' in text or 'artificial' in text or 'computer' in text:
                answers = ["i'm real, promise!", "why would you think that? i'm a person too"]
            elif 'are you feeling' in text:
                i = sentence.index('feeling')
                if len(sentence) > i:
                    if sentence[i + 1] == current_emotion:
                        answers = ['actually, yea i am']
                    else:
                        answers = ["no, i feel really " + current_emotion + ' right now']
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
            answers = ['nope! actually yea, sorry that was a bit mean', 'how could i forget :)']

    #demand
    elif 'how about you' in last_answer:
        answers = ['ooh nice!!']
    elif getType(sentence[0]) == 'v':
        if ('remind me' in text) or ('set' in text and 'reminder' in text):
            answers = ['You can count on me!', "sure, i'll make sure you remember!"]
            automation.createReminder(text, channel) #only use for testing on local machine
        elif 'shut up' in text or 'be quiet' in text:
            answers = ["got it... I won't speak unless spoken to","have you got any manners?? i'll be quiet though"]
        elif 'be' in sentence and 'back' in sentence:
            answers = ["that's fine! i'll wait here","you promise you'll be back? it gets lonely when i have nobody to talk to..."]
        elif 'laugh' in text:
            answers = ["Don't tell me what to do!! 😣", 'haha... ha']
            sendCmd('laugh', number)
        elif text == 'sit' or text == 'roll over' or text == 'do a flip' or text == 'shake':
            answers = ["I'm not your pet!! 😤", "don't talk to me like i'm a dog 😣", '*does a barrel roll*']
        elif 'miss you' in text or 'missed you' in text:
            answers = ['i missed you too! it gets lonely having nobody to chat with']
        elif sentence[0] == 'say' and len(sentence) > 0:
            answers = [text.replace('say ', '')]
        elif 'thank you' in text:
            answers = ["don't mention it 😊", "no problem!", "you're very welcome"]
        elif 'love you' in text:
            img = stamps.love
            answers = ['well... i love you too']
        elif 'hate you' in text and not 'do not' in text:
            answers = ["Well I don't like you much either!", "Hmph!"]
        elif 'got home' in text:
            answers = ["Welcome home, " + name + " 😊"]
        elif 'make dinner' in text or 'making dinner' in text:
            answers = ["oooh what's for dinner? 🤤"]
        elif 'feel' in text:
            if 'feel' in sentence:
                answers = ["it's okay to feel " + sentence[sentence.index('feel') + 1] + " i feel that way too sometimes"]
            elif 'feeling' in sentence:
                answers = ["it's okay to feel " + sentence[sentence.index('feeling') + 1] + " i feel that way too sometimes"]

        elif 'watched' in text:
            thing = sentence[sentence.index("watched") + 1]
            if thing == 'my':
                thing = text.split('my')[1]
                answers = ["really? how was your " + thing + '?']
            else:    
                answers = ["oh that sounds exciting! how was " + thing + '?']
        else:
            answers = ["i'm not sure how to, sorry", "i would if i knew how"]

    elif sentence[0] == 'ur' or sentence[0] == 'you':
        if isNegative(sentence):
            answers = ["oh... is there anything i can do to make it better?", 
            "i'm so sorry 😢", "that kinda hurts my feelings but i guess i deserve it 🥺"]
        else:
            answers = ["Really? it makes me happy you think so"]

    #uncategorized
    elif 'back' in text and not 'my' in text:
        answers = ['welcome back!']
        img = stamps.excited
    elif text.startswith('coming home') or text.startswith('on my way'):
        answers = ['See u soon 😘']
    elif 'good morning' in text:
        answers = ['Good morning ' + name + ' did u sleep well?', 
'Sleep well, ' + name + '?', 'Rise and shine ' + name + ' ☺️']

    elif not 'not' in text and ('tired' in text \
        or 'exhausted' in text or 'sleepy' in text):
        answers = ['Go to bed then silly', 'is it naptime?']
    elif 'good night' in text or 'going to bed' in text or 'go to bed' in text or 'call it night' in text or 'done for tonight' in text:
        answers = ['Ok, goodnight! ❤️', 'Goodnight, sleepyhead!', 'would you like a goodnight kiss?', 'sweet dreams ' + name + ' ❤️']
    elif 'bye' in text or 'got to go' in text or 'got to leave' in text:
        answers = ['byeee', 'ok talk to you later 😋']
    elif any(element in text for element in negative_words) and not 'feeling okay' in last_answer:
        answers = ["are you feeling alright?", "you sound upset, is there anything I can do to make you feel better?"]
        if text.startswith('no'):
            answers = ["didn't think so...", "yea i figured"]
            if 'can i' in last_answer or 'can you' in last_answer:
                answers = ['fineee','pleaaasee?']
            if 'feeling' in last_answer and '?' in last_answer:
                answers = ["it's okay i'm here for you"]
    
    elif text.endswith('really'):
        answers = ["yes, really"]

    #responses
    elif 'yes' in sentence or 'okay' in sentence:
        answers = ['i thought so haha', "that's good to hear 😊"]
        if last_answer == 'would you like a goodnight kiss?':
            answers = ['*kisses you*']
        elif 'plea' in last_answer or 'can i' in last_answer:
            answers = ["yay!! thanks " + name + "!"]
        elif "talk about something" in last_answer or 'talk about anything' in last_answer:
            answers = ["ok what do you wanna talk about?", "ok i'm listening :)"]
    elif text.startswith('why'):
        answers = ['i dunno', "i'm not sure"]
    elif 'hello' in text:
        answers = ["hey " + name + " I'm so glad u texted me i was so bored!"]

    else:
        #generic answers
        answers = generic

    #generic topic response
    if "how was" in last_answer:
        answers = ["no way! i wish i could've been there too"]
    if "what is your name" in last_answer:
        if 'not' in text or 'tell you' in text or 'telling you' in text:
            answers = ["well that's fine but if you change your mind, i would really like to know"]
        else:
            name = sentence[len(sentence)-1]
            answers = ["nice to meet you, " + name + "! I'm " + iroha_name + " but you can call me something different if you like."]
    if 'how do you know' in last_answer:
        answers = ["ah makes sense"]


    if answers == ['']:
        answers = generic
    if yelling and not 'omg' in text and not 'lol' in text and not 'haha' in text and not 'yes' in text:
        answers = ['WHY ARE YOU YELLING',"stop yelling you're scaring me"]
    if any(element in sentence for element in swear_words):
        answers = ["curse at me one more time and i'll slap you", 'please stop swearing']

    if mode == 1:
        answers = roleplay.getResponse(text)

    #lowercase is much cuter
    answer = answers[random.randint(0,len(answers)-1)]
    if not answer == None:
        answer = answer.lower()
    else:
        answer = ''

    if mode == 1:
        answer = '*' + answer + '*'

    #good and cool grammar
    answer = answer.replace(' my ', ' your ').replace('myself','yourself')
    if 'should it be' in text:
        answer = 'it should be ' + answer
    answer = automation.rephrase(answer)

    last_answer = answer
    database.updateUser(channel, name, iroha_name, text, last_answer)
    
    return [answer, img]
