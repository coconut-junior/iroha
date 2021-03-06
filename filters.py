import os
import sys

home_dir = os.getcwd()
factor = 0.7
tempo = 1

def pitch():
    print(home_dir)
    os.system(home_dir + '/bin/ffmpeg -y -i speech.mp3 -af "asetrate=44100*' + str(factor) + ',atempo=' + str(tempo) + ',aresample=44100" output.mp3')
