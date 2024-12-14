import discord
from discord.ext import commands
from discord import app_commands
from src.cogs.nick_lock.nickuser import NickUser
from src.cogs.nick_lock.guild import guild
from src.cogs.defaults import *
from src.cogs.nick_lock.setting import setting
from src.cogs.bot_library import *
from typing import Literal


async def settings_denial(interaction: discord.Interaction):
    await respond_message(message="Sorry, this command is disabled for this server", interaction=interaction,
                          ephemeral=True)


class nick_lock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guilds: dict[int, guild] = {}

    def add_guild(self, guild_id: int):
        print("Adding new guild, " + str(guild_id))
        if guild_id in self.guilds:
            print("ERROR: Guild already exists. \"" + str(guild_id) + "\"")
            return
        self.guilds[guild_id] = guild(guild_id, setting(), {})
        print(self.guilds.keys())

    @commands.Cog.listener()
    async def on_member_update(self, member_before: discord.User, member_after: discord.User):
        guild_id = member_after.guild.id
        if not guild_id in self.guilds:
            self.add_guild(guild_id)
            return

        current_guild: guild = self.guilds[guild_id]
        print(current_guild.guild)
        # Checks to see if feature is enabled
        if not current_guild.settings.rude_features:
            return

        user_id: int = member_after.id
        if not user_id in current_guild.userNicks:
            return

        user: NickUser = current_guild.userNicks[user_id]

        if member_after.nick != user.nick:
            await member_after.edit(nick=user.nick)
            return
        return


    @app_commands.command(name="force_nick",
                      description="Allows you to force a user with permission to change nick to have a specific name")
    @app_commands.choices()
    @commands.has_permissions(manage_nicknames=True)
    async def force_nick(self, interaction: discord.Interaction, username: discord.Member, nick: str):

        # TODO: Check that this is correct permission checking. Looks very strange
        # Permission checks
        if not interaction.user.guild_permissions.manage_nicknames:
            await respond_message(message=PERM_ERROR, interaction=interaction, ephemeral=True)
            return
        if not interaction.user.guild_permissions.administrator:
            await respond_message(message=PERM_ERROR, interaction=interaction, ephemeral=True)
            return

        # Runs if user has permission

        guild_id: int = interaction.guild_id

        # Checks to see if the guild already exists in bots data base
        if not guild_id in self.guilds:
            self.add_guild(guild_id)

        current_guild: guild = self.guilds[guild_id]

        print(guild_id)
        if current_guild.settings.rude_features == False:
            await settings_denial(interaction=interaction)
            return

        await respond_message(message="Editing name", interaction=interaction, ephemeral=True)

        message = await interaction.original_response()

        is_edited = username.id in current_guild.userNicks

        current_guild.userNicks[username.id] = NickUser(username.id, nick)

        await username.edit(nick=nick)
        if not is_edited:
            await edit_message(edit="Nickname lock set", message=message)
        else:
            await edit_message(edit="Existing Nickname lock edited", message=message)

    @app_commands.command(name="remove_nick_lock", description="Allows you remove a locked nickname")
    @app_commands.choices()
    @commands.has_permissions(manage_nicknames=True)
    async def remove_lock_nick(self, interaction: discord.Interaction, username: discord.Member):
        if not interaction.user.guild_permissions.administrator:
            await respond_message(message=PERM_ERROR, interaction=interaction, ephemeral=True)
            return

        guild_id: int = interaction.guild_id
        if not guild_id in self.guilds:
            self.add_guild(guild_id)

        current_guild: guild = self.guilds[guild_id]

        # Checks server settings
        if not current_guild.settings.rude_features:
            await settings_denial(interaction=interaction)
            return

        await respond_message(message="Removing...", interaction=interaction, ephemeral=True)
        message = await interaction.original_response()

        if not username.id in current_guild.userNicks:
            await edit_message(edit="No Locks found for user", message=message)
            return

        current_guild.userNicks.pop(username.id)
        await edit_message(edit="Done", message=message)

    @app_commands.command(name="settings", description="Change settings for server")
    async def change_settings(self, interaction: discord.Interaction, toggle: Literal["Enable", "Disable"],
                              setting_change: Literal["Administrative Features", "Rude Features"]):
        if not interaction.user.guild_permissions.administrator and settings.BOT_OWNER_ID != str(interaction.user.id):
            await respond_message(message="Hey! you can't do that!", interaction=interaction, ephemeral=False)
            return

        guild_id = interaction.guild_id
        if not guild_id in self.guilds:
            self.add_guild(guild_id)

        current_guild: guild = self.guilds[guild_id]

        action = False
        if toggle == "Enable":
            action = True

        if setting_change == "Administrative Features":
            current_guild.settings.administrative_features = bool(action)
            await respond_message(message="Administrative features enabled", interaction=interaction, ephemeral=True)
        elif setting_change == "Rude Features":
            # This setting is a bit more serious. Prefix setting will be ignored.
            current_guild.settings.rude_features = bool(action)
            await interaction.response.send_message(
                "Rude features enabled. These are less obvious administrative features and should not be used for fun without others permission (Should be last option for administrative purposes). Use them wisely.",
                ephemeral=True)


async def setup(bot):
    await bot.add_cog(nick_lock(bot))
    print("nick_lock is loaded")