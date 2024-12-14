import discord
from discord.ext import commands
import sys
import time
import os
from cogs.defaults import *
from cogs.bot_library import send_message,respond_message,edit_message
import settings

last_sync:float = time.time()



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



  @bot.tree.command(name="ping", description="allows you to test if the bot is functioning")
  async def ping(interaction:discord.Interaction):
    await respond_message(message="pong",interaction=interaction, ephemeral=True)

  @bot.tree.command(name="sync_tree", description="Syncs the cogs with the guild. ONLY FOR ADMINS")
  async def sync_tree(interaction:discord.Interaction):
    if not interaction.user.guild_permissions.administrator and str(interaction.user.id) != settings.BOT_OWNER_ID:
      await respond_message(message=PERM_ERROR,interaction=interaction, ephemeral = True)
      return

    global last_sync
    if (time.time() - last_sync) < 30:
      await respond_message(message="sync_tree unavailable. Please wait at least 30 seconds between sync_tree cogs.", interaction=interaction, ephemeral=True)
      return

    await respond_message(message="Syncing...",interaction=interaction, ephemeral = True)
    await bot.tree.sync()
    print("Command tree synced.")
    message = await interaction.original_response()
    await edit_message(edit="Done", message=message)
    last_sync = time.time()


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