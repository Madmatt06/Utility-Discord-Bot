import discord
import src.settings as settings


async def respond_message(message: str, interaction: discord.Interaction, ephemeral: bool, view:discord.ui.View=None):
    if settings.PREFIX:
        await interaction.response.send_message(content=f"{settings.PREFIX} ({message})", ephemeral=ephemeral, view=view)
    else:
        await interaction.response.send_message(content=message, ephemeral=ephemeral, view=view)


async def edit_message(edit: str, message: discord.Interaction.original_response, view:discord.ui.View=None):
    if settings.PREFIX:
        await message.edit(content=f"{settings.PREFIX} ({edit})", view=view)
    else:
        await message.edit(content=edit, view=view)


async def send_message(message: str, channel: discord.Interaction.channel, view:discord.ui.View=None):
    if settings.PREFIX:
        await channel.send(content=f"{settings.PREFIX} ({message})", view=view)
    else:
        await channel.send(content=message, view=view)

def create_command(command: str) -> str:
    return command.replace(" ", settings.COMMAND_SEPERATOR)