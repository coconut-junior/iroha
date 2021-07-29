import discord
import logic
import automation
import random
import asyncio
import time
from datetime import datetime
from datetime import date
import json
import random
from dateutil.easter import *
import database

msg_newyear = 'Happy new year! 🥳🥂'
msg_easter = 'Happy easter! 🐰'
msg_christmas = 'Merry Christmas! 🎄'
known_channels = []
wake_time = "9" + ":" + str(random.randint(0,30))
wait_time = 0
cache = []

class MyClient(discord.Client):

    async def on_ready(self):
        global wait_times

        with  open('startup.txt', 'r') as f:
            contents = f.read()
            print(contents)
            print('')
        
        print('login successful')
        print('client name: ' + client.user.name)
        print('client id: ' + str(client.user.id))
        print('------')
        print('current date is ' + str(date.today()))
        print('wake time is set to ' + wake_time)

        while True:
            global wait_time
            global cache
            t = str(datetime.now().hour) + ":" + str(datetime.now().minute)
            msg = None

            #holiday events
            if date.today().month == 1 and date.today().day == 1 and t == '0:0':
                msg = msg_newyear
            if str(date.today()) == easter(date.today().year) and t == wake_time:
                msg = msg_easter
            if date.today().month == 12 and date.today().day == 25 and t == wake_time:
                msg = msg_christmas

            for r in automation.reminders:
                if str(date.today()) == r['date'] and t == r['time']:
                    print('sending reminder')
                    m = r['message']
                    channel = client.get_channel(r['channel'])
                    await channel.send("hey looks like it's time to " + m)

            #message everyone iroha knows
            if not msg == None:
                for c in known_channels:
                    channel = client.get_channel(c)
                    await channel.send(msg)
            
            #operate once a minute
            await asyncio.sleep(60)
            automation.uptime += 1
            wait_time += 1
            users = database.getAll()
            t = time.localtime()
            hour = t.tm_hour
            minute = t.tm_min

            for u in users:
                uid = str(u[0])
                last_answer = u[4]

                if wait_time == 2 and '?' in last_answer and not 'really' in text and uid in cache:
                    print('sending annoyed message...')
                    channel = client.get_channel(int(uid))
                    annoyed_msg = ["so are you gonna answer me or what lol",
                            "heyyy i asked you a question silly"]
                    msg = annoyed_msg[random.randint(0,len(annoyed_msg)-1)]
                    await channel.send(msg)
                    database.updateUser(u[0],u[1],u[2],u[3],msg)
                
                if hour == 0 and minute == 14 and not 'night' in last_answer and not 'dream' in last_answer and uid in cache:
                    print('sending bedtime reminder...')
                    bedtime_warnings = ["hey it's getting kinda late... do you think you're gonna go to bed soon?"]
                    msg = bedtime_warnings[random.randint(0,len(bedtime_warnings)-1)]
                    channel = client.get_channel(int(uid))
                    await channel.send(msg)
                    database.updateUser(u[0],u[1],u[2],u[3],msg)
                
            if wait_time == 2:
                wait_time = 0
    async def on_message(self, message):
        global cache
        # don't respond to ourselves
        if message.author == self.user:
            return

        answer = logic.getAnswer(message.content, message.channel.id)
        if not answer[1] == '':
            with open(answer[1], 'rb') as f:
                picture = discord.File(f)
                await message.channel.send(file=picture)

        channel = str(message.channel.id)
        await message.channel.send(answer[0])
        if not channel in cache:
            cache.append(channel)


client = MyClient()
client.run('ODI2MTQxMjA2MDY1MDUzNzI3.YGIJ9A.5jYJ7v6JYFQgXoAxOFYK5MBy4Ag')
