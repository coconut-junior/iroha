import gtts
from gtts import gTTS
import vlc #pip install python-vlc
import weather
import filters

owner = 'jimmy' #this can be changed with a transfer ownership command
greetings = ['']

def say(text):
    tts = gTTS(text)
    tts.save('speech.mp3')
    filters.pitch()
    p = vlc.MediaPlayer("output.mp3")
    p.play()
    print(text)

def inquire():
    if 'snow' in weather.report:
        say('caution: there is a high chance of snow today')
    if weather.report == 'light rain':
        say('some light rain is expected today. suggestion: use an umbrella')
    if weather.report == 'overcast clouds':
        say('report: the sky is overcast. suggestion: spend a productive day indoors')
    if weather.report == 'clear sky':
        say('report: the sky is free of clouds. suggestion: spend time outdoors')