import discord
from discord.ext import commands
from cogs.commands import config, infos, server_infos
from bot_config import guild_ids


class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.slash_command(name="help", description="Shows the Help Menu.")
    async def help(self, ctx):
        embed = discord.Embed(title="🔎 Help Menu", description="*Click on a button bellow to get you to the menu of a command.*\n\n", color=discord.Color.embed_background())
        embed.description += "**/config** - Configure me for your server.\n"
        embed.description += "**/infos** - Get plenty of infos about me.\n"
        embed.description += "**/server-infos** - Shows informations about this server\n"
        embed.description += "**/help** - Shows this menu.\n"

        bot = self

        class ToConfigButton(discord.ui.Button):
            def __init__(self):
                super().__init__(label="Config", emoji="🛠")

            async def callback(self, interaction):
                await config.ConfigCommand.configCommand(bot, ctx)
        

        class ToInfosButton(discord.ui.Button):
            def __init__(self):
                super().__init__(label="Infos", emoji="💡")

            async def callback(self, interaction):
                await infos.InfoCommand.infos(bot, ctx)
        

        class ToServerInfosButton(discord.ui.Button):
            def __init__(self):
                super().__init__(label="Server infos", emoji="💡")

            async def callback(bot, interaction):
                await server_infos.ServerCommand.serverInfos(bot, ctx)
        

        class ExitButton(discord.ui.Button):
            def __init__(self):
                super().__init__(label="Exit", style=discord.ButtonStyle.red)

            async def callback(self, interaction):
                await interaction.message.delete()
        
    
        class HelpView(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.add_item(ToConfigButton())
                self.add_item(ToInfosButton())
                self.add_item(ToServerInfosButton())
                self.add_item(ExitButton())
        

        await ctx.respond(embed=embed, view=HelpView())


# Add the cog when the extension is loaded
def setup(bot):
    bot.add_cog(HelpCommand(bot))
    print(' - commands.help, HelpCommand')