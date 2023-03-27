import asyncio
import json
import logging
import time

import discord
import requests
import uvicorn
from discord.ext import tasks, commands
from fastapi import FastAPI

from config import uuid_list, username_list, debug, api_key, KEY, mainchannel, loggingchannel, onlineemoji, \
    offlineemoji, uptime, authlist, modused, apiip
from totaltime import totaltime
from utils import timestamper, hypixelapi, mayorapi, mayorgraphing, skycryptapi_current, \
    skycryptapi_profile, findWholeWord

description = """
Status Bot
https://github.com/fatehuntin/StatusBot
"""
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(
    description=description,
    intents=intents,
)
app = FastAPI()
import nest_asyncio

nest_asyncio.apply()

if __name__ == "__main__":
    uvicorn.run("main:app", host=apiip, port=8000, log_level="debug", loop="asyncio")


@app.post("/")
def add_item(request: dict):
    if request["auth"] in authlist:
        index = uuid_list.index(request["uuid"])
        whosonline[index] = request["player"]
        verified_logins[index] = True
        return {"status": "ok", "message": "Successfully authenticated!"}
    else:
        return {"status": "ok", "message": "Authentication failed!"}


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
    newdata.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0])
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

#TODO add button under offline msg to view the progress made while the account was online
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
            online_status[index] = 'True'
            online_time = ""
        if not online_status[index]:
            statusname = "OFFLINE "
            statuscolour = discord.Color.red()
            statusemoji = offlineemoji
            online_status[index] = 'False'
            if uptime:
                online_time = timestamper(current_time - last_online[index])
            else:
                online_time = ""
        if online_status[index] != online_list[index]:
            embed = discord.Embed(title=f"{username} is now {statusname}", colour=statuscolour,
                                  url=f"https://sky.shiiyu.moe/stats/{uuid_list[index]}")
            embed.set_thumbnail(url="https://visage.surgeplay.com/head/" + str(uuid_list[index]))
            embed.add_field(name=statusemoji, value=f"They have been online since <t:{str(current_time)}:R>")
            if online_time:
                embed.add_field(name="They were online for:", value=online_time, inline=False)
            if modused[index]:
                if verified_logins[index]:
                    embed.add_field(name=f"{whosonline[index]} is now playing on {username}")
                if not verified_logins[index]:
                    await channel.send("@here")
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
        await asyncio.sleep(1)

#TODO put this in info
@bot.slash_command(description="Sends the bot's latency.")
async def ping(ctx):
    await ctx.respond(f"Pong! Latency is {int(bot.latency * 1000)}ms")


@bot.slash_command(description='Total playtime for every account')
async def stats(ctx):
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
    # seems redundant, might fix everything killing itself instantly
    if not status.is_running():
        logging.warning("STATUS STOPPED FOR SOME REASON")
        status.start()
    if not progress.is_running():
        logging.warning("progress stopped")
        progress.start()
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
    embed.add_field(name="Mayorchannel",
                    value=mayorstatus,
                    inline=False)
    await ctx.respond(embed=embed)


@bot.slash_command(description="Start the mayor channel")
async def mayorchannelstart(ctx):
    if mayorchannel.is_running():
        await ctx.respond("The mayor channel loop is currently running!")
    elif not mayorchannel.is_running():
        await ctx.respond("Done!")
        await mayorchannel.start()


mayorruncount = 0


class MyView(discord.ui.View):
    @discord.ui.button(label="View perks", style=discord.ButtonStyle.primary, emoji="❓")
    async def button_callback(self, button, interaction):
        embed = discord.Embed(title="Perks of all the mayors in the current election",
                              color=discord.Color.dark_gold())
        currentelectionperks = "HI"
        mayors = ["1", "2", "3", "4", "5"]
        canindex = int(0)
        parse_mayorapi = mayorapi()
        for x in mayors:
            embed.add_field(name=f"**{parse_mayorapi['current']['candidates'][canindex]['name']}**", value="",
                            inline=False)
            for index, aa in enumerate(parse_mayorapi['current']['candidates'][canindex]['perks']):
                perks = parse_mayorapi['current']['candidates'][canindex]['perks'][index]['description']
                perks = perks.replace("§a", "")
                perks = perks.replace("§7", "")
                perks = perks.replace("§9", "")
                perks = perks.replace("§e", "")
                perks = perks.replace("§5", "")
                perks = perks.replace("§2", "")
                perks = perks.replace("§4", "")
                perks = perks.replace("§c", "")
                perks = perks.replace("§6", "")
                perks = perks.replace("§b", "")
                perks = perks.replace("§3", "")
                perks = perks.replace("§1", "")
                perks = perks.replace("§f", "")
                perks = perks.replace("§d", "")
                perks = perks.replace("§8", "")
                perks = perks.replace("§0", "")
                perks = "• " + parse_mayorapi['current']['candidates'][canindex]['perks'][index]['name'] + "\n" + perks
                # embed.add_field(name="", value=parse_mayorapi['current']['candidates'][canindex]['perks'][index]['name'], inline=False)
                embed.add_field(name="",
                                value=perks,
                                inline=True)
            canindex = canindex + 1
        await interaction.response.send_message(embed=embed, ephemeral=True)


