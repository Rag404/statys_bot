import discord, json
import database_reader as db
from discord.ext import commands
from bot_config import guild_ids


class ServerCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.slash_command(name="server-infos", description="Shows informations about this server")
    async def serverInfos(self, ctx):
        supporterID, excludedIDs = db.record('SELECT supporter_id, excluded_ids FROM guilds WHERE guild_id = ?', ctx.guild.id)
        excludedIDs = list(map(int, excludedIDs.split(', ')))
        
        supporterRole = ctx.guild.get_role(supporterID)
        excludedRolesMention = [ctx.guild.get_role(id).mention for id in excludedIDs]
        
        if supporterRole:
            supporterNumber = len([member for member in ctx.guild.members if supporterRole in member.roles and not member.bot])

            if supporterNumber > 0:
                supporterNumberText = f"There is **{supporterNumber} supporters** on this server, congratulation! 🎉"
            else:
                supporterNumberText = f"Sadly, there is **no supporters** on this server... 😭"
            
            supporterRoleText = f"The supporter role of this server is {supporterRole.mention}."

            if excludedRolesMention:
                excludedRolesText = f"I won't check the status of the members with these roles:\n {' '.join(excludedRolesMention)}"
        
        else:
            supporterNumberText = "There is no supporter role on this server so there can't be any supporter..."
            supporterRoleText = "There is no supporter role on this server. 😞"
        
        color = discord.Color.embed_background()
        mainEmbed = discord.Embed(title="ℹ Infos about this server", color=color)
        mainEmbed.add_field(name="- Number of supporters", value=supporterNumberText)
        mainEmbed.add_field(name="- Supporter role", value=supporterRoleText)
        if excludedRolesMention: mainEmbed.add_field(name="- Excluded roles", value=excludedRolesText, inline=False)
        data = {"guild_id": ctx.guild.id, "supporter_id": supporterID, "excluded_ids": excludedIDs}
        dataEmbed = discord.Embed(title="📂 Collected data", description="I need to collect some data about your server to work proprely. But don't worry, this is not sensitive data!\nI only collect the IDs of **the supporter role** and **the excluded roles** of each server.", color=color)
        dataEmbed.add_field(name="The data of your server", value=f"```json\n{json.dumps(data, indent=2)}\n```")


        class ToDataButton(discord.ui.Button):
            def __init__(self):
                super().__init__(label="Collected data", emoji="📂")

            async def callback(self, interaction):
                await interaction.message.edit(embed=dataEmbed, view=DataView())


        class BackButton(discord.ui.Button):
            def __init__(self):
                super().__init__(label="Back", emoji="<:back_arrow:940318470069960744>")

            async def callback(self, interaction):
                await interaction.message.edit(embed=mainEmbed, view=MainView())

        class ExitButton(discord.ui.Button):
            def __init__(self):
                super().__init__(label="Exit", style=discord.ButtonStyle.red)

            async def callback(self, interaction):
                await interaction.message.delete()
        

        class MainView(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.add_item(ToDataButton())
                self.add_item(ExitButton())
        
        class DataView(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.add_item(BackButton())
                self.add_item(ExitButton())


        await ctx.respond(embed=mainEmbed, view=MainView())



# Add the cog when the extension is loaded
def setup(bot):
    bot.add_cog(ServerCommand(bot))
    print(' - commands.help, HelpCommand')