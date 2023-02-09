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
@bot.slash_command(description='Total playtime for every account')
async def playtime(ctx):
    embed = discord.Embed(title="Stats" ,
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
            print(online_status)
        embed.add_field(name=username + statusEmoji,
                        value=lastorsince + str(last_online[index]) + ":R> \n" + onlineorno + "Total time online: " + total_time,
                        inline=False)
    embed.set_footer(text="Made by Noly")
    await ctx.respond(embed=embed)

def setup(bot):
    print("Loading playtime")
