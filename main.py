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
@bot.event
async def on_ready():
    logchannel = bot.get_channel(loggingchannel)
    await logchannel.send("STARTED")
    await bot.sync_commands()
    await logchannel.edit(content="")
    bot.load_extension("status")
    bot.load_extension("info")
    bot.load_extension("fortnitewins")
    bot.load_extension("playtime")
    bot.load_extension("housekeeping")
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



@bot.slash_command(description="Start the mayor channel")
async def mayorchannelstart(ctx):
    global mayorchannelid
    mayorchannelid1 = bot.get_channel(mayorchannelid)
    parse_mayorapi = mayorapi()
    lastupdated = parse_mayorapi['lastUpdated']
    if mayorchannel.is_running():
        await ctx.respond("The mayor channel loop is currently running!")
    elif not mayorchannel.is_running():
        await ctx.respond("Done!")
        await mayorchannel.start()
mayorruncount = 0

@tasks.loop(minutes=15)
async def mayorchannel():
    parse_mayorapi = mayorapi()
    global mayorchannelid
    global mayorruncount
    mayorchannelid1 = bot.get_channel(mayorchannelid)
    lastupdated = parse_mayorapi['lastUpdated']
    if mayorruncount == 0:
        embed = discord.Embed(title="The current mayor is: "+ parse_mayorapi['mayor']['name'] + "(" + parse_mayorapi['mayor']['key'] + ")",
        color=discord.Color.dark_gold())
        currentmayor_perks = parse_mayorapi['mayor']['perks']
        embed.add_field(name="Perks",
        value="",
        inline=False)
        for index, aa in enumerate(currentmayor_perks):
            perks = parse_mayorapi['mayor']['perks'][index]['description']
            perks = perks.replace("§a","")
            perks = perks.replace("§7","")
            perks = perks.replace("§9","")
            perks = perks.replace("§e","")
            perks = perks.replace("§5","")
            embed.add_field(name=parse_mayorapi['mayor']['perks'][index]['name'],
            value=perks,
            inline=True)
        lastupdated = str(lastupdated)[:-3]
        embed.add_field(name="Last Updated",
        value="<t:"+ str(lastupdated) + ":R>",
        inline=False)
        print(mayorruncount)
        mayorruncount =+ 1
        print(mayorruncount)
        await mayorchannelid1.send(embed=embed)
        global lastmessage
        lastmessage = bot.get_message(mayorchannelid1.last_message_id)
    if mayorruncount > 0:
        embed = discord.Embed(title="The current mayor is: "+ parse_mayorapi['mayor']['name'] + "(" + parse_mayorapi['mayor']['key'] + ")",
        color=discord.Color.dark_gold())
        currentmayor_perks = parse_mayorapi['mayor']['perks']
        embed.add_field(name="Perks",
        value="",
        inline=False)
        for index, aa in enumerate(currentmayor_perks):
            perks = parse_mayorapi['mayor']['perks'][index]['description']
            perks = perks.replace("§a","")
            perks = perks.replace("§7","")
            perks = perks.replace("§9","")
            perks = perks.replace("§e","")
            perks = perks.replace("§5","")
            embed.add_field(name=parse_mayorapi['mayor']['perks'][index]['name'],
            value=perks,
            inline=True)
        lastupdated = str(lastupdated)[:-3]
        embed.add_field(name="Last Updated",
        value="<t:"+ str(lastupdated) + ":R>",
        inline=False)
        graphurl = mayorgraphing()
        embed.set_image(url=graphurl)
        mayorruncount =+ 1
        await lastmessage.edit(embed=embed)

bot.run(KEY)
