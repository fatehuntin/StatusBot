import json
import requests
import discord
import asyncio
import time
from discord.ext import commands, tasks
from discord import app_commands
from config import uuid_list, username_list, debug, api_key, KEY, mainchannel, loggingchannel

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
online_list = ['False','False','False']
gamers = []
@tasks.loop(seconds=5)
async def status():
    for index, uuid in enumerate(uuid_list):
        API_data_hypixel = requests.get('https://api.hypixel.net/status?key=' + api_key + '&uuid='+uuid)
        #API_data_mojang = requests.get('https://api.mojang.com/user/profile/' + uuid)
        apidata_hypixel = API_data_hypixel.text
        #apidata_mojang = API_data_mojang.text
        parse_json_apidata_hypixel = json.loads(apidata_hypixel)
        #parse_json_apidata_mojang = json.loads(apidata_mojang)
        try: 
            online_status = parse_json_apidata_hypixel['session']['online']
        except Exception:
            if debug:
                await logchannel.send("API error perhaps")
            pass
        #username = parse_json_apidata_mojang['name']
        username = username_list[index]
        if debug: print(online_status, username, online_list[index])
        channel = client.get_channel(mainchannel)
        logchannel = client.get_channel(loggingchannel)
        current_time = int(time.time())
        if online_status:
            statusname = "ONLINE :green_square:"
            online_status = 'True'
        if not online_status:
            statusname = "OFFLINE :red_square:"
            online_status = 'False'
        if online_status != online_list[index]:
            await channel.send(username + " has been " + statusname + " since <t:" + str(current_time) + ":R>")
            online_list[index] = online_status
            if online_status == 'True':
                gamers.append(username)
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
