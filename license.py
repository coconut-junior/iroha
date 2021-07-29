import time
import random

char_list = "abcdefghijklmnopqrstuvwxyz1234567890"
secret = 800
check = 8
length = 15

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
    
    print(key)
    return key

