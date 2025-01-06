import discord
from discord.ext import commands
import sys
import os
from cogs.bot_library import respond_message
import settings
import asyncio
import logging

from src.cogs.bot_library import create_command


def run():
  intents = discord.Intents.default()
  intents.message_content = True
  intents.members = True
  bot = commands.Bot(command_prefix="#", intents = intents)

  async def load_cog(cog_path:str):
    print(f"Loading {cog_path[2:-3].replace('/', '.').replace('\\', '.')}")
    await bot.load_extension(cog_path[2:-3].replace('/', '.').replace('\\', '.'))

  async def load_cogs(PATH:str = "./cogs", LEVEL:int = 0, LATE:bool = False):
    MAX:int = 3
    COG_PRE = "COG_"
    LATE_COG_PRE = "LCOG"
    PY_EXT = ".py"
    for filename in os.listdir(PATH):
      path = os.path.join(PATH, filename)
      if filename.endswith(PY_EXT) and filename.startswith(COG_PRE) and not LATE:
        await load_cog(path)
      elif filename.endswith(PY_EXT) and filename.startswith(LATE_COG_PRE) and LATE:
        await load_cog(path)
      elif MAX >= LEVEL and os.path.isdir(path):
        await load_cogs(path, LEVEL+1, LATE)

  async def main():
    async with bot:
      print("Loading first cogs")
      await load_cogs()
      print("Loading last cogs")
      await load_cogs(LATE=True)
      await bot.start(settings.DISCORD_API_SECRET)

  @bot.event
  async def on_ready():
    print(f"Bot Name: {bot.user}")
    print(f"Bot ID: {bot.user.id}")
    print("--------------------------------------")

  stop_name: str = create_command("stop")
  @bot.tree.command(name=stop_name, description="Shutdown the bot")
  async def stop(interaction:discord.Interaction):
    if not interaction.user.guild_permissions.administrator and settings.BOT_OWNER_ID != str(interaction.user.id):
      await respond_message(message="Hey! you can't do that!",interaction=interaction, ephemeral=False)
      return
    print(interaction.user.id)
    await respond_message(message="Shutting down...",interaction=interaction, ephemeral=True)
    await bot.close()
    print("Bot has shutdown.")
    sys.exit()

  logger = logging.getLogger('discord')
  logger.setLevel(logging.DEBUG)
  handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
  handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
  logger.addHandler(handler)
  asyncio.run(main())

if __name__ == "__main__":
  run()