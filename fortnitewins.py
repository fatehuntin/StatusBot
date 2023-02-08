from main import bot
parse_fortnite_api = fortniteapi()
wins = parse_fortnite_api['data']['stats']['all']['overall']['wins']
@tasks.loop(seconds=10)
async def fortnitewins():
    global wins
    parse_fortnite_api = fortniteapi()
    try:
        newwins = parse_fortnite_api['data']['stats']['all']['overall']['wins']
    except Exception:
        logging.error("API ERROR")
    fnchannel = bot.get_channel(fortnitechannel)
    try:
        if newwins > wins:
            await fnchannel.send("BIG W " + fortniteusername + " GOT AN EPIC VICTORY ROYALE <@&1058524479959076975> ")
            wins = newwins
    except Exception:
        print("Fuck api ig")

def setup(bot):
    print("Loading fortnitewins")