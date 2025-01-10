from discord.app_commands import guilds
from discord.ext import commands
from discord import app_commands
import discord

from src.cogs.bot_library import create_command, respond_message, send_message
from src.cogs.defaults import PERM_ERROR


class Staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guilds_saved: dict[int, int] = {}

    @app_commands.command(name=create_command("notify channel"), description="Sets channel for notifications to appear")
    async def set_staff_channel(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            await respond_message(message=PERM_ERROR, interaction=interaction, ephemeral=True)
            return
        self.guilds_saved[interaction.guild_id] = interaction.channel_id
        await respond_message(message="Channel set!", interaction=interaction, ephemeral=True)


    async def notify_staff(self, guild_id:int, message:str, view:discord.ui.View=None) -> bool:
        if not guild_id in self.guilds_saved:
            return False
        notify_channel:discord.Interaction.channel = self.bot.get_channel(self.guilds_saved[guild_id])
        await send_message(message=message, channel=notify_channel, view=view)
        return True


async def setup(bot):
    await bot.add_cog(Staff(bot))
    print("Staff Notify is loaded")