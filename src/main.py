import discord
from discord.ext import commands
import sys
import os
from cogs.bot_library import send_message,respond_message,edit_message
import settings



def run():
  intents = discord.Intents.default()
  intents.message_content = True
  intents.members = True
  bot = commands.Bot(command_prefix="#", intents = intents)

  async def load_cog(cog_path:str):
    print(f"Loading Cog {cog_path[2:-3].replace('/', '.').replace('\\', '.')}")
    await bot.load_extension(cog_path[2:-3].replace('/', '.').replace('\\', '.'))

  async def load_cogs(PATH:str = "./cogs", LEVEL:int = 0):
    MAX:int = 3
    COG_PRE = "COG_"
    PY_EXT = ".py"
    for filename in os.listdir(PATH):
      if filename.endswith(PY_EXT) and filename.startswith(COG_PRE):
        cog_path = os.path.join(PATH, filename)
        await load_cog(cog_path)
      elif MAX >= LEVEL:
        new_path = os.path.join(PATH, filename)
        if os.path.isdir(new_path):
          await load_cogs(new_path, LEVEL+1)

  @bot.event
  async def on_ready():
    print("Loading cogs")
    await load_cogs()
    print("Cogs loaded")
    print(f"Bot Name: {bot.user}")
    print(f"Bot ID: {bot.user.id}")
    print("--------------------------------------")

  @bot.tree.command(name="stop", description="Shutdown the bot")
  async def stop(interaction:discord.Interaction):
    if not interaction.user.guild_permissions.administrator and settings.BOT_OWNER_ID != str(interaction.user.id):
      await respond_message(message="Hey! you can't do that!",interaction=interaction, ephemeral=False)
      return
    print(interaction.user.id)
    await respond_message(message="Shutting down...",interaction=interaction, ephemeral=True)
    await bot.close()
    print("Bot has shutdown.")
    sys.exit()

  bot.run(settings.DISCORD_API_SECRET)

if __name__ == "__main__":
  run()