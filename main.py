import discord
import asyncio
import time
import logging
from discord.ext import tasks, commands
from config import uuid_list, username_list, debug, api_key, KEY, mainchannel, loggingchannel, modifier, onlineemoji, offlineemoji, uptime, fortnitechannel, fortniteusername, dmuser, mayorchannelid
from utils import timestamper, hypixelapi, fortniteapi, mayorapi, mayorgraphing
from totaltime import totaltime
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
    logchannel = bot.get_channel(loggingchannel)
    await logchannel.send("STARTED")
    await bot.sync_commands()
    await logchannel.edit(content="")
    
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

@bot.slash_command(description='Total playtime for every account')
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

@bot.slash_command(description="Tech support for the tech support loop")
async def tech_support(ctx):
    restoremyfaithinhumanity.start()
    moyai.start()
    await ctx.respond("Why did you even need to use this command smh (noly is shit at coding)")

@tasks.loop(seconds=30)
async def restoremyfaithinhumanity():
    #seems redundant, might fix everything killing itself instantly
    logchannel = bot.get_channel(loggingchannel)

    if not status.is_running():
        if not fortnitewins.is_running():
            try:
                fortnitewins.start()
                status.start()
            except Exception:
                pass
            await logchannel.send("Everything restarted, something catastrophic probably happened <@319574411579752459> \nThis can also just be the program starting")
        if fortnitewins.is_running():
            try:
                status.start()
            except Exception:
                pass
            await logchannel.send("Status restarted (Fuck api(probably))")
    if not fortnitewins.is_running():
        try:
            fortnitewins.start()
        except Exception:
            pass
        await logchannel.send("Fortnitewins restarted (it broke)")

    else:
        pass
    await asyncio.sleep(30)
@bot.slash_command(description="Get statuses and general stats of the bot")
async def info(ctx):
    if status.is_running():
        statusStatus = "Running   :green_square:"
    if not status.is_running():
        statusStatus = "Not running   :red_square:"
    if restoremyfaithinhumanity.is_running():
        skillIssue = "Running   :green_square:"
    if not restoremyfaithinhumanity.is_running():
        skillIssue = "Not running   :red_square:"
    if fortnitewins.is_running():
        fortnitestatus = "Running   :green_square:"
    if not fortnitewins.is_running():
        fortnitestatus = "Not running   :red_square:"
    if mayorchannel.is_running():
        mayorstatus = "Running   :green_square:"
    if not mayorchannel.is_running():
        mayorstatus = "Not running   :red_square:"
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
    embed.add_field(name="Fortnite Win Tracker",
    value=fortnitestatus,
    inline=False)
    embed.add_field(name="Mayorchannel",
    value=mayorstatus,
    inline=False)
    await ctx.respond(embed=embed)

@tasks.loop(hours=1)
async def moyai():
    userchnl = bot.get_channel(dmuser)
    print(dmuser)
    print(userchnl)
    await userchnl.send(":moyai:")


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
