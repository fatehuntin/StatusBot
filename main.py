import asyncio
import json
import logging
import time
import discord
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from discord.ext import tasks, commands
from config import uuid_list, username_list, debug, api_key, KEY, mainchannel, loggingchannel, onlineemoji, \
    offlineemoji, uptime, twotimesuser
from totaltime import totaltime
from utils import timestamper, hypixelapi, levelsapi

description = """
Status Bot
https://github.com/fatehuntin/StatusBot
"""
intents = discord.Intents.default()
bot = commands.Bot(
    description=description,
    intents=intents,
)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('-------------------------------------------------')
    logchannel = bot.get_channel(loggingchannel)
    await logchannel.send("STARTED")
    await bot.sync_commands()
    await restoremyfaithinhumanity.start()

pinged = False
whosonline = []
verified_logins = []
online_list = []
online_status = []
newdata = []
olddata = []
last_online = [0, 0, 0, 0]
level = [0, 0, 0, 0]
channel = bot.get_channel(mainchannel)
logchannel = bot.get_channel(loggingchannel)
nextelection = 1677338100
nextbooth = 1677449700
for index, x in enumerate(uuid_list):
    online_list.append('False')
    online_status.append('False')
    whosonline.append('')
    verified_logins.append(False)
    last_online.append(int(time.time()))
    newdata.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
gamers = []
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


# TODO add button under offline msg to view the progress made while the account was online
@tasks.loop(seconds=10)
async def status():
    global statusname, statuscolour, statusemoji, online_time, online_time, level
    for index, uuid in enumerate(uuid_list):
        expgained = levelsapi(uuid) - level[index]
        parse_json_apidata_hypixel = hypixelapi(uuid, api_key)
        channel = bot.get_channel(mainchannel)
        logchannel = bot.get_channel(loggingchannel)
        current_time = int(time.time())
        if not parse_json_apidata_hypixel['success']:
            break
        try:
            online_status[index] = parse_json_apidata_hypixel['session']['online']
        except Exception:
            logging.warning("API ERROR")
            online_status[
                index] = "Questionable variable assignment to make api drop a straight nuclear shit in my bed causing the whole program to erupt"
            pass
        username = username_list[index]
        if debug:
            print(online_status[index], username, online_list[index], online_list, last_online)
            logging.debug(online_status[index], online_list[index], username, last_online[index],
                          timestamper(current_time - last_online[index]))
        if online_status[index]:
            statusname = "ONLINE "
            statuscolour = discord.Color.green()
            statusemoji = onlineemoji
            ballsinyamouth = "They were offline for:"
            online_status[index] = 'True'
            lastorsince = "They have been online since"
            if uptime:
                online_time = timestamper(current_time - last_online[index])
            else:
                online_time = ""
        if not online_status[index]:
            statusname = "OFFLINE "
            statuscolour = discord.Color.red()
            statusemoji = offlineemoji
            lastorsince = "They have been offline since"
            ballsinyamouth = "They were online for:"
            online_status[index] = 'False'
            if uptime:
                online_time = timestamper(current_time - last_online[index])
            else:
                online_time = ""
        if online_status[index] != online_list[index]:
            level[index] = levelsapi(uuid)
            embed = discord.Embed(title=f"{username} is now {statusname}", colour=statuscolour,
                                  url=f"https://sky.shiiyu.moe/stats/{uuid_list[index]}")
            embed.set_thumbnail(url="https://visage.surgeplay.com/head/" + str(uuid))
            embed.add_field(name=statusemoji, value=f"{lastorsince} <t:{str(current_time)}:R>")
            if online_time:
                embed.add_field(name=ballsinyamouth, value=online_time, inline=False)
            if expgained > 0: embed.add_field(name="",value=f"Skyblock exp gained: {expgained}")
            await channel.send(embed=embed)
            online_list[index] = online_status[index]
            if online_status[index] == 'True':
                gamers.append(username)
                last_online[index] = current_time
                with open('totaltime.py', 'w+') as fp:
                    fp.write("totaltime = [")
                    for x in totaltime:
                        fp.write("%s," % x)
                    fp.write("]")
                    fp.close()
            elif online_status[index] == 'False':
                gamers.remove(username)
                timeplayed = current_time - last_online[index]
                totaltime[index] = totaltime[index] + timeplayed
                with open('totaltime.py', 'w+') as fp:
                    fp.write("totaltime = [")
                    for x in totaltime:
                        fp.write("%s," % x)
                    fp.write("]")
                    fp.close()
                last_online[index] = current_time
        else:
            pass
        if len(gamers) > 1:
            separator = ", "
            await bot.change_presence(activity=discord.Game(name=separator.join(gamers) + " are online"))
        elif len(gamers) == 1:
            separator = ", "
            await bot.change_presence(activity=discord.Game(name=separator.join(gamers) + " is online"))
        elif len(gamers) == 0:
            await bot.change_presence(activity=discord.Game(name="No one is online"))
        await asyncio.sleep(2)


