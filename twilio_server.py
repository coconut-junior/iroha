import subprocess

#serve application publicly
subprocess.run('lt --port 5000 -s "iroha" & python3 sms.py', shell=True)