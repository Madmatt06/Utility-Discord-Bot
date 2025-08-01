import discord
from discord.ext import commands
from discord import app_commands
from src.cogs.nick_lock.nickuser import NickUser
from src.cogs.nick_lock.guild import Guild
from src.cogs.defaults import *
from src.cogs.bot_library import respond_message, edit_message, create_command
from typing import Literal
import logging


class NickLock(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.guilds: dict[int, Guild] = {}

  nick_lock = app_commands.Group(name=create_command('nick lock'), description='All commands for nick lock', default_permissions=discord.Permissions(manage_nicknames=True))

  def add_guild(self, guild_id: int):
    print('Adding new guild, ' + str(guild_id))
    if guild_id in self.guilds:
      print('ERROR: Guild already exists. "' + str(guild_id) + '"')
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



  @nick_lock.command(name=create_command('set'),
                     description="Changes the nickname of a user and prevents the user from changing it")
  @app_commands.choices()
  async def force_nick(self, interaction: discord.Interaction, username: discord.Member, nick: str):
    """Adds a nick lock to a user on a guild

    Checks if the user performing the action has the proper permissions and if the server has nick lock enabled.
    The function then tries to edit the name and then saves the nickname for the user in the guild.
    """

    guild_id: int = interaction.guild_id

    # Checks to see if the guild already exists in bots database
    if not guild_id in self.guilds:
      self.add_guild(guild_id)

    current_guild: Guild = self.guilds[guild_id]

    print(guild_id)

    await respond_message(message='Editing name', interaction=interaction, ephemeral=True)

    message = await interaction.original_response()

    is_edited = username.id in current_guild.user_nicks

    # TODO: Fix to try editing nickname before adding to dictionary.
    current_guild.user_nicks[username.id] = NickUser(username.id, nick)

    try:
      await username.edit(nick=nick)
    except discord.errors.Forbidden:
      await edit_message(edit='Looks like I don\'t have permissions to do that!', message=message)
      return
    except Exception as bot_error:
      # Keeps User informed something happened and raises error to make debugging easier
      await edit_message(edit='Sorry, I can\'t do that right now. Try again later.', message=message)
      logging.error(bot_error)
      raise

    if not is_edited:
      await edit_message(edit='Nickname lock set', message=message)
    else:
      await edit_message(edit='Existing Nickname lock edited', message=message)


  @nick_lock.command(name=create_command('remove'), description='Allows the user to change their nickname')
  @app_commands.choices()
  async def remove_lock_nick(self, interaction: discord.Interaction, username: discord.Member):

    guild_id: int = interaction.guild_id
    if not guild_id in self.guilds:
      self.add_guild(guild_id)

    current_guild: Guild = self.guilds[guild_id]

    await respond_message(message='Removing...', interaction=interaction, ephemeral=True)
    message = await interaction.original_response()

    if not username.id in current_guild.user_nicks:
      await edit_message(edit='No Locks found for user', message=message)
      return

    current_guild.user_nicks.pop(username.id)
    await edit_message(edit='Done', message=message)


  async def cog_unload(self) -> None:
    print('nick_lock is unloaded')
    return await super().cog_unload()



async def setup(bot):
  await bot.add_cog(NickLock(bot))
  print('nick_lock is loaded')
