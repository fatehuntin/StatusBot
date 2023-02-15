from discord.ext import tasks, commands, bridge
import discord

description = """
Status Bot
https://github.com/fatehuntin/StatusBot
"""
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = bridge.Bot(
    command_prefix= "~",
    description = description,
    intents = intents,
)
@bot.bridge_command(description="Get statuses and general info of the bot")
async def info(ctx):
    print("Balls")
    """if status.is_running():
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
    embed.add_field(name="Ping",
    value="{int(bot.latency * 1000)}ms",
    inline=False)
    await ctx.respond(embed=embed)"""
    
def setup(bot):
    print("Loading info")
    bot.add_command("info")