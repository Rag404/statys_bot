import discord
import database_reader as db
from datetime import datetime
from discord.ext import commands
from bot_config import guild_ids

from dotenv import load_dotenv
from os import getenv

intents = discord.Intents.default()
intents.presences = True
intents.members = True


client = commands.Bot(command_prefix='..', intents=intents)  # create the bot


# The extensions to load at the start of the bot
initial_extensions = [
    "status_checker",
    "bot_status",
    "commands.config",
    "commands.help",
    "commands.infos",
    "commands.server_infos",
    "commands.report"
]

print("Loading cogs...")
for extension in initial_extensions:  # Load the extensions
    client.load_extension(f"cogs.{extension}")
print("- - -")


async def sendToOwner(text, thumbnailURL=None):
    owner = client.get_user(576435921390403623)
    embed = discord.Embed(title="🔔 Notification", description=text)
    if thumbnailURL: embed.set_thumbnail(thumbnailURL)
    await owner.send(embed=embed)


@client.event
async def on_ready():
    print('We have logged in as', client.user, "in", len(client.guilds), "guilds")
    print(datetime.now().strftime('%m/%d/%Y, %H:%M:%S'), "UTC+1")  # Print the discord tag of the bot and the date when ready
    print('- - -')    


@client.event
async def on_guild_join(guild: discord.Guild):
    print("Guild joined:", guild.name, (guild.id))
    await sendToOwner(f"**📥 Guild joined**\n{guild.name} ||{guild.id}||", guild.icon.url)
    
    for channel in guild.text_channels:
        try:
            await channel.send("Hey! Use `/config` to configure me for this server")
        except Exception:
            pass
        else:
            return print(f"I said yes in #{channel.name}")
    print("I couldn't say hey...")


@client.event
async def on_guild_remove(guild: discord.Guild):
    print("Guild left:", guild.name, (guild.id))
    await sendToOwner(f"**📤 Guild left**\n{guild.name} ||{guild.id}||", guild.icon.url)



@client.command(name="shutdown")
async def shutdown_command(ctx):
    db.commit()
    await ctx.send("Shutting down...")
    await client.close()



load_dotenv()
token = getenv("TOKEN")  # Get the token from the .env file

client.run('OTIwNzIwMzMxODkzNzg4NzE1.YbodoQ.S7Ek_mU4S26-QJc42aVCQzou0T8')  # Start the bot