@tasks.loop(minutes=1)
async def mayorchannel():
    parse_mayorapi = mayorapi()
    global mayorchannelid
    global mayorruncount
    mayorchannelid1 = bot.get_channel(mayorchannelid)
    lastupdated = parse_mayorapi['lastUpdated']
    if mayorruncount == 0:
        embed = discord.Embed(
            title="The current mayor is: " + parse_mayorapi['mayor']['name'] + "(" + parse_mayorapi['mayor'][
                'key'] + ")",
            color=discord.Color.dark_gold())
        currentmayor_perks = parse_mayorapi['mayor']['perks']
        embed.add_field(name="Perks",
                        value="",
                        inline=False)
        mayorruncount = + 1
        await mayorchannelid1.send(embed=embed)
        global lastmessage
        lastmessage = bot.get_message(mayorchannelid1.last_message_id)
    if mayorruncount > 0:
        embed = discord.Embed(
            title="The current mayor is: " + parse_mayorapi['mayor']['name'] + "(" + parse_mayorapi['mayor'][
                'key'] + ")",
            color=discord.Color.dark_gold())
        if parse_mayorapi['mayor']['name'] == "Aatrox":
            currentmayorthumbnail = "https://static.wikia.nocookie.net/hypixel-skyblock/images/a/a5/Aatrox.png/revision/latest?cb=20200915234840"
        if parse_mayorapi['mayor']['name'] == "Cole":
            currentmayorthumbnail = "https://static.wikia.nocookie.net/hypixel-skyblock/images/b/b8/Cole.png/revision/latest?cb=20200921062534"
        if parse_mayorapi['mayor']['name'] == "Diana":
            currentmayorthumbnail = "https://static.wikia.nocookie.net/hypixel-skyblock/images/5/5f/Diana.png/revision/latest?cb=20200912120658"
        if parse_mayorapi['mayor']['name'] == "Diaz":
            currentmayorthumbnail = "https://static.wikia.nocookie.net/hypixel-skyblock/images/d/da/Diaz.png/revision/latest?cb=20200921063025"
        if parse_mayorapi['mayor']['name'] == "Finnegan":
            currentmayorthumbnail = "https://static.wikia.nocookie.net/hypixel-skyblock/images/8/85/Finnegan.png/revision/latest?cb=20221118161611"
        if parse_mayorapi['mayor']['name'] == "Foxy":
            currentmayorthumbnail = "https://static.wikia.nocookie.net/hypixel-skyblock/images/9/90/Foxy.png/revision/latest?cb=20200919054800"
        if parse_mayorapi['mayor']['name'] == "Marina":
            currentmayorthumbnail = "https://static.wikia.nocookie.net/hypixel-skyblock/images/9/9d/Marina.png/revision/latest?cb=20200915234253"
        if parse_mayorapi['mayor']['name'] == "Paul":
            currentmayorthumbnail = "https://static.wikia.nocookie.net/hypixel-skyblock/images/0/00/Paul.png/revision/latest?cb=20200921063037"
        if parse_mayorapi['mayor']['name'] == "Jerry":
            currentmayorthumbnail = "https://static.wikia.nocookie.net/hypixel-skyblock/images/5/58/Villager.png/revision/latest?cb=20210805125409"
        if parse_mayorapi['mayor']['name'] == "Derpy":
            currentmayorthumbnail = "https://static.wikia.nocookie.net/hypixel-skyblock/images/d/de/Derpy.png/revision/latest?cb=20210802153205"
        if parse_mayorapi['mayor']['name'] == "Scorpius":
            currentmayorthumbnail = "https://static.wikia.nocookie.net/hypixel-skyblock/images/a/af/Scorpius.png/revision/latest?cb=20201017023156"
        embed.set_thumbnail(url=currentmayorthumbnail)
        currentmayor_perks = parse_mayorapi['mayor']['perks']
        embed.add_field(name="Perks",
                        value="",
                        inline=False)
        for index, aa in enumerate(currentmayor_perks):
            perks = parse_mayorapi['mayor']['perks'][index]['description']
            perks = perks.replace("§a", "")
            perks = perks.replace("§7", "")
            perks = perks.replace("§9", "")
            perks = perks.replace("§e", "")
            perks = perks.replace("§5", "")
            perks = perks.replace("§2", "")
            perks = perks.replace("§4", "")
            perks = perks.replace("§c", "")
            perks = perks.replace("§6", "")
            perks = perks.replace("§b", "")
            perks = perks.replace("§3", "")
            perks = perks.replace("§1", "")
            perks = perks.replace("§f", "")
            perks = perks.replace("§d", "")
            perks = perks.replace("§8", "")
            perks = perks.replace("§0", "")
            embed.add_field(name=parse_mayorapi['mayor']['perks'][index]['name'],
                            value=perks,
                            inline=True)
        global nextbooth
        global nextelection
        if nextelection < int(time.time()):
            nextelection = nextelection + 446400
        if nextbooth < int(time.time()):
            nextbooth = nextbooth + 446400
        lastupdated = str(lastupdated)[:-3]
        embed.add_field(name="Next election",
                        value="<t:" + str(nextelection) + ":R>",
                        inline=False)
        embed.add_field(name="next booth open",
                        value="<t:" + str(nextbooth) + ":R>",
                        inline=False)
        embed.add_field(name="Last Updated",
                        value="<t:" + str(lastupdated) + ":R>",
                        inline=False)
        graphurl = mayorgraphing()
        embed.set_image(url=graphurl)
        mayorruncount = + 1
        await lastmessage.edit(embed=embed, view=MyView())


