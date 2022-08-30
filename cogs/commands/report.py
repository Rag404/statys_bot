import discord
from discord.commands import Option
from discord.ext import commands


class ReportCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.slash_command(name="report", description="Report a bug to the owner of the bot. Please do not abuse of this.")
    async def report(self, ctx, issue: Option(str, "Explain your issue", required=True)):
        owner = self.bot.get_user(576435921390403623)
        
        color = discord.Color.embed_background()
        ownerEmbed = discord.Embed(title=f"Issue report by {ctx.author}", color=color)
        ownerEmbed.add_field(name="Description", value=issue, inline=False)
        ownerEmbed.add_field(name="Author", value=f"{ctx.author}\n||{ctx.author.id}||")
        ownerEmbed.add_field(name="Guild", value=f"{ctx.guild.name}\n||{ctx.guild.id}||")
        ownerEmbed.set_thumbnail(url=ctx.author.avatar.url)

        authorEmbed = discord.Embed(title="❤ Thanks for your report", description="My owner will try to fix this issue, thank you for helping us in my developement.")
        
        await owner.send(embed=ownerEmbed)
        await ctx.respond(embed=authorEmbed, ephemeral=True)




# Add the cog when the extension is loaded
def setup(bot):
    bot.add_cog(ReportCommand(bot))
    print(' - report, ReportCommand')