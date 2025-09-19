import os.path
from discord.ext import commands
from discord import app_commands
import discord
from src.cogs.bot_library import create_command, respond_message, send_message
from src.cogs.defaults import PERM_ERROR, SAVE_PATH


SAVE = 'staff_notify'

class Staff(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

    # Load Save Data
    data: dict[int, int] = {}
    if os.path.isfile(f'{SAVE_PATH}/{SAVE}'):
      with open(f'{SAVE_PATH}/{SAVE}', 'r') as save_file:
        save_data: str = save_file.read()
        save_data_by_guild: [str] = save_data.splitlines()
        for guild in save_data_by_guild:
          guild_data: [str] = guild.split(' ')
          try:
            data[int(guild_data[0])] = int(guild_data[1])
          except ValueError:
            print('Invalid save data found. Skipping...')
          except Exception as error:
            print(f'unknown error occurred. Stopping Load. {error}')
            return
    self.guilds_saved:[int, int] = data

  @app_commands.command(name=create_command('notify channel'), description='Sets channel for notifications for admins '
                                                                           'to appear.')
  async def set_staff_channel(self, interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
      await respond_message(message=PERM_ERROR, interaction=interaction, ephemeral=True)
      return
    self.guilds_saved[interaction.guild_id] = interaction.channel_id
    await respond_message(message='Channel set!', interaction=interaction, ephemeral=True)


  async def notify_staff(self, guild_id:int, message:str, view:discord.ui.View=None) -> bool:
    if not guild_id in self.guilds_saved:
      return False
    notify_channel:discord.Interaction.channel = self.bot.get_channel(self.guilds_saved[guild_id])
    await send_message(message=message, channel=notify_channel, view=view)
    return True

  async def cog_unload(self) -> None:
    try:
       with open(f'{SAVE_PATH}/{SAVE}', 'w') as save_file:
         for guild in self.guilds_saved:
           save_file.write(f'{guild} {self.guilds_saved[guild]}\n')
    except PermissionError:
      print('Unable to write save file due to permission errors')
      return
    print('Saved staff_notify settings')

async def setup(bot):
  await bot.add_cog(Staff(bot))
  print('Staff Notify is loaded')
