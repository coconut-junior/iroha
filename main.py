import pyglet
import time
import threading
import random
import weather
import speech

#============================
#Copyright 2021 Project Iroha
#============================

#todo
#how can this improve the lives of those with disabilities?

#basic functions
#===============
#respond to simple commands using snowboy module
#at least 3 tones of voice
#movable ears
#file sorting on computer
#can tell the weather
#remind you
#recognize people


emotion = "neutral"
animation = pyglet.image.load_animation('bootup.gif')
eyes = pyglet.sprite.Sprite(animation)
img = pyglet.image.load('crt_filter.png')
crt = pyglet.sprite.Sprite(img)
tasks = []

w = eyes.width
h = eyes.height

weather.getWeather()

window = pyglet.window.Window(width=480, height=320)#,fullscreen=True
window.set_caption("iroha")
pyglet.gl.glClearColor(0,0,0,1)

@window.event
def on_draw():
    window.clear()
    eyes.draw()
    crt.draw()

def update(dt):
    if emotion == "scared":
        eyes.update(x=random.randint(0,10), y=random.randint(0,10))

def report():
    time.sleep(2)
    speech.say('it is currently ' + str(weather.temperature) + ' degrees')
    time.sleep(3.5)
    speech.say('the humidity is ' + str(weather.humidity) + '%')
    time.sleep(3)
    speech.say('good morning! ' + speech.owner)
    time.sleep(2)

t = threading.Timer(0, report)
t.start()

pyglet.clock.schedule_interval(update, 1/60.)
pyglet.app.run()