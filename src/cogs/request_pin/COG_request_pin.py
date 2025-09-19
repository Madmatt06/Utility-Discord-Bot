import discord
from discord import app_commands, Interaction
from discord.ext import commands

from src.cogs.bot_library import create_command, respond_message, edit_message, create_text
from src.cogs.staff_notify import COG_staff_notify

class Buttons(discord.ui.View):
  def __init__(self, *, timeout=None, bot:discord.ClientUser.bot, message_id:int, channel_id:int, requester_id:int):
    super().__init__(timeout=timeout)
    self.bot = bot
    self.message_id = message_id
    self.channel_id = channel_id
    self.requester_id = requester_id
  @discord.ui.button(label='Pin Message',style=discord.ButtonStyle.green)
  async def accept_button(self,interaction:discord.Interaction, button:discord.ui.Button):
    channel: discord.TextChannel = self.bot.get_channel(self.channel_id)
    message_to_pin: discord.Message = await channel.fetch_message(self.message_id)
    requester = channel.guild.get_member(self.requester_id)
    requester_name = requester.name
    requester_nick = requester.display_name
    accepter_name = interaction.user.name
    accepter_nick = interaction.user.display_name
    try:
      await message_to_pin.pin(reason=create_text(f'Pin request from {requester_name} '
                                                  f'{f'(goes by: {requester_nick})' if requester_nick is not None else ''}'
                                                  f' accepted by '
                                                  f'{accepter_name} '
                                                  f'{f'(goes by: {requester_nick})' if accepter_nick is not None else ''}'))
    except discord.errors.HTTPException as error:
      print(f'Received error when attempting to pin {error.code} with explanation {await error.response.text()}')
      if error.code == 50021:
        button.disabled = True
        await edit_message(message='I could not pin this message', original_response=interaction.message, view=self)
        await interaction.response.defer()
        return
      await edit_message(message='Something went wrong', original_response=interaction.message)
      await interaction.response.defer()
      return
    self.clear_items()
    await edit_message(message=f'Message Pinned! https://discord.com/channels/{message_to_pin.guild.id}/'
                               f'{self.channel_id}/{self.message_id}', original_response=interaction.message, view=self)
    await interaction.response.defer()
  @discord.ui.button(label='Decline Request',style=discord.ButtonStyle.danger)
  async def decline_button(self, interaction:discord.Interaction, button:discord.ui.Button):
    self.clear_items()
    channel: discord.TextChannel = self.bot.get_channel(self.channel_id)
    message_to_pin: discord.Message = await channel.fetch_message(self.message_id)
    await edit_message(message=f'Pin request declined for https://discord.com/channels/{message_to_pin.guild.id}/'
                               f'{channel.id}/{message_to_pin.id}', original_response=interaction.message, view=self)
    await interaction.response.defer()



class RequestPin(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.ctx_menu:app_commands.ContextMenu = app_commands.ContextMenu(name='Request Pin', callback=self.request_pin)
    self.bot.tree.add_command(self.ctx_menu)

  async def cog_unload(self) -> None:
    self.bot.tree.remove_command(self.ctx_menu.name, type=self.ctx_menu.type)

  #TODO: Add a check to make sure user can't pin it themself, prevent spam, and auto deny requests on system messages
  # (causes crash)
  async def request_pin(self, interaction: Interaction, message: discord.Message):
    staff_cog:COG_staff_notify = self.bot.get_cog('Staff')
    if staff_cog is None:
      await respond_message(message='Something has gone wrong!', interaction=interaction, ephemeral=True)
      print('request_pin has failed to get staff_notify cog!')
      return
    sent:bool = await staff_cog.notify_staff(message=f'<@{interaction.user.id}> has requested a message to be pinned. '
                                                     f'https://discord.com/channels/{message.guild.id}'
                                                     f'/{message.channel.id}/{message.id}',
                                             guild_id=interaction.guild_id,
                                             view=Buttons(bot=self.bot,message_id=message.id,
                                                          channel_id=message.channel.id,
                                                          requester_id=interaction.user.id))
    if not sent:
      await respond_message(
        message='The owner hasn\'t set up some features yet. Ask the server admins to setup a staff notification chat '
                'to use this command!',
        interaction=interaction, ephemeral=True)
      return
    await  respond_message(message='Request sent!', interaction=interaction, ephemeral=True)


async def setup(bot):
  await bot.add_cog(RequestPin(bot))
  print('Request Pin is loaded')
