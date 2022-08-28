import discord
from discord.ext import commands, tasks


class BotStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Loop to change every 10min
    global loopStatus    
    @tasks.loop(minutes=10)
    async def loopStatus(self):
        newActivity = f"/help | {len(self.bot.guilds)} servers"  # Set the activity of the bot with the number of guilds
        await self.bot.change_presence(activity=discord.Streaming(name=newActivity, url="https://www.twitch.tv/ragdoll_do"))
    
    # Start the loop when the cog is loaded
    @commands.Cog.listener()
    async def on_ready(self):
        loopStatus.start(self)


# Add the cog when the extension is loaded
def setup(bot):
    bot.add_cog(BotStatus(bot))
    print(' - bot_status, BotStatus')

# End the loop when the extension is unloaded
def teardown(bot):
    loopStatus.cancel()