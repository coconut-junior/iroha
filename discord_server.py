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

class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')
        print('wake time is set to ' + wake_time)
        print('current date is ' + str(date.today()))

        while True:
            t = str(datetime.now().hour) + ":" + str(datetime.now().minute)
            msg = None

            #holiday events
            if date.today().month == 1 and date.today().day == 1 and t == '0:0'
                msg = msg_newyear
            if str(date.today()) == easter(date.today().year) and t == wake_time:
                msg = msg_easter
            if date.today().month == 12 and date.today().day == 25 and t == wake_time:
                msg = msg_christmas

            #message everyone iroha knows
            if not msg == None:
                for c in known_channels:
                    channel = client.get_channel(c)
                    await channel.send(msg_easter)
            #operate once a minute
            await asyncio.sleep(60)

    async def on_message(self, message):
        global known_channels
        # don't respond to ourselves
        if message.author == self.user:
            return

        answer = logic.getAnswer(message.content, automation.phone_number)
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