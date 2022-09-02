from discord import Cog, Bot, ApplicationContext, Embed, Color, ButtonStyle, slash_command
from discord.ui import Button, View
from cogs.commands import config, infos, server_infos


class HelpCommand(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
    

    @slash_command(name="help", description="Shows the Help Menu.")
    async def help(self, ctx: ApplicationContext):
        embed = Embed(title="🔎 Help Menu", description="*Click on a button bellow to get you to the menu of a command.*\n\n", color=Color.embed_background())
        embed.description += "**/config** - Configure me for your server.\n"
        embed.description += "**/infos** - Get plenty of infos about me.\n"
        embed.description += "**/server-infos** - Shows informations about this server\n"
        embed.description += "**/help** - Shows this menu.\n"

        class ToConfigButton(Button):
            def __init__(self):
                super().__init__(label="Config", emoji="🛠")

            async def callback(self, interaction):
                await config.ConfigCommand.configCommand(ctx)
        

        class ToInfosButton(Button):
            def __init__(self):
                super().__init__(label="Infos", emoji="💡")

            async def callback(self, interaction):
                await infos.InfoCommand.infos(ctx)
        

        class ToServerInfosButton(Button):
            def __init__(self):
                super().__init__(label="Server infos", emoji="💡")

            async def callback(bot, interaction):
                await server_infos.ServerCommand.serverInfos(ctx)
        

        class ExitButton(Button):
            def __init__(self):
                super().__init__(label="Exit", style=ButtonStyle.red)

            async def callback(self, interaction):
                await interaction.message.delete()
        
    
        class HelpView(View):
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