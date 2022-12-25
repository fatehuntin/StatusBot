import discord
import asyncio
import time
import logging
from discord.ext import tasks
from discord import app_commands
from config import uuid_list, username_list, debug, api_key, KEY, mainchannel, loggingchannel, modifier, onlineemoji, offlineemoji, uptime
from utils import timestamper, hypixelapi

class discoword(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False
    async def on_ready(self):
        status.start()
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f"We have logged in as {self.user}.")

client = discoword()
tree = app_commands.CommandTree(client)
online_list = []
last_online = [0,0,0]
channel = client.get_channel(mainchannel)
logchannel = client.get_channel(loggingchannel)
for x in uuid_list:
    online_list.append('False')
gamers = []
@tasks.loop(seconds=5)
async def status():
    for index, uuid in enumerate(uuid_list):
        parse_json_apidata_hypixel = hypixelapi(uuid,api_key)
        channel = client.get_channel(mainchannel)
        logchannel = client.get_channel(loggingchannel)
        if debug:
            logging.basicConfig(
                filename="logs.log",
                format='%(asctime)s %(levelname)-8s %(message)s',
                level=logging.DEBUG,
                datefmt='%Y-%m-%d %H:%M:%S')
        if not debug:
            logging.basicConfig(
                filename="logs.log",
                format='%(asctime)s %(levelname)-8s %(message)s',
                level=logging.WARNING,
                datefmt='%Y-%m-%d %H:%M:%S')
        try: 
            online_status = parse_json_apidata_hypixel['session']['online']
        except Exception:
            logging.warning("API ERROR")
            if debug:
                await logchannel.send("API error perhaps")
            pass
        username = username_list[index]
        current_time = int(time.time())
        if debug: 
            print(online_status, username, online_list[index], online_list,last_online)
            logging.debug(online_status, online_list[index], username, last_online[index], timestamper(current_time - last_online[index]))
        if online_status:
            statusname = "ONLINE " + onlineemoji
            online_status = 'True'
            online_time = ""
        if not online_status:
            statusname = "OFFLINE " + offlineemoji
            online_status = 'False'
            if uptime:
                online_time = " They were online for: " + timestamper(current_time - last_online[index])
            else: 
                online_time = ""
        if online_status != online_list[index]:
            await channel.send(modifier[index] + username + " has been " + statusname + " since <t:" + str(current_time) + ":R>" + online_time)
            online_list[index] = online_status
            if online_status == 'True':
                gamers.append(username)
                last_online[index] = current_time
            elif online_status == 'False':
                gamers.remove(username)
        else:
            pass
        if len(gamers) > 1:
            separator = ", "
            await client.change_presence(activity=discord.Game(name=separator.join(gamers) + " are online"))
        elif len(gamers) == 1:
            separator = ", "
            await client.change_presence(activity=discord.Game(name= separator.join(gamers) + " is online")) 
        elif len(gamers) == 0:
            await client.change_presence(activity=discord.Game(name="No one is online"))
        await asyncio.sleep(5)

client.run(KEY)
