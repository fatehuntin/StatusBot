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
    offlineemoji, uptime, twotimesrole, send, dapingrole
from utils import timestamper, hypixelapi, levelsapi, usernameapi

description = """
Status Bot
https://github.com/fatehuntin/StatusBot
"""
intents = discord.Intents.default()
bot = commands.Bot(
    description=description,
    intents=intents,
    command_prefix='!',
)




pinged = False
daping = False
online_list = []
online_status = []
last_online = [0, 0, 0, 0, 0, 0]
sblevel = [0, 0, 0, 0, 0, 0]
newlvl = [0, 0, 0, 0, 0, 0]
expgained = [0, 0, 0, 0, 0, 0]
totaltime = [0, 0, 0, 0, 0, 0]
statusstarted = False
channel = bot.get_channel(mainchannel)
logchannel = bot.get_channel(loggingchannel)
for index, x in enumerate(uuid_list):
    online_list.append('False')
    online_status.append('False')
    last_online.append(int(time.time()))
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
    
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('-------------------------------------------------')
    await bot.sync_commands()
    await restoremyfaithinhumanity.start()

# TODO add button under offline msg to view the progress made while the account was online
@tasks.loop(seconds=7)
async def status():
    global statusname, statuscolour, statusemoji, online_time, sblevel, statusstarted, timeplayed
    if not statusstarted: 
        print("Loading Status...") 
        statusstarted = True
    for index, uuid in enumerate(uuid_list):
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
        if online_status[index]:
            newlvl[index] = levelsapi(uuid)
            statusname = "ONLINE "
            statuscolour = discord.Color.green()
            statusemoji = onlineemoji
            ballsinyamouth = "They were offline for:"
            online_status[index] = 'True'
            lastorsince = "They have been online since"

            if uptime:
                timeplayed = current_time - last_online[index]
                online_time = timestamper(current_time - last_online[index])
            else:
                timeplayed = current_time - last_online[index]
                online_time = ""
        if not online_status[index]:
            expgained[index] = newlvl[index] - sblevel[index]
            sblevel[index] = newlvl[index]
            statusname = "OFFLINE "
            statuscolour = discord.Color.red()
            statusemoji = offlineemoji
            lastorsince = "They have been offline since"
            ballsinyamouth = "They were online for:"
            online_status[index] = 'False'
            if uptime:
                timeplayed = current_time - last_online[index]
                online_time = timestamper(current_time - last_online[index])
            else:
                timeplayed = current_time - last_online[index]
                online_time = ""
        if online_status[index] != online_list[index]:
            embed = discord.Embed(title=f"{username} is now {statusname}", colour=statuscolour,
                                  url=f"https://sky.shiiyu.moe/stats/{uuid_list[index]}")
            embed.set_thumbnail(url="https://visage.surgeplay.com/head/" + str(uuid))
            embed.add_field(name=statusemoji, value=f"{lastorsince} <t:{str(current_time)}:R>")
            if online_time:
                embed.add_field(name=ballsinyamouth, value=online_time, inline=False)
            if expgained[index] > 0: 
                embed.add_field(name="",value=f"Skyblock exp gained: {expgained[index]}")
                expgained[index] = 0
            #print(f"expgained: {expgained}, index: {index}, newlvl{newlvl}, sblvl: {sblevel}, username: {username}{username_list[index]}")
            if send[index]: await channel.send(embed=embed)
            else: pass 
            online_list[index] = online_status[index]
            if online_status[index] == 'True':
                gamers.append(username)
                last_online[index] = current_time
            elif online_status[index] == 'False':
                gamers.remove(username)
                timeplayed = current_time - last_online[index]
                totaltime[index] = totaltime[index] + timeplayed
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
        
async def soopycommands(ctx: discord.AutocompleteContext):
    command_list = ["rtca", "sblvl", "currdungeon"]
    return command_list

@bot.slash_command(description='soopy commands')
async def soopy(ctx, command: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(soopycommands)), player: discord.Option(str, required=False) ):
    soopyapi = requests.get(f'https://soopy.dev/api/soopyv2/botcommand?m={command}&u={player}')
    asyncio.sleep(3)
    apidata_soopy = soopyapi.text
    soopyresult = json.loads(apidata_soopy)
    print(soopyresult)
    await ctx.send(soopyresult)


@bot.slash_command(description='Fix the bot')
async def fix(ctx):
    await ctx.respond("Kill yourself.")

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

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
        status.start()
        #playtime.start()
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
        if not pinged: await channel.send("2x Powder is now active in the dwarven mines " + twotimesrole)
        pinged = True
    else:
        pinged = False


@tasks.loop(seconds=20)
async def darkauction():
    global daping, dapingrole
    channel = bot.get_channel(mainchannel)
    obj = time.localtime()
    time_str = str(time.asctime(obj))
    if time_str[:-8].endswith("53"):
        if not daping: 
            await channel.send(f"{dapingrole} 2 minutes to dark acution")
            await asyncio.sleep(60)
            await channel.send(f"{dapingrole} FOOOBEL IT IS DARK AUCTION GO GET THE FUCKING THING PLEASE")
        daping = True
    else:
        daping = False


@bot.slash_command(description="2X POWDER NOTIFIER TOGGLE MEOWWW")
async def twotimes(ctx):
    global pinged
    if twotimespowder.is_running():
        twotimespowder.cancel()
        print("2x: ✗")
        pinged = False
        await ctx.respond("2x powder counter is now stopped please stop downtiming", ephemeral=True)
    elif not twotimespowder.is_running():
        twotimespowder.start()
        pinged = False
        print("2x: ✓")
        await ctx.respond("Locked in powder grinder activated", ephemeral=True)

@bot.slash_command(description="Dark auction foobel pinger")
async def daping(ctx):
    global daping
    if darkauction.is_running():
        darkauction.cancel()
        print("da: ✗")
        daping = False
        await ctx.respond("go farm famer boy", ephemeral=True)
    elif not darkauction.is_running():
        darkauction.start()
        print("da: ✓")
        daping = False
        await ctx.respond("dark auction ping turned on", ephemeral=True)

@bot.slash_command(description="Get statuses and general stats of the bot")
async def info(ctx):
    global skillIssue, mayorstatus, statusStatus, powderstatus, dastatus
    if twotimespowder.is_running():
        powderstatus = "Running   :green_square:"
    if not twotimespowder.is_running():
        powderstatus = "Not running   :red_square:"
    if darkauction.is_running():
        dastatus = "Running   :green_square:"
    if not darkauction.is_running():
        dastatus = "Not running   :red_square:"
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
                    inline=False)
    
    embed.add_field(name="Task keeper",
                    value=skillIssue,
                    inline=False)
    
    embed.add_field(name="2x Powder",
                    value=powderstatus,
                    inline=False)
    
    embed.add_field(name="Dark Auction",
                    value=dastatus,
                    inline=False)

    embed.add_field(name="Ping",
                    value=f"Latency is {int(bot.latency * 1000)}ms")
    await ctx.respond(embed=embed, ephemeral=True)


bot.run(KEY)
