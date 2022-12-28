import discord
import asyncio
import time
import logging
from discord.ext import tasks, commands
#from discord import app_commands
from config import uuid_list, username_list, debug, api_key, KEY, mainchannel, loggingchannel, modifier, onlineemoji, offlineemoji, uptime
from utils import timestamper, hypixelapi, skycryptapi, fakeapi
from totaltime import totaltime
print(totaltime)
description = """
Status Bot
https://github.com/fatehuntin/StatusBot
"""
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(
    description = description,
    intents = intents
)
@bot.event
async def on_ready():
    status.start()
    await bot.sync_commands()
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

online_list = []
online_status =[]
last_online = [0,0,0]
channel = bot.get_channel(mainchannel)
logchannel = bot.get_channel(loggingchannel)
for index, x in enumerate(uuid_list):
    online_list.append('False')
    online_status.append(False)
    last_online[index] = int(time.time())
gamers = []
current_time = int(time.time())
@tasks.loop(seconds=5)
async def status():
    for index, uuid in enumerate(uuid_list):
        parse_json_apidata_hypixel = fakeapi() #hypixelapi(uuid,api_key)
        channel = bot.get_channel(mainchannel)
        logchannel = bot.get_channel(loggingchannel)
        current_time = int(time.time())
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
            online_status[index] = parse_json_apidata_hypixel['session']['online']
        except Exception:
            logging.warning("API ERROR")
            if debug:
                await logchannel.send("API error perhaps")
            pass
        username = username_list[index]
        if debug: 
            print(online_status[index], username, online_list[index], online_list,last_online)
            logging.debug(online_status[index], online_list[index], username, last_online[index], timestamper(current_time - last_online[index]))
        if online_status[index]:
            statusname = "ONLINE " + onlineemoji
            online_status[index] = 'True'
            online_time = ""
        if not online_status[index]:
            statusname = "OFFLINE " + offlineemoji
            online_status[index] = 'False'
            if uptime:
                online_time = " They were online for: " + timestamper(current_time - last_online[index])
            else: 
                online_time = ""
        if online_status[index] != online_list[index]:
            await channel.send(modifier[index] + username + " has been " + statusname + " since <t:" + str(current_time) + ":R>" + online_time)
            online_list[index] = online_status[index]
            if online_status[index] == 'True':
                gamers.append(username)
                timeplayed = current_time-last_online[index]
                print("lastonline index" , last_online[index])
                print("timeplayed",timeplayed)
                print("totaltime index",totaltime[index])
                totaltime[index] =+ timeplayed
                last_online[index] = current_time
                with open('totaltime.py', 'w+') as fp:
                    fp.write("totaltime = [")
                    for x in totaltime:
                        fp.write("%s," %x)
                    fp.write("]")
                    fp.close()
            elif online_status[index] == 'False':
                gamers.remove(username)
                last_online[index] = current_time
                with open('totaltime.py', 'w+') as fp:
                    fp.write("totaltime = [")
                    for x in totaltime:
                        fp.write("%s," %x)
                    fp.write("]")
                    fp.close()
        else:
            pass
        if len(gamers) > 1:
            separator = ", "
            await bot.change_presence(activity=discord.Game(name=separator.join(gamers) + " are online"))
        elif len(gamers) == 1:
            separator = ", "
            await bot.change_presence(activity=discord.Game(name= separator.join(gamers) + " is online")) 
        elif len(gamers) == 0:
            await bot.change_presence(activity=discord.Game(name="No one is online"))
        await asyncio.sleep(5)
@bot.slash_command(description="Sends the bot's latency.")
async def ping(ctx):
    await ctx.respond(f"Pong! Latency is {int(bot.latency) * 1000}ms")

@bot.slash_command(description='Provides stats for a player')
async def stats(ctx):
    embed = discord.Embed(title="Stats" ,
                          description="Total playtime for each account",
                          color=discord.Color.dark_purple())
    for index, username in enumerate(username_list):
        total_time = timestamper(totaltime[index])
        current_time = int(time.time())
        if online_status[index] == 'True':
            statusEmoji = " :green_square:"
            onlineorno = "**Online**\n"
        elif online_status[index] == 'False':
            statusEmoji = " :red_square:"
            onlineorno = "**Offline**\n"
        else:
            statusEmoji = ":question:"
            onlineorno = "**SOMETHING BROKE PING NOLAN!!!!**\n"
            print(online_status)
        embed.add_field(name=username + statusEmoji,
                        value="Last online: <t:" + str(last_online[index]) + ":R> \n" + onlineorno + "Total time online: " + total_time,
                        inline=False)
    embed.set_footer(text="Made by Noly")
    await ctx.respond(embed=embed)
bot.run(KEY)
