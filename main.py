import pyglet
import time
import threading
import random
import weather
import speech
import filters
import os
import network
import json
import automation

#==================
#2021 Project Iroha
#==================

#on macOS brew, apt-get on linux
#brew install portaudio
#brew install nmap
#brew install ffmpeg

emotion = "neutral"
animation = pyglet.image.load_animation('faces/bootup.gif')
eyes = pyglet.sprite.Sprite(animation)
img = pyglet.image.load('crt_filter.png')
crt = pyglet.sprite.Sprite(img)

weather.getWeather()

window = pyglet.window.Window(width=480, height=320)#,fullscreen=True
window.set_caption("iroha")
pyglet.gl.glClearColor(0,0,0,1)

@window.event
def on_draw():
    window.clear()
    eyes.draw()
    #crt.draw()

@window.event       
def on_close():
    automation.saveConfig()
    network.running = False

def update(dt):
    automation.uptime += 1 #ticks or 1/60 of a second

    if emotion == "scared":
        eyes.update(x=random.randint(0,10), y=random.randint(0,10))

def report():
    automation.loadConfig()
    time.sleep(2)
    speech.say('it is currently ' + str(weather.temperature) + ' degrees')
    time.sleep(3.5)
    speech.say('the humidity is ' + str(weather.humidity) + '%')
    time.sleep(3)
    speech.say('good morning ' + speech.owner)
    time.sleep(2)
    speech.say('would you like to hear the news today?')
    network.running = True

t = threading.Timer(0, report)
t.start()

pyglet.clock.schedule_interval(update, 1/60.)
pyglet.app.run()