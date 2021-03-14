import pyglet
import time
import threading
import random
import weather
import speech
import filters
import os
import json
import automation
import network

#==================
#2021 Project Iroha
#==================

#on macOS brew, apt-get on linux
#brew install portaudio
#brew install nmap
#brew install ffmpeg

emotion = "neutral"
boot_anim = pyglet.sprite.Sprite(pyglet.image.load_animation('faces/bootup.gif'))
think_anim = pyglet.sprite.Sprite(pyglet.image.load_animation('faces/thinking.gif'))
idle_anim = pyglet.sprite.Sprite(pyglet.image.load_animation('faces/idle.gif'))

img = pyglet.image.load('crt_filter.png')
crt = pyglet.sprite.Sprite(img)

weather.getWeather()

window = pyglet.window.Window(width=480, height=320)#,fullscreen=True
window.set_caption("iroha")
pyglet.gl.glClearColor(0,0,0,1)
booting = True

@window.event
def on_draw():
    global booting

    window.clear()
    if network.thinking:
        think_anim.draw()
    elif booting:
        boot_anim.draw()
    else:
        idle_anim.draw()
    #crt.draw()

@window.event       
def on_close():
    automation.saveConfig()

def update(dt):
    automation.uptime += 1 #ticks or 1/60 of a second

def report():
    global booting
    automation.loadConfig()
    
    time.sleep(3)
    booting = False
    time.sleep(2)
    speech.say('it is currently ' + str(weather.temperature) + ' degrees')
    time.sleep(3.5)
    speech.say('the humidity is ' + str(weather.humidity) + '%')
    time.sleep(3)
    speech.say('good morning ' + speech.owner)
    time.sleep(2)
    speech.say('would you like to hear the news today?')
    network.running = True
    network.scan()

t = threading.Timer(0, report)
t.start()

pyglet.clock.schedule_interval(update, 1/60.)
pyglet.app.run()