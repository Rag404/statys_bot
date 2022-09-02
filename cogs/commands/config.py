from discord import Cog, ApplicationContext, Color, Embed, Bot, Interaction, SelectOption, Role, ButtonStyle, slash_command, option
from discord.ui import Button, Select, View
import database_reader as db
from discord import ApplicationContext
from data.locales.commands import config_loc, back_button, exit_button, missing_permission_embed

color = Color.embed_background()
missingPermEmbed = Embed(title="⛔ Missing permissions", description="You need the Administrator permissions to use this command! 😢", color=color)


class ConfigCommand(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot


    @slash_command(
        name="config",
        name_localizations=config_loc["name"],
        description="Admins only. Configure the bot for your server.",
        description_localizations=config_loc["description"]
    )
    async def config_cmd(self, ctx: ApplicationContext):
        
        def get_locale(locales: dict):
            return locales.get(ctx.locale, "en-US")
        
        
        # If the user who invoked the command is not admin, send him an embed
        if not ctx.author.guild_permissions.administrator:
            return await ctx.respond(embed=get_locale(missing_permission_embed), ephemeral=True)
        
        
        # Create a function to check if the user who interact is an admin
        async def is_missing_perms(interaction: Interaction):
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message(embed=get_locale(missing_permission_embed), ephemeral=True)  # If not, send a embed to inform the user
                return True
            return False
        

        main_embed: Embed = get_locale(config_loc["embeds"]["main"])
        select_supporter_embed: Embed = get_locale(config_loc["embeds"]["select_supporter"])
        exclude_roles_embed: Embed = get_locale(config_loc["embeds"]["exclude_roles"])

        class SelectRoleButton(Button):
            def __init__(self):
                super().__init__(
                    label=get_locale(config_loc["buttons"]["select_supporter"]),
                    emoji="🎭"
                )

            async def callback(self, interaction: Interaction):
                if await is_missing_perms(interaction): return
                await interaction.message.edit(embed=select_supporter_embed, view=SelectView())  # Edit the message to display the role selection menu
        

        class SelectRoleDropdown(Select):            
            def __init__(self):
                options = [SelectOption(
                    label=get_locale(config_loc["dropdowns"]["select_supporter"]),
                    emoji="🚫",
                    value="0",
                    default=True
                )]
                current_role_id = db.field('SELECT supporter_id FROM guilds WHERE guild_id = ?', ctx.guild.id)

                count = 0
                for role in ctx.guild.roles:
                    if role.is_default() or role.managed: continue
                    count += 1
                    if count > 24: break  # There already is the "no role" options so there is only 24 options left for roles, not 25
                    options.append(SelectOption(label=role.name, value=str(role.id), emoji="<:mention:940318470002835477>"))
                    if current_role_id == role.id:
                        options[-1].default = True
                        options[0].default = False

                super().__init__(options=options)

            async def callback(self, interaction: Interaction):
                if await is_missing_perms(interaction): return
                new_role_id = int(self.values[0])
                db.execute('UPDATE guilds SET supporter_id = ? WHERE guild_id = ?', new_role_id, interaction.guild.id)
        

        class ExcludeButton(Button):
            def __init__(self):
                super().__init__(
                    label=get_locale(config_loc["buttons"]["exclude_roles"]),
                    emoji="❌"
                )
                
            async def callback(self, interaction):
                if await is_missing_perms(interaction): return
                await interaction.message.edit(embed=exclude_roles_embed, view=ExcludeView())
        

        class ExcludeDropdown(Select):
            def __init__(self):
                options = []

                excludedIDs = db.field('SELECT excluded_ids FROM guilds WHERE guild_id = ?', ctx.guild.id)
                excludedIDs = list(map(int, excludedIDs.split(', ')))

                count = 0
                for count, role in enumerate(ctx.guild.roles):
                    if role.is_default(): continue
                    count += 1
                    if count > 25: break
                    options.append(SelectOption(label=role.name, value=str(role.id), emoji="<:mention:940318470002835477>"))
                    if role.id in excludedIDs:
                        options[-1].default = True

                super().__init__(options=options, placeholder="Select roles or Leave empty", min_values=0, max_values=len(options))

            async def callback(self, interaction):
                if await is_missing_perms(interaction): return

                new_excludedIDs = ', '.join(self.values)
                db.execute('UPDATE guilds SET excluded_ids = ? WHERE guild_id = ?', new_excludedIDs, interaction.guild.id)


        class BackButton(Button):
            def __init__(self):
                super().__init__(
                    label=get_locale(back_button),
                    emoji="<:back_arrow:940318470069960744>",
                    row=4
                )

            async def callback(self, interaction):
                if await is_missing_perms(interaction): return
                await interaction.message.edit(embed=main_embed, view=MainView())
        

        class ExitButton(Button):
            def __init__(self, row=4):
                super().__init__(
                    label=get_locale(exit_button),
                    style=ButtonStyle.red,
                    row=row
                )

            async def callback(self, interaction):
                if await is_missing_perms(interaction): return
                await interaction.message.delete()


        class MainView(View):
            def __init__(self):
                super().__init__()
                self.add_item(SelectRoleButton())
                self.add_item(ExcludeButton())
                self.add_item(ExitButton(row=0))

        class SelectView(View):
            def __init__(self):
                super().__init__()

                if len(ctx.guild.roles) > 24:
                    select_supporter_embed.description += get_locale(config_loc["select_supporter"]["warning"])
                        
                self.add_item(SelectRoleDropdown())
                self.add_item(BackButton())
                self.add_item(ExitButton())
        
        class ExcludeView(View):
            def __init__(self):
                super().__init__()
                
                if len(ctx.guild.roles) > 25:
                    exclude_roles_embed.description += get_locale(config_loc["exclude_roles"]["warning"])

                self.add_item(ExcludeDropdown())
                self.add_item(BackButton())
                self.add_item(ExitButton())


        await ctx.respond(embed=main_embed, view=MainView())
    


    @Cog.listener()
    async def on_guild_join(self, guild):
        db.execute('INSERT INTO guilds (guild_id, supporter_id, excluded_ids) VALUES (?, ?, ?)', guild.id, 0, "0")
    

    @Cog.listener()
    async def on_guild_remove(self, guild):
        db.execute('DELETE FROM guilds WHERE guild_id = ?', guild.id)
    

    @Cog.listener()
    async def on_ready(self):
        # Check if all the guilds are registered in the data
        for guild in self.bot.guilds:
            guild_data = db.record('SELECT * FROM guilds WHERE guild_id = ?', guild.id)
            if not guild_data:
                db.execute('INSERT INTO guilds (guild_id, supporter_id, excluded_ids) VALUES (?, ?, ?)', guild.id, 0, "0")
    

    @Cog.listener()
    async def is_closed(self):
        db.commit()
    
    

    @slash_command(name="set-supporter", description="Admins only. Set the supporter role for this server.")
    @option("role", description="Select a role")
    async def set_supporter(self, ctx: ApplicationContext, role: Role):
        if not ctx.author.guild_permissions.administrator:
            return await ctx.respond(embed=missingPermEmbed, ephemeral=True)
        
        if role.is_default():
            embed = Embed(title="⚠ Oops!", description="I'm sorry but you cannot select this role as it is the **default role**.", color=color)
            return await ctx.respond(embed=embed, ephemeral=True)
        
        if role.managed:
            embed = Embed(title="⚠ Oops!", description="I'm sorry but you cannot select this role as it is **managed by an integration**.", color=color)
            return await ctx.respond(embed=embed, ephemeral=True)
        
        botMember = ctx.guild.get_member(self.bot.user.id)
        if role >= botMember.top_role:
            embed = Embed(title="⚠ Oops!", description="I'm sorry but can't manage this role as it is **higher than my highest role**.", color=color)
            return await ctx.respond(embed=embed, ephemeral=True)

        db.execute('UPDATE guilds SET supporter_id = ? WHERE guild_id = ?', role.id, ctx.guild.id)
        
        embed = Embed(title="✅ Supporter role selected", description=f"The supporter role has been set to {role.mention}", color=color)
        await ctx.respond(embed=embed, ephemeral=True)
    


    @slash_command(name="add-excluded", description="Admins only. Set the roles I won't check on this server.")
    @option("role", description="Select a role")
    async def add_excluded(self, ctx: ApplicationContext, role: Role):
        if not ctx.author.guild_permissions.administrator:
            return await ctx.respond(embed=missingPermEmbed, ephemeral=True)
        
        if role.is_default():
            embed = Embed(title="⚠ Oops!", description="I'm sorry but you cannot select this role as it is the **default role**.", color=color)
            return await ctx.respond(embed=embed, ephemeral=True)
        
        excludedIDs = db.field('SELECT excluded_ids FROM guilds WHERE guild_id = ?', ctx.guild.id)

        if role.id in excludedIDs:
            embed = Embed(title="⚠ Oops!", description="This role is already excluded.", color=color)
            return await ctx.respond(embed=embed, ephemeral=True)
        
        new_excludedIDs += ', ' + role.id
        db.execute('UPDATE guilds SET excluded_ids = ? WHERE guild_id = ?', new_excludedIDs, ctx.guild.id)
        
        embed = Embed(title="✅ Excluded role added", description=f"The role {role.mention} has been excluded from my list.", color=color)
        await ctx.respond(embed=embed, ephemeral=True)
    


    @slash_command(name="remove-excluded", description="Admins only. Set the roles I won't check on this server.")
    @option("role", description="Select a role")
    async def add_excluded(self, ctx: ApplicationContext, role: Role):
        if not ctx.author.guild_permissions.administrator:
            return await ctx.respond(embed=missingPermEmbed, ephemeral=True)
        
        excludedIDs = db.field('SELECT excluded_ids FROM guilds WHERE guild_id = ?', ctx.guild.id)
        excludedIDs = list(map(int, ', '.join(excludedIDs)))

        if role.id not in excludedIDs:
            embed = Embed(title="⚠ Oops!", description="This role is not excluded.", color=color)
            return await ctx.respond(embed=embed, ephemeral=True)
        
        new_excludedIDs = ', '.join(excludedIDs.remove(role.id))
        db.execute('UPDATE guilds SET excluded_ids = ? WHERE guild_id = ?', new_excludedIDs, ctx.guild.id)
            
        embed = Embed(title="✅ Excluded role removed", description=f"The role {role.mention} has been removed from the excluded roles list.", color=color)
        await ctx.respond(embed=embed, ephemeral=True)



# Add the cog when the extension is loaded
def setup(bot):
    bot.add_cog(ConfigCommand(bot))
    print(' - commands.config, ConfigCommand')