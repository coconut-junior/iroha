import time
import random
from datetime import datetime

char_list = "abcdefghijklmnopqrstuvwxyz1234567890"
secret = 1688
check = 20
length = 20

def activationDate(key):
    ts = int(key.split('-')[1])
    date = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return date

def validate(key):
    total = 0
    for i in range(check):
        total += ord(key[i])
    if total == secret:
        return True
    else:
        return False

def generate():
    global secret
    activ_time = time.time()
    key = ''
    valid = False
    
    while not valid:
        while len(key) < length:
            c = char_list[random.randint(0,len(char_list)-1)]
            key += c
        if validate(key):
            valid = True
            break
        else:
            key = ''
    key += '-' + str(int(time.time()))
    print(key)
    return key
