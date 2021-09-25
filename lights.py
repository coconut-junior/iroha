# coding=utf-8
import sys
from time import sleep
from lifxlan import RED, BLUE, GREEN, LifxLAN

print('Loading LIFX module...')
lifx = LifxLAN()
devices = lifx.get_lights()

def main():
    global devices
    original_power = 65535
    blink(5, 1)

def blink(times, interval):
    global devices

    for i in range(times):
        for bulb in devices:
            try:
                bulb.set_power('off')
                sleep(interval)
            except:
                bulb.set_power('off')
                sleep(interval)
            try:
                bulb.set_power('on')
                sleep(interval)
            except:
                bulb.set_power('on')
                sleep(interval)

if __name__=="__main__":
    main()

