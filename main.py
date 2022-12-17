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
        bot_status.start()
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f"We have logged in as {self.user}.")

client = discoword()
tree = app_commands.CommandTree(client)
statusNumber = [0,0]

@tasks.loop(seconds=10)
async def status():
    try:
        status_froggy = False
        status_macroalt = False
        statusNumber = [0,0]
        channel = client.get_channel(1022187717192323112)
        oldcataexp = "0"
        while True:
            # sleep time
            await asyncio.sleep(5)

            # status api stuff
            froggy_API = requests.get('https://api.hypixel.net/status?key=4a4bf834-c737-4e2d-89c8-c8506a819e7e&uuid=e23703d2-6f4e-43d7-9d17-146821c32943')
            hypixeldata_froggy = froggy_API.text
            parse_json_hypixel_froggy = json.loads(hypixeldata_froggy)
            online_status_froggy = parse_json_hypixel_froggy['session']['online']

            channel = client.get_channel(1022187717192323112)
            
            macroalt_API = requests.get('https://api.hypixel.net/status?key=4a4bf834-c737-4e2d-89c8-c8506a819e7e&uuid=25d9f9ccdfd9491e8f886a48de671510')
            hypixeldata_macroalt = macroalt_API.text
            parse_json_hypixel_macroalt = json.loads(hypixeldata_macroalt)
            online_status_macroalt = parse_json_hypixel_macroalt['session']['online']
            # get time then cut off decimal points
            current_time = int(time.time())
            # skycrypt dungeon exp api stuff
            """skycrypt_response_API = requests.get('https://sky.shiiyu.moe/api/v2/dungeons/FroggyPadi/Blueberry')
            skycryptdata = skycrypt_response_API.text
            parse_json_skycrypt = json.loads(skycryptdata)
            dungeons_exp = parse_json_skycrypt['dungeons']['catacombs']['level']['xp']
            cataexp = int(dungeons_exp)"""
            if online_status_froggy != status_froggy:
                status_froggy = online_status_froggy
                #d = datetime.datetime.now()
                #List = [d.strftime("%a") + " " + d.strftime("%b") + " " + d.strftime("%d") + " " + d.strftime("%Y"),
                #        cataexp]

                if status_froggy:
                    statusNumber[0] = 1
                    await channel.send("FroggyPadi is online since <t:" + str(current_time) + ":R>")
                    print(statusNumber)
                    #await client.change_presence(activity=discord.Game(name="FroggyPadi is Online"))
                elif not status_froggy:
                    await channel.send("FroggyPadi has been offline since <t:" + str(
                        current_time) + ":R>")
                    statusNumber[0] = 0
                    print(statusNumber)
            elif online_status_macroalt != status_macroalt:
                status_macroalt = online_status_macroalt
                if status_macroalt:
                    statusNumber[1] = 1
                    await channel.send("WeeGoJIM has been online since <t:" + str(current_time) + ":R>")
                    print(statusNumber)
                elif not status_macroalt:
                    statusNumber[1] = 0
                    await channel.send("WeeGoJIM has been offline since <t:" + str(current_time) + ":R>")
                    print(statusNumber)

                    """with open('FroggyPadi.csv', "a") as f_object:
                        writer_object = writer(f_object)
                        writer_object.writerow(List)
                        f_object.close()
                        print("wrote")
                    df = pd.read_csv('FroggyPadi.csv')
                    df = df.replace('', np.nan).replace('na', np.nan)
                    df = df.dropna()
                    second_elements = df.iloc[:, 1]
                    last_element = second_elements.iloc[-1]
                    second_to_last_element = second_elements.iloc[-2]
                    cataexpgain = last_element - second_to_last_element"""
                    
                    #await client.change_presence(activity=discord.Game(name="FroggyPadi is Offline"))
                    #make a list with the current date and the current cata experience and then append that to the csv file


    except Exception:
        pass

@tasks.loop(seconds=30)
async def bot_status():
    if statusNumber == [1,0]:
        await client.change_presence(activity=discord.Game(name="FroggyPadi is online"))
    elif statusNumber == [0,1]:
        await client.change_presence(activity=discord.Game(name="WeeGoJIM is online"))
    elif statusNumber == [0,0]:
        await client.change_presence(activity=discord.Game(name="No one is currently online"))





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
