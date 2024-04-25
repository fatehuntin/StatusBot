import asyncio
import json
import logging
import time
import discord
import requests
from discord.ext import tasks, commands
from config import uuid_list, username_list, debug, api_key, KEY, mainchannel, loggingchannel, onlineemoji, \
    offlineemoji, uptime, authlist, apiip
from totaltime import totaltime
from utils import timestamper, hypixelapi, mayorapi, mayorgraphing, skycryptapi_current, \
    skycryptapi_profile, findWholeWord, human_format

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
    logchannel = bot.get_channel(loggingchannel)
    await logchannel.send("STARTED")
    await bot.sync_commands()
    await restoremyfaithinhumanity.start()
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('-------------------------------------------------')


whosonline = []
verified_logins = []
online_list = []
online_status = []
newdata = []
olddata = []
last_online = [0, 0, 0, 0]
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
@tasks.loop(seconds=3)
async def status():
    global statusname, statuscolour, statusemoji, online_time, online_time
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
            embed = discord.Embed(title=f"{username} is now {statusname}", colour=statuscolour,
                                  url=f"https://sky.shiiyu.moe/stats/{uuid_list[index]}")
            embed.set_thumbnail(url="https://visage.surgeplay.com/head/" + str(uuid))
            embed.add_field(name=statusemoji, value=f"{lastorsince} <t:{str(current_time)}:R>")
            if online_time:
                embed.add_field(name=ballsinyamouth, value=online_time, inline=False)
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
                print("HI")
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


# TODO put this in info
@bot.slash_command(description="Sends the bot's latency.")
async def ping(ctx):
    await ctx.respond(f"Pong! Latency is {int(bot.latency * 1000)}ms")


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


@bot.slash_command(description="Tech support for the tech support loop")
async def tech_support(ctx):
    restoremyfaithinhumanity.start()
    await ctx.respond("Why did you even need to use this command smh (noly is shit at coding)")


@tasks.loop(seconds=30)
async def restoremyfaithinhumanity():
    logchannel = bot.get_channel(loggingchannel)
    # seems redundant, might fix everything killing itself instantly
    if not status.is_running():
        logging.warning("STATUS STOPPED FOR SOME REASON")
        status.start()
        with open('logs.log', 'r+') as fp:
            await logchannel.send(file=discord.File(fp, 'logs.log'))
            fp.truncate(0)
    #if not progress.is_running():
        #logging.warning("progress stopped")
        #progress.start()
        #with open('logs.log', 'r+') as fp:
           #await logchannel.send(file=discord.File(fp, 'logs.log'))
            #fp.truncate(0)
    await asyncio.sleep(30)


@bot.slash_command(description="Get statuses and general stats of the bot")
async def info(ctx):
    global skillIssue, mayorstatus, statusStatus
    if progress.is_running():
        progressstatus = "ok"
    if not progress.is_running():
        progressstatus = "I drink to keep the pain away"
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

    embed.add_field(name="Ping",
                    value=f"Latency is {int(bot.latency * 1000)}ms")
    await ctx.respond(embed=embed)




mayorruncount = 0



async def get_profile_names(ctx: discord.AutocompleteContext):
    global API_data_skycrypt_current
    player_name = ctx.options['player']
    profile_list = []
    await asyncio.sleep(1)
    try:
        API_data_skycrypt_current = requests.get('https://sky.shiiyu.moe/api/v2/profile/' + player_name)
    except Exception:
        pass
    apidata_skycrypt_current = API_data_skycrypt_current.text
    parse_json_apidata_skycrypt_current = json.loads(apidata_skycrypt_current)
    for profile in parse_json_apidata_skycrypt_current['profiles']:
        cute_name = parse_json_apidata_skycrypt_current['profiles'][profile]['cute_name']
        profile_list.append(cute_name)
    return profile_list


@bot.slash_command(description="search for an item on a profile")
async def itemsearch(ctx, item: discord.Option(str), player: discord.Option(str),
                     profile: discord.Option(str, required=False,
                                             autocomplete=discord.utils.basic_autocomplete(get_profile_names))):
    if profile:
        try:
            itemapi = skycryptapi_profile(player, profile)
            location = itemapi[0]['highest_rarity_sword']['display_name']
            await ctx.respond(location)
        except Exception:
            await ctx.respond("Api error, try again")
    else:
        # try:
        if True:
            location = "Error"
            itemapi = skycryptapi_current(player)[0]
            if findWholeWord(item)(str(itemapi)):
                location = "Item found on player but not in any normal inventories"
                if findWholeWord(item)(str(itemapi['inventory'])):
                    location = "Item is in player inventory"
                    await ctx.respond(location)
                elif findWholeWord(item)(str(itemapi['enderchest'])):
                    location = "Item is in enderchest"
                    await ctx.respond(location)
                elif findWholeWord(item)(str(itemapi['personal_vault'])):
                    location = "Item is in personal vault (What?)"
                    await ctx.respond(location)
                elif findWholeWord(item)(str(itemapi['storage'])):
                    location = "Item is in storage but cannot be found in a backpack"
                    iteration = 0
                    for x in itemapi['storage']:
                        if findWholeWord(item)(str(itemapi['storage'][iteration])):
                            location = f"Item is in backpack {iteration + 1}"
                            await ctx.respond(location)
                        iteration = iteration + 1

        # except Exception:
        # await ctx.respond("Api error, try again")


