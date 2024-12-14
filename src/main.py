import settings
import discord
from discord.ext import commands
from discord import app_commands
from src.cogs.nickuser import NickUser
import sys
import requests
from random import randint
from src.cogs.guild import guild
import time
from typing import Literal
from src.cogs.setting import setting

last_sync:float = time.time()

def run():
  intents = discord.Intents.default()
  intents.message_content = True
  intents.members = True
  bot = commands.Bot(command_prefix="#", intents = intents)
  guilds:dict[int, guild] = {}


  PERM_ERROR = "Sorry! You dont have the proper permissions for that!"

  async def respond_message(message:str,interaction:discord.Interaction, ephemeral:bool):
    if settings.PREFIX:
      await interaction.response.send_message(f"{settings.PREFIX} ({message})", ephemeral=ephemeral)
    else:
      await interaction.response.send_message(message, ephemeral=ephemeral)

  async def edit_message(edit:str, message:discord.Interaction.original_response):
    if settings.PREFIX:
      await message.edit(content=f"{settings.PREFIX} ({edit})")
    else:
      await message.edit(content=edit)

  async def send_message(message:str,channel:discord.Interaction.channel):
    if settings.PREFIX:
      await channel.send(f"{settings.PREFIX} ({message})")
    else:
      await channel.send(message)

  async def settings_denial(interaction:discord.Interaction):
    await respond_message(message="Sorry, this command is disabled for this server", interaction=interaction, ephemeral=True)

  def add_guild(guild_id:int):
    print("Adding new guild, " + str(guild_id))
    if guild_id in guilds:
      print("ERROR: Guild already exists. \"" + str(guild_id) + "\"")
      return
    guilds[guild_id] = guild(guild_id, setting(), {})
    print(guilds.keys())

  @bot.event
  async def on_ready():
    print(f"Bot Name: {bot.user}")
    print(f"Bot ID: {bot.user.id}")
    print("--------------------------------------")

  @bot.event
  async def on_member_update(member_before:discord.User, member_after:discord.User):
    guild_id = member_after.guild.id
    if not guild_id in guilds:
      add_guild(guild_id)
      return

    current_guild:guild = guilds[guild_id]
    print(current_guild.guild)
    # Checks to see if feature is enabled
    if not current_guild.settings.rude_features:
      return

    user_id:int = member_after.id
    if not user_id in current_guild.userNicks:
      return

    user:NickUser = current_guild.userNicks[user_id]

    if member_after.nick != user.nick:
      await member_after.edit(nick=user.nick)
      return
    return

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

  @bot.tree.command(name="settings", description="Change settings for server")
  async def change_settings(interaction: discord.Interaction, toggle: Literal["Enable", "Disable"], setting_change: Literal["Administrative Features", "Rude Features"]):
    if (not interaction.user.guild_permissions.administrator and settings.BOT_OWNER_ID != str(interaction.user.id)):
      await respond_message(message="Hey! you can't do that!", interaction=interaction, ephemeral=False)
      return

    guild_id = interaction.guild_id
    if not guild_id in guilds:
      add_guild(guild_id)

    current_guild:guild = guilds[guild_id]

    action = False
    if toggle == "Enable":
      action = True

    if setting_change == "Administrative Features":
      current_guild.settings.administrative_features = bool(action)
      await respond_message(message="Administrative features enabled", interaction=interaction, ephemeral=True)
    elif setting_change == "Rude Features":
      # This setting is a bit more serious. Prefix setting will be ignored.
      current_guild.settings.rude_features = bool(action)
      await interaction.response.send_message("Rude features enabled. These are less obvious administrative features and should not be used for fun without others permission (Should be last option for administrative purposes). Use them wisely.", ephemeral=True)


  @bot.tree.command(name="stop", description="Shutsdown the bot")
  async def stop(interaction:discord.Interaction):
    if(not interaction.user.guild_permissions.administrator and settings.BOT_OWNER_ID != str(interaction.user.id)):
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