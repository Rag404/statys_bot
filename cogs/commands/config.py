import discord
import database_reader as db
from discord.ext import commands
from bot_config import guild_ids

color = discord.Color.embed_background()
missingPermEmbed = discord.Embed(title="⛔ Missing permissions", description="You need the Administrator permissions to use this command! 😢", color=color)


class ConfigCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.slash_command(name="config", description="Admins only. Configure the bot for your server.", guild_ids=guild_ids)
    async def configCommand(self, ctx: commands.Context):
        # If the user who invoked the command is not admin, send him an embed
        if not ctx.author.guild_permissions.administrator:
            return await ctx.respond(embed=missingPermEmbed, ephemeral=True)
        
        # Create a function to check if the user who interact is an admin
        async def isMissingPerm(interaction: discord.Interaction):
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message(embed=missingPermEmbed, ephemeral=True)  # If not, send a embed to inform the user
                return True
            return False

        mainEmbed = discord.Embed(title=":gear: Config Statys for your server", description="Select an option in the buttons bellow.", color=color)
        selectRoleEmbed = discord.Embed(title="🎭 Select a role", description="**Select the role that will be given to the supporters.**", color=color)
        excludeEmbed = discord.Embed(title="❌ Exclude roles", description="**The satus of the members with the selected roles won't be checked.**\n\n*Note: If one of the selected roles is also the role given to supporters, the members will never lose this role after getting it.*", color=color)

        class SelectRoleButton(discord.ui.Button):
            def __init__(self):
                super().__init__(label="Role", emoji="🎭")

            async def callback(self, interaction: discord.Interaction):
                if await isMissingPerm(interaction): return
                await interaction.message.edit(embed=selectRoleEmbed, view=SelectRoleView())  # Edit the message to display the role selection menu
        

        class SelectRoleDropdown(discord.ui.Select):            
            def __init__(self):
                options = [discord.SelectOption(label="Do not give a role", emoji="🚫", value=0, default=True)]
                current_role_id = db.field('SELECT supporter_id FROM guilds WHERE guild_id = ?', ctx.guild.id)

                count = 0
                for role in ctx.guild.roles:
                    if role.is_default() or role.managed: continue
                    count += 1
                    if count > 24: break  # There already is the "no role" options so there is only 24 options left for roles, not 25
                    options.append(discord.SelectOption(label=role.name, value=role.id, emoji="<:mention:940318470002835477>"))
                    if current_role_id == role.id:
                        options[-1].default = True
                        options[0].default = False

                super().__init__(options=options)

            async def callback(self, interaction: discord.Interaction):
                if await isMissingPerm(interaction): return
                new_role_id = int(self.values[0])
                db.execute('UPDATE guilds SET supporter_id = ? WHERE guild_id = ?', new_role_id, interaction.guild.id)
        

        class ExcludeButton(discord.ui.Button):
            def __init__(self):
                super().__init__(label="Exclude", emoji="❌")
                
            async def callback(self, interaction):
                if await isMissingPerm(interaction): return
                await interaction.message.edit(embed=excludeEmbed, view=ExcludeView())
        

        class ExcludeDropdown(discord.ui.Select):
            def __init__(self):
                options = []

                excludedIDs = db.field('SELECT excluded_ids FROM guilds WHERE guild_id = ?', ctx.guild.id)
                excludedIDs = list(map(int, excludedIDs.split(', ')))

                count = 0
                for count, role in enumerate(ctx.guild.roles):
                    if role.is_default(): continue
                    count += 1
                    if count > 25: break
                    options.append(discord.SelectOption(label=role.name, value=role.id, emoji="<:mention:940318470002835477>"))
                    if role.id in excludedIDs:
                        options[-1].default = True

                super().__init__(options=options, placeholder="Select roles or Leave empty", min_values=0, max_values=len(options))

            async def callback(self, interaction):
                if await isMissingPerm(interaction): return

                new_excludedIDs = ', '.join(self.values)
                db.execute('UPDATE guilds SET excluded_ids = ? WHERE guild_id = ?', new_excludedIDs, interaction.guild.id)


        class BackButton(discord.ui.Button):
            def __init__(self):
                super().__init__(label="Back", emoji="<:back_arrow:940318470069960744>", row=4)

            async def callback(self, interaction):
                if await isMissingPerm(interaction): return
                await interaction.message.edit(embed=mainEmbed, view=MainView())
        

        class ExitButton(discord.ui.Button):
            def __init__(self, row=4):
                super().__init__(label="Exit", style=discord.ButtonStyle.red, row=row)

            async def callback(self, interaction):
                if await isMissingPerm(interaction): return
                await interaction.message.delete()


        class MainView(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.add_item(SelectRoleButton())
                self.add_item(ExcludeButton())
                self.add_item(ExitButton(row=0))

        class SelectRoleView(discord.ui.View):
            def __init__(self):
                super().__init__()

                if len(ctx.guild.roles) > 24:
                    selectRoleEmbed.description += "\n\n⚠ Your server seems to have more roles than the menu can handle. Use `/set-supporter` instead if you don't see the role you want in the dropdown."
                        
                self.add_item(SelectRoleDropdown())
                self.add_item(BackButton())
                self.add_item(ExitButton())
        
        class ExcludeView(discord.ui.View):
            def __init__(self):
                super().__init__()
                
                if len(ctx.guild.roles) > 25:
                    selectRoleEmbed.description += "\n\n⚠ Your server seems to have more roles than the menu can handle. Use `/add-excluded` and `/remove-excluded` instead if you don't see the roles you want in the dropdown."

                self.add_item(ExcludeDropdown())
                self.add_item(BackButton())
                self.add_item(ExitButton())


        await ctx.respond(embed=mainEmbed, view=MainView())
    


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        db.execute('INSERT INTO guilds (guild_id, supporter_id, excluded_ids) VALUES (?, ?, ?)', guild.id, 0, "0")
    

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        db.execute('DELETE FROM guilds WHERE guild_id = ?', guild.id)
    

    @commands.Cog.listener()
    async def on_ready(self):
        # Check if all the guilds are registered in the data
        for guild in self.bot.guilds:
            guild_data = db.record('SELECT * FROM guilds WHERE guild_id = ?', guild.id)
            if not guild_data:
                db.execute('INSERT INTO guilds (guild_id, supporter_id, excluded_ids) VALUES (?, ?, ?)', guild.id, 0, "0")
    

    @commands.Cog.listener()
    async def is_closed(self):
        db.commit()
    


    @commands.slash_command(name="set-supporter", description="Admins only. Set the supporter role for this server.", guild_ids=guild_ids)
    async def set_supporter(self, ctx, role: discord.Option(discord.Role, "Select a role", required=True)):
        if not ctx.author.guild_permissions.administrator:
            return await ctx.respond(embed=missingPermEmbed, ephemeral=True)
        
        if role.is_default():
            embed = discord.Embed(title="⚠ Oops!", description="I'm sorry but you cannot select this role as it is the **default role**.", color=color)
            return await ctx.respond(embed=embed, ephemeral=True)
        
        if role.managed:
            embed = discord.Embed(title="⚠ Oops!", description="I'm sorry but you cannot select this role as it is **managed by an integration**.", color=color)
            return await ctx.respond(embed=embed, ephemeral=True)
        
        botMember = ctx.guild.get_member(self.bot.user.id)
        if role >= botMember.roles[0]:
            embed = discord.Embed(title="⚠ Oops!", description="I'm sorry but can't manage this role as it is **higher than my highest role**.", color=color)
            return await ctx.respond(embed=embed, ephemeral=True)

        db.execute('UPDATE guilds SET supporter_id = ? WHERE guild_id = ?', role.id, ctx.guild.id)
        
        embed = discord.Embed(title="✅ Supporter role selected", description=f"The supporter role has been set to {role.mention}", color=color)
        await ctx.respond(embed=embed, ephemeral=True)
    


    @commands.slash_command(name="add-excluded", description="Admins only. Set the roles I won't check on this server.", guild_ids=guild_ids)
    async def add_excluded(self, ctx, role: discord.Option(discord.Role, "Select a role", required=True)):
        if not ctx.author.guild_permissions.administrator:
            return await ctx.respond(embed=missingPermEmbed, ephemeral=True)
        
        if role.is_default():
            embed = discord.Embed(title="⚠ Oops!", description="I'm sorry but you cannot select this role as it is the **default role**.", color=color)
            return await ctx.respond(embed=embed, ephemeral=True)
        
        excludedIDs = db.field('SELECT excluded_ids FROM guilds WHERE guild_id = ?', ctx.guild.id)

        if role.id in excludedIDs:
            embed = discord.Embed(title="⚠ Oops!", description="This role is already excluded.", color=color)
            return await ctx.respond(embed=embed, ephemeral=True)
        
        new_excludedIDs += ', ' + role.id
        db.execute('UPDATE guilds SET excluded_ids = ? WHERE guild_id = ?', new_excludedIDs, ctx.guild.id)
        
        embed = discord.Embed(title="✅ Excluded role added", description=f"The role {role.mention} has been excluded from my list.", color=color)
        await ctx.respond(embed=embed, ephemeral=True)
    


    @commands.slash_command(name="remove-excluded", description="Admins only. Set the roles I won't check on this server.", guild_ids=guild_ids)
    async def add_excluded(self, ctx, role: discord.Option(discord.Role, "Select a role", required=True)):
        if not ctx.author.guild_permissions.administrator:
            return await ctx.respond(embed=missingPermEmbed, ephemeral=True)
        
        excludedIDs = db.field('SELECT excluded_ids FROM guilds WHERE guild_id = ?', ctx.guild.id)
        excludedIDs = list(map(int, ', '.join(excludedIDs)))

        if role.id not in excludedIDs:
            embed = discord.Embed(title="⚠ Oops!", description="This role is not excluded.", color=color)
            return await ctx.respond(embed=embed, ephemeral=True)
        
        new_excludedIDs = ', '.join(excludedIDs.remove(role.id))
        db.execute('UPDATE guilds SET excluded_ids = ? WHERE guild_id = ?', new_excludedIDs, ctx.guild.id)
            
        embed = discord.Embed(title="✅ Excluded role removed", description=f"The role {role.mention} has been removed from the excluded roles list.", color=color)
        await ctx.respond(embed=embed, ephemeral=True)



# Add the cog when the extension is loaded
def setup(bot):
    bot.add_cog(ConfigCommand(bot))
    print(' - commands.config, ConfigCommand')