import asyncio
import json
import logging
import os
import time
import discord
import requests
from discord.ext import tasks, commands
from config import uuid_list, username_list, debug, api_key, KEY, mainchannel, onlineemoji, \
    offlineemoji, uptime, twotimesdm, send, dapingrole, twotimesch, activerole
from utils import timestamper, hypixelapi, levelsapi

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




daping = False
online_list = []
online_status = []
last_online = []
sblevel = []
newlvl = []
expgained = []
totaltime = []
statusstarted = False
gamers = []
STATE_FILE = "status_state.json"
logging.basicConfig(
    filename="logs.log",
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG if debug else logging.WARNING,
    datefmt='%Y-%m-%d %H:%M:%S')


def load_status_state():
    try:
        with open(STATE_FILE) as state_file:
            state = json.load(state_file)
    except FileNotFoundError:
        return {}
    except (OSError, json.JSONDecodeError) as error:
        logging.warning("Could not load status state: %s", error)
        return {}
    return state.get("players", {}) if isinstance(state, dict) else {}


def save_status_state():
    state = {
        "players": {
            uuid: {
                "last_online": last_online[index],
                "experience": sblevel[index],
                "current_experience": newlvl[index],
                "online": online_status[index] == "True",
            }
            for index, uuid in enumerate(uuid_list)
        }
    }
    try:
        with open(f"{STATE_FILE}.tmp", "w") as state_file:
            json.dump(state, state_file)
        os.replace(f"{STATE_FILE}.tmp", STATE_FILE)
    except OSError as error:
        logging.warning("Could not save status state: %s", error)


saved_players = load_status_state()
for index, uuid in enumerate(uuid_list):
    saved_player = saved_players.get(uuid, {})
    is_online = saved_player.get("online") is True
    online_list.append("True" if is_online else "False")
    online_status.append("True" if is_online else "False")
    last_online.append(saved_player.get("last_online", int(time.time())))
    sblevel.append(saved_player.get("experience", 0))
    newlvl.append(saved_player.get("current_experience", 0))
    expgained.append(0)
    totaltime.append(0)
    if is_online:
        gamers.append(username_list[index])

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('-------------------------------------------------')
    await bot.sync_commands()
    await restoremyfaithinhumanity.start()

# TODO add button under offline msg to view the progress made while the account was online
@tasks.loop(seconds=5)
async def status():
    global statusname, statuscolour, statusemoji, online_time, sblevel, statusstarted, timeplayed
    if not statusstarted: 
        print("Loading Status...") 
        statusstarted = True
    for index, uuid in enumerate(uuid_list):
        parse_json_apidata_hypixel = hypixelapi(uuid, api_key)
        channel = bot.get_channel(mainchannel)
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
            save_status_state()
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
                if debug: print("last_online[index]", last_online[index])
                if last_online[index] == 0: online_time = "The bot just started please ignore this"
                else: online_time = timestamper(current_time - last_online[index])
            else:
                timeplayed = current_time - last_online[index]
                online_time = ""
        if online_status[index] != online_list[index]:
            if online_status[index] == 'True':
                gamers.append(username)
            else:
                gamers.remove(username)
                totaltime[index] = totaltime[index] + current_time - last_online[index]
            last_online[index] = current_time
            online_list[index] = online_status[index]
            save_status_state()

            embed = discord.Embed(title=f"{username} is now {statusname}", colour=statuscolour,
                                  url=f"https://sky.shiiyu.moe/stats/{uuid_list[index]}")
            embed.set_thumbnail(url="https://visage.surgeplay.com/head/" + str(uuid))
            embed.add_field(name=statusemoji, value=f"{lastorsince} <t:{str(current_time)}:R>")
            if online_time:
                embed.add_field(name=ballsinyamouth, value=online_time, inline=False)
            if expgained[index] > 0: 
                embed.add_field(name="",value=f"Skyblock exp gained: {expgained[index]}")
                expgained[index] = 0
            if debug: print(f"expgained: {expgained}, index: {index}, newlvl{newlvl}, sblvl: {sblevel}, username: {username}{username_list[index]}")
            if send[index]: await channel.send(embed=embed)
            else: pass 
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
async def mines2x():
    global dmpinged
    channel = bot.get_channel(mainchannel)
    url = "https://soopy.dev/api/soopyv2/botcommand?m=chevents%20mines"
    text = requests.get(url).text
    if "DOUBLE_POWDER" in text:
        if not dmpinged: await channel.send("2x Powder is now active in the dwarven mines " + twotimesdm)
        dmpinged = True
    else:
        dmpinged = False


@tasks.loop(minutes=1)
async def dwarvenevent():
    global activepinged
    channel = bot.get_channel(mainchannel)
    url = "https://soopy.dev/api/soopyv2/botcommand?m=chevents%20mines"
    text = requests.get(url).text
    if "RAFFLE" in text:
        if activepinged != 1 : await channel.send("Raffle " + activerole)
        activepinged = 1
    elif "GOBLIN_RAID" in text:
        if activepinged != 2 : await channel.send("Goblin Raid " + activerole)
        activepinged = 2
    elif "MITHRIL_GOURMAND" in text: 
        if activepinged != 3 : await channel.send("Mithril Grourmand " + activerole)
        activepinged = 3
    else:
        activepinged = 0

@bot.slash_command(description="THIS DOES NOT WORK")
async def active(ctx):
    global activepinged
    if dwarvenevent.is_running():
        dwarvenevent.cancel()
        if debug: print("Active Events: ✗")
        activepinged = False
        await ctx.respond("Buh bye", ephemeral=True)
    elif not hollows2x.is_running():
        dwarvenevent.start()
        activepinged = False
        if debug: print("Active Events: ✓")
        await ctx.respond("Active events will now be pinged", ephemeral=True)


@tasks.loop(minutes=1)
async def hollows2x():
    global chpinged
    channel = bot.get_channel(mainchannel)
    url = "https://soopy.dev/api/soopyv2/botcommand?m=chevents"
    text = requests.get(url).text
    if "DOUBLE_POWDER" in text:
        if not chpinged: await channel.send("2x Powder is now active in the crystal hollows " + twotimesch)
        chpinged = True
    else:
        chpinged = False


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
async def dwarven(ctx):
    global dmpinged
    if mines2x.is_running():
        mines2x.cancel()
        if debug: print("2x dm: ✗")
        dmpinged = False
        await ctx.respond("2x powder counter is now stopped please stop downtiming", ephemeral=True)
    elif not mines2x.is_running():
        mines2x.start()
        dmpinged = False
        if debug: print("2x dm: ✓")
        await ctx.respond("Locked in powder grinder activated", ephemeral=True)

@bot.slash_command(description="2X POWDER NOTIFIER TOGGLE MEOWWW")
async def hollows(ctx):
    global chpinged
    if hollows2x.is_running():
        hollows2x.cancel()
        if debug: print("2x ch: ✗")
        chpinged = False
        await ctx.respond("2x powder counter is now stopped please stop downtiming", ephemeral=True)
    elif not hollows2x.is_running():
        hollows2x.start()
        chpinged = False
        if debug: print("2x ch: ✓")
        await ctx.respond("Locked in powder grinder activated", ephemeral=True)

@bot.slash_command(description="Dark auction foobel pinger")
async def daping(ctx):
    global daping
    if darkauction.is_running():
        darkauction.cancel()
        if debug: print("da: ✗")
        daping = False
        await ctx.respond("go farm famer boy", ephemeral=True)
    elif not darkauction.is_running():
        darkauction.start()
        if debug: print("da: ✓")
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
