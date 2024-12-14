import discord
from discord.ext import commands
from discord import app_commands
import sys
import requests
from random import randint
import time
import os
from cogs.defaults import *
from cogs.bot_library import *

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
      await respond_message(message="sync_tree unavaliable. Please wait at least 30 seconds between sync_tree cogs.", interaction=interaction, ephemeral=True)
      return

    await respond_message(message="Syncing...",interaction=interaction, ephemeral = True)
    await bot.tree.sync()
    print("Command tree synced.")
    message = await interaction.original_response()
    await edit_message(edit="Done", message=message)
    last_sync = time.time()

  @bot.tree.command(name="say", description="allows the bot to say things")
  @app_commands.choices()
  async def say(interaction:discord.Interaction, say: str):
    if(not interaction.user.guild_permissions.administrator):
      return
    await send_message(message=say, channel=interaction.channel)
    await respond_message(message="Done",interaction=interaction, ephemeral=True)

  # TODO: Make faster by caching next image.
  @bot.tree.command(name="cat", description="Generates a cat")
  async def cat(interaction:discord.Interaction):
    img_data = requests.get("https://genrandom.com/api/cat").content
    with open('image_name.jpg', 'wb') as image:
      image.write(img_data)
    with open('image_name.jpg', 'rb') as image:
      imageFile = discord.File(image)
      await interaction.response.send_message(file=imageFile)

  @bot.tree.command(name="cattp", description="Random HTTP code cat style")
  async def cattp(interaction:discord.Interaction):
    http_codes = [100,101,102,103,200,201,202,203,204,205,206,207,208,214,226,300,301,302,303,304,305,307,308,400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,418,421,422,423,424,425,426,428,429,431,444,450,451,497,498,499,500,501,502,503,504,506,507,508,509,510,511,521,522,523,525,530,599]
    http_code = http_codes[randint(0, len(http_codes)-1)]
    await interaction.response.send_message("https://http.cat/" + str(http_code))



  @bot.tree.command(name="stop", description="Shutsdown the bot")
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