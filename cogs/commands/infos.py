import discord, datetime, time
from discord.ext import commands


class InfoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.slash_command(name="infos", description="Shows some infos about the bot.")
    async def infos(self, ctx: commands.Context):
        mainEmbed = discord.Embed(color=discord.Color.embed_background())
        mainEmbed.title = "💡 Infos about me"
        mainEmbed.description = "**What is my purpose?** I am here to check every __5 minutes__ if any of the members have an invitation code for this server in their status, and i give them the role that the admins selected.\n"
        mainEmbed.description += "**What are my limitations?** Due to discord limitation, I can't check the description of a user, so if a member has a code in his description I won't be able to see it 😔\n"
        mainEmbed.description += "By the way, thank you so much for having me in your server! 🥰"

        mainEmbed.add_field(name="- My creation", value=f"I was created in February 2022 by <@!576435921390403623> a young French developer :flag_fr:")
        mainEmbed.add_field(name="- Guilds", value=f"I am currently in **{len(self.bot.guilds)} guilds**, and this is one of them!")
        mainEmbed.add_field(name="- Users", value=f"I can see **{len([user for user in self.bot.users if not user.bot])} users** and **{len([user for user in self.bot.users if user.bot])} bots** right now 🧐")
        
        from cogs.status_checker import lastIteration
        from cogs.commands.infos import startTime  # Import from here because if invoked from help menu, it can't access to startTime
        nerdEmbed = discord.Embed(color=discord.Color.embed_background())
        nerdEmbed.title = ":desktop: Stats for nerds"
        nerdEmbed.description = "Some infos that you might want to know if you're a fellow nerd 🤓\n"
        nerdEmbed.description += f"```\nlatency = {round(self.bot.latency*1000)}ms\nuptime = {datetime.timedelta(seconds=int(round(time.time()-startTime)))}\nlast activity check = {lastIteration.strftime('%H:%M:%S')} UTC\n```"


        class ToNerdButton(discord.ui.Button):
            def __init__(self):
                super().__init__(label="Stats for nerds", emoji="🖥")

            async def callback(self, interaction):
                await interaction.message.edit(embed=nerdEmbed, view=NerdView())
        

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
                self.add_item(ToNerdButton())
                self.add_item(ExitButton())
        
        class NerdView(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.add_item(BackButton())
                self.add_item(ExitButton())

        
        await ctx.respond(embed=mainEmbed, view=MainView())
    

    @commands.Cog.listener()
    async def on_ready(self):
        global startTime
        startTime = time.time()


# Add the cog when the extension is loaded
def setup(bot):
    bot.add_cog(InfoCommand(bot))
    print(' - commands.info, InfoCommand')