@bot.slash_command(description="Create an embed")
async def embedmaker(ctx, channel: discord.Option(str), title: discord.Option(str), color: discord.Option(int),
                     image: discord.Option(str), authorname: discord.Option(str, required=False),
                     authorimg: discord.Option(str, required=False), thumbnail: discord.Option(str, required=False),
                     texthead: discord.Option(str, required=False), text: discord.Option(str, required=False),
                     footer: discord.Option(str, required=False)):
    embed = discord.Embed(title=title,
                          color=color)
    if not authorimg:
        authorimg = "https://cdn.discordapp.com/attachments/996284607404200057/1082773804893347951/cbc20oz17dg71.png"
    if authorname:
        embed.set_author(name=authorname, icon_url=authorimg)
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    if texthead:
        embed.add_field(name=texthead,
                        value=text)
    if footer:
        embed.set_footer(text=footer)
    if image:
        embed.set_image(url=image)
    await ctx.respond(
        "Delete this after the embed appears \n If the embed doesnt appear something went wrong, either retry or change ur command")
    await ctx.send(embed=embed)

oldapi = ""
@tasks.loop(hours=24)
async def progress():
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    global newdata, oldapi, olddata
    updated = []
    for x in uuid_list:
        updated.append("False")
    channel = bot.get_channel(mainchannel)
    names = ["Taming", "Farming", "Mining", "Combat", "Foraging", "Fishing", "Enchanting", "Alchemy", "Zombie Slayer",
             "Spider Slayer", "Wolf Slayer", "Enderman Slayer", "Blaze Slayer", "Catacombs", "????", "????", "????", "????", "????"]
    olddata = newdata
    newdata = []
    while "False" in updated:
        print(updated)
        await asyncio.sleep(10)
        for daily_uuidindex, uuid in enumerate(uuid_list):
            if updated[daily_uuidindex] == "True":
                pass
            api = skycryptapi_current(uuid_list[daily_uuidindex])
            if not api:
                break
            api = api[1]
            logging.debug(api)
            send = False
            updated[daily_uuidindex] = "True"
            embed = discord.Embed(
                title=f"Daily progress update for {username_list[daily_uuidindex]}",
                url=f"https://sky.shiiyu.moe/stats{uuid_list[daily_uuidindex]}"
            )
            embed.set_thumbnail(url="https://visage.surgeplay.com/head/" + str(uuid))
            newdata.append([])
            newdata[daily_uuidindex].append(int(api['levels']['taming']['xp']))  # 0
            newdata[daily_uuidindex].append(int(api['levels']['farming']['xp']))  # 1
            newdata[daily_uuidindex].append(int(api['levels']['mining']['xp']))  # 2
            newdata[daily_uuidindex].append(int(api['levels']['combat']['xp']))  # 3
            newdata[daily_uuidindex].append(int(api['levels']['foraging']['xp']))  # 4
            newdata[daily_uuidindex].append(int(api['levels']['fishing']['xp']))  # 5
            newdata[daily_uuidindex].append(int(api['levels']['enchanting']['xp']))  # 6
            newdata[daily_uuidindex].append(int(api['levels']['alchemy']['xp']))  # 7
            newdata[daily_uuidindex].append(int(api['slayers']['zombie']['xp']))  # 8
            newdata[daily_uuidindex].append(int(api['slayers']['spider']['xp']))  # 9
            newdata[daily_uuidindex].append(int(api['slayers']['wolf']['xp']))  # 10
            if api['slayers']['enderman']['level']['currentLevel'] != 0:
                newdata[daily_uuidindex].append(int(api['slayers']['enderman']['xp']))  # 11
            if api['slayers']['blaze']['level']['currentLevel'] != 0:
                newdata[daily_uuidindex].append(int(api['slayers']['blaze']['xp']))  # 12
            newdata[daily_uuidindex].append(int(api['dungeons']['catacombs']['level']['xp']))  # 13
            await asyncio.sleep(10)
            print(username_list[daily_uuidindex])
            try:
                for index1, y in enumerate(newdata[daily_uuidindex]):
                    # print(newdata[daily_uuidindex])
                    # print(olddata[daily_uuidindex])
                    # print(y)
                    #print(index1)
                    if newdata[daily_uuidindex][index1] > olddata[daily_uuidindex][index1]:
                        send = True
                        embed.add_field(name=names[index1],
                                        value=str(human_format(olddata[daily_uuidindex][index1])) + "→" + str(
                                            human_format(newdata[daily_uuidindex][index1]) + "  +" +
                                            human_format(
                                                newdata[daily_uuidindex][index1] - olddata[daily_uuidindex][index1])),
                                        inline=False)
                if send:
                    await channel.send(embed=embed)
                else:
                    pass
            except Exception:
                pass


bot.run(KEY)
