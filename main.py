import json
import requests
import discord
import asyncio
import time
from discord.ext import commands, tasks
from discord import app_commands
import pandas as pd
import plotly.express as px
from csv import writer
import datetime
import numpy as np


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
statusNumber = [0,0]
uuid_list = ['25d9f9ccdfd9491e8f886a48de671510', 'e23703d26f4e43d79d17146821c32943', '05ba7cd0c6f54e198717a919983ed3d6']
username_list = ['WeeGoJIM', 'FroggyPadi', 'gemstone_nuker']
online_list = ['False','False','False']
gamers = []
@tasks.loop(seconds=5)
async def status():
    for index, uuid in enumerate(uuid_list):
        API_data_hypixel = requests.get('https://api.hypixel.net/status?key=4a4bf834-c737-4e2d-89c8-c8506a819e7e&uuid='+uuid)
        #API_data_mojang = requests.get('https://api.mojang.com/user/profile/' + uuid)
        apidata_hypixel = API_data_hypixel.text
        #apidata_mojang = API_data_mojang.text
        parse_json_apidata_hypixel = json.loads(apidata_hypixel)
        #parse_json_apidata_mojang = json.loads(apidata_mojang)
        try: 
            online_status = parse_json_apidata_hypixel['session']['online']
        except Exception:
            await logchannel.send("API error perhaps")
            pass
        #username = parse_json_apidata_mojang['name']
        username = username_list[index]
        print(online_status, username, online_list[index])
        channel = client.get_channel(1022187717192323112)
        logchannel = client.get_channel(996284607404200057)
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
@tree.command(name="graph", description="send graph of cata exp")
async def self(interaction):
    df = pd.read_csv("FroggyPadi.csv")
    fig = px.line(df, x='Time', y='Experience', title='FroggyPadi catacombs experience over time')
    fig.write_image("graph.png")
    fig.write_html("graph.html")
    await interaction.response.send_message(file=discord.File('graph.png'))
    #await interaction.response.send_message(file=discord.File('graph.html'))



# only use for main
client.run('MTA0NjY5MDI4NTI3MjQzNjgxNw.GO6rch.UQURF8AwFVeyW_30gnRSmRmIGrNoRVYCOvlY-Q')
# only use for testing
#client.run('MTA0MzIxNzAxNjIyNTUzODExOQ.GG8p2U.6PxFsKzHlYH0sZzSTDfcx4ACGocvkJaFdgOwQQ')