@bot.slash_command(description='Total playtime for every account')
async def stats(ctx):
    global lastorsince
    embed = discord.Embed(title="Stats",
                          description="Total playtime for each account",
                          color=discord.Color.dark_purple())
    for index, username in enumerate(username_list):
        total_time = timestamper(totaltime[index])
        current_time = int(time.time())
        if online_status[index] == 'True':
            statusEmoji = " :green_square:"
            onlineorno = "**Online**\n"
            lastorsince = "Online since: <t:"
        elif online_status[index] == 'False':
            statusEmoji = " :red_square:"
            onlineorno = "**Offline**\n"
            lastorsince = "Last online: <t:"
        else:
            statusEmoji = ":question:"
            onlineorno = "**SOMETHING BROKE PING NOLAN!!!!**\n"
        embed.add_field(name=username + statusEmoji,
                        value=lastorsince + str(
                            last_online[index]) + ":R> \n" + onlineorno + "Total time online: " + total_time,
                        inline=False)
    embed.set_footer(text="Made by Noly")
    await ctx.respond(embed=embed)


@tasks.loop(seconds=30)
async def restoremyfaithinhumanity():
    if not status.is_running():
        logging.warning("STATUS STOPPED FOR SOME REASON")
        status.start()
        with open('logs.log', 'r+') as fp:
            fp.truncate(0)
    await asyncio.sleep(30)


@tasks.loop(minutes=1)
async def twotimespowder():
    global pinged
    channel = bot.get_channel(mainchannel)
    url = "https://soopy.dev/api/soopyv2/botcommand?m=chevents%20mines"
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")
    text = soup.get_text()
    if "DOUBLE_POWDER" in text:
        if not pinged: await channel.send("2x Powder is now active in the dwarven mines <@" + twotimesuser + ">")
        pinged = True
    else:
        pinged = False

@bot.slash_command(description="2X POWDER NOTIFIER TOGGLE MEOWWW")
async def twotimes(ctx):
    global pinged
    if twotimespowder.is_running():
        twotimespowder.cancel()
        pinged = False
        await ctx.respond("2x powder counter is now stopped please stop downtiming")
    elif not twotimespowder.is_running():
        twotimespowder.start()
        pinged = False
        await ctx.respond("Locked in powder grinder activated")

@bot.slash_command(description="Get statuses and general stats of the bot")
async def info(ctx):
    global skillIssue, mayorstatus, statusStatus, powderstatus
    if twotimespowder.is_running():
        powderstatus = "Running   :green_square:"
    if not twotimespowder.is_running():
        powderstatus = "Not running   :red_square:"
    if status.is_running():
        statusStatus = "Running   :green_square:"
    if not status.is_running():
        statusStatus = "Not running   :red_square:"
    if restoremyfaithinhumanity.is_running():
        skillIssue = "Running   :green_square:"
    if not restoremyfaithinhumanity.is_running():
        skillIssue = "Not running   :red_square:"
    embed = discord.Embed(title="Info",
                          color=discord.Color.dark_purple()
                          )
    embed.add_field(name="Status",

                    value=statusStatus,
                    inline=False
                    )
    embed.add_field(name="Task keeper",
                    value=skillIssue,
                    inline=False)
    embed.add_field(name="2x Powder",
                    value=powderstatus,
                    inline=False)

    embed.add_field(name="Ping",
                    value=f"Latency is {int(bot.latency * 1000)}ms")
    await ctx.respond(embed=embed)


bot.run(KEY)
