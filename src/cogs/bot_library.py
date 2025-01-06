import discord
import src.settings as settings


async def respond_message(message: str, interaction: discord.Interaction, ephemeral: bool):
    if settings.PREFIX:
        await interaction.response.send_message(f"{settings.PREFIX} ({message})", ephemeral=ephemeral)
    else:
        await interaction.response.send_message(message, ephemeral=ephemeral)


async def edit_message(edit: str, message: discord.Interaction.original_response):
    if settings.PREFIX:
        await message.edit(content=f"{settings.PREFIX} ({edit})")
    else:
        await message.edit(content=edit)


async def send_message(message: str, channel: discord.Interaction.channel):
    if settings.PREFIX:
        await channel.send(f"{settings.PREFIX} ({message})")
    else:
        await channel.send(message)

def create_command(command: str) -> str:
    return command.replace(" ", settings.COMMAND_SEPERATOR)