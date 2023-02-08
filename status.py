import discord
import asyncio
import time
import logging
from discord.ext import tasks
from config import uuid_list, username_list, debug, api_key, KEY, mainchannel, loggingchannel, modifier, onlineemoji, offlineemoji, uptime
from utils import timestamper, hypixelapi
from totaltime import totaltime


@tasks.loop(seconds=3)
async def status():
    for index, uuid in enumerate(uuid_list):
        parse_json_apidata_hypixel = hypixelapi(uuid,api_key)
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
        if not parse_json_apidata_hypixel['success']:
            break
        try: 
            online_status[index] = parse_json_apidata_hypixel['session']['online']
        except Exception:
            logging.warning("API ERROR")
            await logchannel.send("API error perhaps (I want to die)" + str(parse_json_apidata_hypixel))
            online_status[index] = "Questionable variable assignment to make api drop a straight nuclear shit in my bed causing the whole program to erupt"
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
                last_online[index] = current_time
                print("writing", totaltime)
                with open('totaltime.py', 'w+') as fp:
                    fp.write("totaltime = [")
                    for x in totaltime:
                        fp.write("%s," %x)
                    fp.write("]")
                    fp.close()
            elif online_status[index] == 'False':
                gamers.remove(username)
                timeplayed = current_time-last_online[index]
                totaltime[index] = totaltime[index]+timeplayed
                with open('totaltime.py', 'w+') as fp:
                    fp.write("totaltime = [")
                    for x in totaltime:
                        fp.write("%s," %x)
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
            await bot.change_presence(activity=discord.Game(name= separator.join(gamers) + " is online")) 
        elif len(gamers) == 0:
            await bot.change_presence(activity=discord.Game(name="No one is online"))
        await asyncio.sleep(1)


def setup(bot):
    print("Loading status")