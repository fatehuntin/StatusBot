import discord
import asyncio
import time
import logging
from discord.ext import tasks, commands
from config import uuid_list, username_list, debug, api_key, KEY, mainchannel, loggingchannel, modifier, onlineemoji, offlineemoji, uptime, fortnitechannel, fortniteusername, dmuser, mayorchannelid
from utils import timestamper, hypixelapi, fortniteapi, mayorapi, mayorgraphing, firstrun
from totaltime import totaltime
description = """
Status Bot
https://github.com/fatehuntin/StatusBot
"""
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(
    command_prefix= "~",
    description = description,
    intents = intents,
)


bot.load_extension("status")
bot.load_extension("fortnitewins")
bot.load_extension("playtime")
bot.load_extension("housekeeping")
bot.load_extension("mayorchannel")
@bot.event
async def on_ready():
    logchannel = bot.get_channel(loggingchannel)
    await logchannel.send("Im Gay")
    await logchannel.edit(content="")
    await bot.sync_commands()
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('-------------------------------------------------')
online_list = []
online_status =[]
last_online = [0,0,0,0]
channel = bot.get_channel(mainchannel)
logchannel = bot.get_channel(loggingchannel)
for index, x in enumerate(uuid_list):
    online_list.append('False')
    online_status.append(False)
    last_online.append(int(time.time()))
gamers = []
current_time = int(time.time())

bot.load_extension("info")
bot.run(KEY)
