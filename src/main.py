import discord
from discord.ext import commands
import sys
import os
from cogs.bot_library import respond_message
import settings
import asyncio
import logging

from src.cogs.bot_library import create_command
from src.cogs.defaults import SAVE_PATH


def run():
  intents = discord.Intents.default()
  intents.message_content = True
  intents.members = True
  bot = commands.Bot(command_prefix='#', intents=intents)

  async def load_cog(cog_path: str):
    print(f'Loading {cog_path[2:-3].replace('/', '.').replace('\\', '.')}')
    await bot.load_extension(cog_path[2:-3].replace('/', '.').replace('\\', '.'))

  async def load_cogs(PATH: str = './cogs', LEVEL: int = 0):
    MAX: int = 3
    COG_PRE = 'COG_'
    PY_EXT = '.py'
    for filename in os.listdir(PATH):
      if filename.endswith(PY_EXT) and filename.startswith(COG_PRE):
        cog_path = os.path.join(PATH, filename)
        await load_cog(cog_path)
      elif MAX >= LEVEL:
        new_path = os.path.join(PATH, filename)
        if os.path.isdir(new_path):
          await load_cogs(new_path, LEVEL + 1)

  async def unload_cogs(PATH: str = './cogs', LEVEL: int = 0):
    MAX: int = 3
    COG_PRE = 'COG_'
    PY_EXT = '.py'
    for filename in os.listdir(PATH):
      if filename.endswith(PY_EXT) and filename.startswith(COG_PRE):
        cog_path = os.path.join(PATH, filename)
        await unload_cog(cog_path)
      elif MAX >= LEVEL:
        new_path = os.path.join(PATH, filename)
        if os.path.isdir(new_path):
          await unload_cogs(new_path, LEVEL + 1)

  async def unload_cog(cog_path: str):
    python_path = cog_path[2:-3].replace('/', '.').replace('\\', '.')
    print(f'Unloading {python_path}')
    try:
      await bot.unload_extension(python_path)
    except:
      print(f'failed to unload {cog_path}. Was it ever even loaded?')

  async def main():
    async with bot:
      await load_cogs()
      await bot.start(settings.DISCORD_API_SECRET)

  @bot.event
  async def on_ready():
    print(f'Bot Name: {bot.user}')
    print(f'Bot ID: {bot.user.id}')
    print('--------------------------------------')

  @bot.tree.command(name=create_command('stop'), description='Shutdown the bot')
  async def stop(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator and settings.BOT_OWNER_ID != str(interaction.user.id):
      await respond_message(message='Hey! you can\'t do that!', interaction=interaction, ephemeral=False)
      return
    print(interaction.user.id)
    await respond_message(message='Shutting down...', interaction=interaction, ephemeral=True)
    await unload_cogs()
    await bot.close()
    print('Bot has shutdown.')

  logs_path = f'{SAVE_PATH}/discord.log'
  logger = logging.getLogger('discord')
  if settings.LOG_LEVEL == '3':
    logger.setLevel(logging.DEBUG)
  elif settings.LOG_FILE == '2':
    logger.setLevel(logging.INFO)
  else:
    logger.setLevel(logging.CRITICAL)
  if not os.path.isdir(SAVE_PATH):
    try:
      os.makedirs(SAVE_PATH)
    except PermissionError:
      print('Permission Error. Unable to create saves directory')
  if settings.LOG_FILE == 'true':
    try:
      handler = logging.FileHandler(filename=logs_path, encoding='utf-8', mode='w')
      handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
      logger.addHandler(handler)
    except FileNotFoundError:
      print('Saves directory not found. logs unavailable')
    except PermissionError:
      print('Permission Error. Unable to write log file. Logs unavailable')
  else:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

  asyncio.run(main())


if __name__ == '__main__':
  run()
