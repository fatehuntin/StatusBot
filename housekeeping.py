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
@commands.command(description="Tech support for the tech support loop")
async def tech_support(ctx):
    restoremyfaithinhumanity.start()
    await ctx.respond("All functions started!")

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


def setup(bot):
    print("Loading housekeeping")
    bot.add_command(tech_support)
    print("Done!")