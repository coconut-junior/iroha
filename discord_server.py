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

msg_newyear = 'Happy new year! 🥳🥂'
msg_easter = 'Happy easter! 🐰'
msg_christmas = 'Merry Christmas! 🎄'
known_channels = [] #we will keep these anonymous for now
wake_time = "9" + ":" + str(random.randint(0,30))


#fix reminders!

class MyClient(discord.Client):

    async def on_ready(self):
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

    async def on_message(self, message):
        global known_channels
        # don't respond to ourselves
        if message.author == self.user:
            return

        answer = logic.getAnswer(message.content, automation.phone_number, message.channel.id)
        if not answer[1] == '':
            with open(answer[1], 'rb') as f:
                picture = discord.File(f)
                await message.channel.send(file=picture)

        if not message.channel.id in known_channels:
            known_channels.append(message.channel.id)
            print('adding channel ' + str(message.channel.id))

        await message.channel.send(answer[0])

client = MyClient()
client.run('ODI2MTQxMjA2MDY1MDUzNzI3.YGIJ9A.5jYJ7v6JYFQgXoAxOFYK5MBy4Ag')
