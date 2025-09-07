import discord.ext.commands
from discord.ext import commands
from discord import app_commands,Interaction
from src.cogs.defaults import *
from src.cogs.bot_library import respond_message, edit_message, create_command
import src.settings as settings
import time

class SyncTree(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.last_sync:float = time.time()

  @app_commands.command(name=create_command('sync'), description='Syncs the cogs with the guild. ONLY FOR ADMINS')
  async def sync_tree(self, interaction: Interaction):
    if not interaction.user.guild_permissions.administrator and str(interaction.user.id) != settings.BOT_OWNER_ID:
      await respond_message(message=PERM_ERROR, interaction=interaction, ephemeral=True)
      return

    if (time.time() - self.last_sync) < 30:
      await respond_message(
        message='sync tree unavailable. Please wait at least 30 seconds between sync_tree calls.',
        interaction=interaction, ephemeral=True)
      return

    await respond_message(message='Syncing...', interaction=interaction, ephemeral=True)
    await self.bot.tree.sync()
    print('Command tree synced.')
    message = await interaction.original_response()
    await edit_message(message='Done', original_response=message)
    self.last_sync = time.time()

  @commands.command()
  async def sync(self, ctx: discord.ext.commands.Context):
    if not ctx.message.author.guild_permissions.administrator and str(ctx.message.author.id) != settings.BOT_OWNER_ID:
      await ctx.channel.send(content=PERM_ERROR)
      return

    if (time.time() - self.last_sync) < 30:
      await ctx.channel.send(content='sync tree unavailable. Please wait at least 30 seconds between sync_tree calls.')
      return

    await self.bot.tree.sync()
    print('Command tree synced.')
    await ctx.channel.send(content='Synced')
    self.last_sync = time.time()

async def setup(bot):
  await bot.add_cog(SyncTree(bot))
  print('sync_tree is loaded')
