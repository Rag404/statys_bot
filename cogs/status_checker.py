import discord, json
import database_reader as db
from discord.ext import commands, tasks
from datetime import datetime
from bot_config import guild_ids

# time of the last iteration
global lastIteration
lastIteration = datetime.utcnow()


class StatusChecker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Loop to check every 5min
    global checkLoop
    @tasks.loop(minutes=5)
    async def checkLoop(self):
        global lastIteration
        lastIteration = datetime.utcnow()  # update the time of the last iteration

        # For each guild the bot is in
        for guild in self.bot.guilds:
            supporterID, excludedIDs = db.record('SELECT supporter_id, excluded_ids FROM guilds WHERE guild_id = ?', guild.id)
            excludedIDs = list(map(int, excludedIDs.split(', ')))
            
            supporterRole = guild.get_role(supporterID)  # Get the supporter role of the server
            excludedRoles = [guild.get_role(roleID) for roleID in excludedIDs]

            if not supporterRole:  # If the guild has no supporter role, skip this guild
                continue

            # Get all the invite codes on the sevrer
            codes = [i.code for i in await guild.invites()]

            # Function to get the custom activity of a member
            def getCustomActivity(activities):
                # For each activities the member is doing
                for activity in activities:
                    # If the activity currently checked is the custom activity, returns it
                    if isinstance(activity, discord.CustomActivity):
                        return activity.name
                # If the member has no custom activity return None
                return None


            # For each member in the server
            for member in guild.members:
                activity = getCustomActivity(member.activities)  # Get the custom activity of the member
                
                roles = member.roles  # Get the role list of the member

                if any([role in roles for role in excludedRoles]):  # If the member has any of the excluded roles on the guild, skip this member
                    continue

                # If the code with ".gg/" is found in the activity of the member, and if he doesn't have the supporter role, give it to him
                if activity and any(f".gg/{code}" in activity for code in codes):
                    if supporterRole not in roles:
                        await member.add_roles(supporterRole)
                        print("Supporter role given to", member)
                    continue
                # If the member has't the code in his activity and have the the supporter role, remove it from him
                elif supporterRole in roles:
                    await member.remove_roles(supporterRole)
                    print("Supporter role removed from", member)


    # Start the loop when the cog is loaded
    @commands.Cog.listener()
    async def on_ready(self):
        checkLoop.start(self)


# Add the cog when the extension is loaded
def setup(bot):
    bot.add_cog(StatusChecker(bot))
    print(' - status_checker, StatusChecker')

# End the loop when the extension is unloaded
def teardown(bot):
    checkLoop.cancel()