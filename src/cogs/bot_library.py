import discord
import src.settings as settings


async def respond_message(message: str, interaction: discord.Interaction, ephemeral: bool, view:discord.ui.View=None):
  if settings.PREFIX:
    if view is None:
      await interaction.response.send_message(content=f'{settings.PREFIX} ({message})', ephemeral=ephemeral)
    else:
      await interaction.response.send_message(content=f'{settings.PREFIX} ({message})', ephemeral=ephemeral,
                                              view=view)

  else:
    if view is None:
      await interaction.response.send_message(content=message, ephemeral=ephemeral)
    else:
      await interaction.response.send_message(content=message, ephemeral=ephemeral, view=view)

async def followup_message(message: str, interaction: discord.Interaction, ephemeral: bool, view:discord.ui.View=None):
  if settings.PREFIX:
    if view is None:
      await interaction.followup.send(content=f'{settings.PREFIX} ({message})', ephemeral=ephemeral)
    else:
      await interaction.followup.send(content=f'{settings.PREFIX} ({message})', ephemeral=ephemeral,
                                              view=view)

  else:
    if view is None:
      await interaction.followup.send(content=message, ephemeral=ephemeral)
    else:
      await interaction.followup.send(content=message, ephemeral=ephemeral, view=view)

async def edit_message(message: str, original_response: discord.Interaction.message,
                       view: discord.ui.View = None):
  if settings.PREFIX:
    if view is None:
      await original_response.edit(content=f'{settings.PREFIX} ({message})')
    else:
      await original_response.edit(content=f'{settings.PREFIX} ({message})', view=view)
  else:
    if view is None:
      await original_response.edit(content=message)
    else:
      await original_response.edit(content=message, view=view)

async def edit_interaction(message: str, interaction: discord.Interaction, view:discord.ui.View=None):
  if settings.PREFIX:
    if view is None:
      await interaction.response.edit_message(content=f'{settings.PREFIX} ({message})')
    else:
      await interaction.response.edit_message(content=f'{settings.PREFIX} ({message})', view=view)
  else:
    if view is None:
      await interaction.response.edit_message(content=message)
    else:
      await interaction.response.edit_message(content=message, view=view)


async def send_message(message: str, channel: discord.Interaction.channel, view:discord.ui.View=None):
  if settings.PREFIX:
    if view is None:
      await channel.send(content=f'{settings.PREFIX} ({message})')
    else:
      await channel.send(content=f'{settings.PREFIX} ({message})', view=view)
  else:
    if view is None:
      await channel.send(content=message)
    else:
      await channel.send(content=message, view=view)


def create_text(text:str) -> str:
  if settings.PREFIX:
    return f'{settings.PREFIX} ({text})'
  else:
    return text

def create_command(command: str) -> str:
  return command.replace(' ', settings.COMMAND_SEPERATOR)