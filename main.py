try:
    import os
    os.chdir("./statys_bot")
except:
    pass


from discord import Guild, Intents
from discord.ext import commands
from data.bot_config import EXTENSIONS
from data.my_utils import log, send_to_owner
from datetime import datetime
from dotenv import load_dotenv
from os import getenv


intents = Intents.default()
intents.presences = True
intents.members = True

client = commands.Bot(intents=intents)  # create the bot


print("Loading cogs...")
for extension in EXTENSIONS:  # Load the extensions
    client.load_extension(f"cogs.{extension}")
print("- - -")


@client.event
async def on_ready():
    print('We have logged in as', client.user, "in", len(client.guilds), "guilds")
    print(datetime.now().strftime('%m/%d/%Y, %H:%M:%S'), "UTC+1")  # Print the discord tag of the bot and the date when ready
    print('- - -')    


@client.event
async def on_guild_join(guild: Guild):
    log("Guild joined:", guild.name, (guild.id))
    await send_to_owner(client, f"**📥 Guild joined**\n{guild.name} ||{guild.id}||", guild.icon.url)
    
    for channel in guild.text_channels:
        try:
            await channel.send("Hey! Use `/config` to configure me for this server")
        except Exception:
            pass
        else:
            return print(f"I said 'hey' in #{channel.name}")
    print("I couldn't say 'hey'...")


@client.event
async def on_guild_remove(guild: Guild):
    log("Guild left:", guild.name, (guild.id))
    await send_to_owner(client, f"**📤 Guild left**\n{guild.name} ||{guild.id}||", guild.icon.url)



load_dotenv()
token = getenv("TOKEN")  # Get the token from the .env file
client.run(token)  # Start the bot