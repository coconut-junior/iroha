# coding=utf-8
import sys
from time import sleep
from lifxlan import RED, BLUE, GREEN, LifxLAN

print('Loading LIFX module...')

lifx = LifxLAN()
devices = lifx.get_lights()
print(devices)

def turn_on():
    global devices
    for bulb in devices:
        try:
            bulb.set_power('on')
        except:
            turn_on()

def turn_off():
    global devices
    for bulb in devices:
        try:
            bulb.set_power('off')
        except:
            turn_off()

def blink(times, interval):
    global devices

    for i in range(times):
        turn_on()
        sleep(interval)
        turn_off()
        sleep(interval)

