import gtts
from gtts import gTTS
import vlc #pip install python-vlc
import weather
import filters
import random
import time
import speech_recognition as sr
import requests, json

owner = 'jimmy' #this can be changed with a transfer ownership command
greetings = ['']
praises = ['well done', 'good job', 'impressive', 'wonderful', 'excellent']     

def say(text):
    tts = gTTS(text)
    tts.save('speech.mp3')
    filters.pitch()
    p = vlc.MediaPlayer("output.mp3")
    p.play()
    print(text)

def praise():
    filters.factor += 0.1
    say(praises[random.randint(0, len(praises) - 1)])
    filters.factor -= 0.1

def weather_report():
    if 'snow' in weather.report:
        say('caution: there is a high chance of snow today')
    if weather.report == 'light rain':
        say('some light rain is expected today. suggestion: use an umbrella')
    if weather.report == 'overcast clouds':
        say('report: the sky is overcast. suggestion: spend a productive day indoors')
    if weather.report == 'clear sky':
        say('report: the sky is free of clouds. suggestion: spend time outdoors')

def random_advice():
    j = requests.get('https://api.adviceslip.com/advice').json()
    return j['slip']['advice']

def specific_advice(term):
    j = requests.get('https://api.adviceslip.com/advice/search/' + term).json()
    advice = ""
    slips = len(j['slips']) - 1
    
    try:
        advice = j['slips'][random.randint(0, slips)]['advice']
    except:
        advice = "i'm not sure"

    return advice

print(specific_advice('help'))