async def get_profile_names(ctx: discord.AutocompleteContext):
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
    chnl = bot.get_channel(str(channel))
    await ctx.respond(
        "Delete this after the embed appears \n If the embed doesnt appear something went wrong, either retry or change ur command")
    await ctx.send(embed=embed)

#TODO make sure that this runs on the correct timeframe hours=24
@tasks.loop(minutes=30)
async def progress():
    global newdata
    channel = bot.get_channel(mainchannel)
    embed = discord.Embed(
        title="Daily progress update"
    )
    names = ["Taming", "Farming", "Mining", "Combat", "Foraging", "Fishing", "Enchanting", "Alchemy", "Zombie Slayer",
             "Spider Slayer", "Wolf Slayer", "Enderman Slayer", "Blaze Slayer", "Catacombs"]
    olddata = newdata
    newdata = []
    for index, x in enumerate(uuid_list):
        embed = discord.Embed(
            title=f"Daily progress update for{username_list[index]}"
        )
        api = skycryptapi_current(uuid_list[index])[1]
        newdata.append([])
        newdata[index].append(int(api['levels']['taming']['xp']))  # 0
        newdata[index].append(int(api['levels']['farming']['xp']))  # 1
        newdata[index].append(int(api['levels']['mining']['xp']))  # 2
        newdata[index].append(int(api['levels']['combat']['xp']))  # 3
        newdata[index].append(int(api['levels']['foraging']['xp']))  # 4
        newdata[index].append(int(api['levels']['fishing']['xp']))  # 5
        newdata[index].append(int(api['levels']['enchanting']['xp']))  # 6
        newdata[index].append(int(api['levels']['alchemy']['xp']))  # 7
        newdata[index].append(int(api['slayers']['zombie']['xp']))  # 8
        newdata[index].append(int(api['slayers']['spider']['xp']))  # 9
        newdata[index].append(int(api['slayers']['wolf']['xp']))  # 10
        if api['slayers']['enderman']['level']['currentLevel'] != 0:
            newdata[index].append(int(api['slayers']['enderman']['xp']))  # 11
        if api['slayers']['blaze']['level']['currentLevel'] != 0:
            newdata[index].append(int(api['slayers']['blaze']['xp']))  # 12
        newdata[index].append(int(api['dungeons']['catacombs']['level']['xp']))  # 13
        time.sleep(10)
        for index1, y in enumerate(newdata[index]):
            if newdata[index][index1] > olddata[index][index1]:
                embed.add_field(name=names[index1], value=str(olddata[index][index1]) + "-->" + str(newdata[index][index1] - olddata[index][index1]), inline=False)

        await channel.send(embed=embed)


bot.run(KEY)
