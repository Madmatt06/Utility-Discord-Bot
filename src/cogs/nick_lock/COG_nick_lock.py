import discord
from discord.ext import commands
from discord import app_commands
from src.cogs.nick_lock.nickuser import NickUser
from src.cogs.nick_lock.guild import Guild
from src.cogs.defaults import *
from src.cogs.bot_library import respond_message,edit_message
from typing import Literal
import logging


async def settings_denial(interaction: discord.Interaction):
    await respond_message(message="Sorry, this command is disabled for this server", interaction=interaction,
                          ephemeral=True)


class nick_lock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guilds: dict[int, Guild] = {}

    def add_guild(self, guild_id: int):
        print("Adding new guild, " + str(guild_id))
        if guild_id in self.guilds:
            print("ERROR: Guild already exists. \"" + str(guild_id) + "\"")
            return
        self.guilds[guild_id] = Guild(guild_id)
        print(self.guilds.keys())

    @commands.Cog.listener()
    async def on_member_update(self, member_before: discord.User, member_after: discord.User):
        guild_id = member_after.guild.id
        if not guild_id in self.guilds:
            self.add_guild(guild_id)
            return

        current_guild: Guild = self.guilds[guild_id]
        print(current_guild.guild)
        # Checks to see if feature is enabled
        if not current_guild.enabled:
            return

        user_id:int = member_after.id
        if not user_id in current_guild.user_nicks:
            return

        user:NickUser = current_guild.user_nicks[user_id]

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

        # Checks to see if the guild already exists in bots database
        if not guild_id in self.guilds:
            self.add_guild(guild_id)

        current_guild: Guild = self.guilds[guild_id]

        print(guild_id)
        if not current_guild.enabled:
            await settings_denial(interaction=interaction)
            return

        await respond_message(message="Editing name", interaction=interaction, ephemeral=True)

        message = await interaction.original_response()

        is_edited = username.id in current_guild.user_nicks

        current_guild.user_nicks[username.id] = NickUser(username.id, nick)

        try:
            await username.edit(nick=nick)
        except discord.errors.Forbidden:
            await edit_message(edit="Looks like I don't have permissions to do that!", message=message)
            return
        except Exception as bot_error:
            # Keeps User informed something happened and raises error to make debugging easier
            await edit_message(edit="Sorry, I can't do that right now. Try again later.", message=message)
            logging.error(bot_error)
            raise

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

        current_guild: Guild = self.guilds[guild_id]

        # Checks server settings
        if not current_guild.enabled:
            await settings_denial(interaction=interaction)
            return

        await respond_message(message="Removing...", interaction=interaction, ephemeral=True)
        message = await interaction.original_response()

        if not username.id in current_guild.user_nicks:
            await edit_message(edit="No Locks found for user", message=message)
            return

        current_guild.user_nicks.pop(username.id)
        await edit_message(edit="Done", message=message)

    @app_commands.command(name="settings", description="Change settings for server")
    @commands.has_permissions(administrator=True)
    async def change_settings(self, interaction: discord.Interaction, toggle: Literal["Enable", "Disable"],
                              setting_change: Literal["Nick Lock"]):
        if not interaction.user.guild_permissions.administrator:
            await respond_message(message="Hey! you can't do that!", interaction=interaction, ephemeral=False)
            return

        guild_id = interaction.guild_id
        if not guild_id in self.guilds:
            self.add_guild(guild_id)

        current_guild: Guild = self.guilds[guild_id]

        action = False
        if toggle == "Enable":
            action = True

        if setting_change == "Nick Lock":
            # This setting is a bit more sketchy. Prefix setting will be ignored.
            current_guild.enabled = bool(action)
            await interaction.response.send_message(
                "Nick Lock enabled. This is a less obvious administrative features and should not be used for fun without others permission (Should be last option for administrative purposes). Use them wisely.",
                ephemeral=True)


async def setup(bot):
    await bot.add_cog(nick_lock(bot))
    print("nick_lock is loaded")