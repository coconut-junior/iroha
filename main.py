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
boot_anim = pyglet.image.load_animation('faces/bootup.gif')
think_anim = pyglet.image.load_animation('faces/thinking.gif')
eyes = pyglet.sprite.Sprite(boot_anim)
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

    if network.thinking:
        eyes = pyglet.sprite.Sprite(think_anim)

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