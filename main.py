import json
import requests
import discord
import asyncio
import time
from discord.ext import commands, tasks
from discord import app_commands
from config import uuid_list, username_list, debug, api_key, KEY, mainchannel, loggingchannel, modifier, onlineemoji, offlineemoji, uptime


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
def timestamper(epochin):
    if int(epochin) < 60:
        epoch = epochin + " seconds"
    elif int(epochin) < 3600:
        epoch = str(int(int(epochin)/60)) + " minutes and " + str(int(epochin)%60) + " seconds"
    elif int(epochin) < 86400:
        epoch = str(int(int(epochin)/3600)) + " hours, " + str(int(int(epochin)%3600/60)) + " minutes and " + str(int(epochin)%60) + " seconds"
    elif int(epochin) > 86400:
        epoch = str(int(int(epochin)/86400)) + " days, " + str(int(int(epochin)%86400/3600)) + " hours, " + str(int(int(epochin)%3600/60)) + " minutes and " + str(int(epochin)%60) + " seconds"
    return epoch
@tasks.loop(seconds=5)
async def status():
    for index, uuid in enumerate(uuid_list):
        API_data_hypixel = requests.get('https://api.hypixel.net/status?key=' + api_key + '&uuid='+uuid)
        apidata_hypixel = API_data_hypixel.text
        parse_json_apidata_hypixel = json.loads(apidata_hypixel)
        channel = client.get_channel(mainchannel)
        logchannel = client.get_channel(loggingchannel)
        try: 
            online_status = parse_json_apidata_hypixel['session']['online']
        except Exception:
            if debug:
                await logchannel.send("API error perhaps")
            pass
        username = username_list[index]
        if debug: print(online_status, username, online_list[index], online_list,last_online)
        
        current_time = int(time.time())
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
                #gamers.remove(username)
                pass
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
