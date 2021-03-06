import os
import sys

home_dir = os.getcwd()
binary_dir = ''

if os.name == 'nt':
    binary_dir = '/bin/win32/'
elif os.name == 'darwin':
    binary_dir = '/bin/darwin/'
else:
    binary_dir = ''

factor = 0.75
tempo = 1

def pitch():
    print(home_dir)
    os.system(home_dir + binary_dir + 'ffmpeg -y -i speech.mp3 -af "asetrate=44100*' + str(factor) + ',atempo=' + str(tempo) + ',aresample=44100" output.mp3')
