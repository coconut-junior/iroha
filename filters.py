import os
import sys

home_dir = os.getcwd()
binary_dir = ''

if os.name == 'nt':
    binary_dir = home_dir + '/bin/win32/'
elif os.name == 'posix':
    binary_dir = ''
else:
    binary_dir = ''

factor = 0.75
tempo = 0.9
highpass = 200
lowpass = 1500

def pitch():
    print(home_dir)
    os.system(binary_dir + 'ffmpeg -y -i speech.mp3 -af "asetrate=44100*' + str(factor) + ',atempo=' + str(tempo) + ',aresample=44100, highpass=f=' + str(highpass) + ', lowpass=f=' + str(lowpass) + '" output.mp3')
