from discord.ext import tasks, commands
import discord

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


def setup(bot):
    print("Loading mayorchannel")