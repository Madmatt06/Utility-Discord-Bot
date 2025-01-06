import discord
from discord.ext import commands
from discord import app_commands
from src.cogs.bot_library import send_message, respond_message, create_command
from typing import Literal



class Settings(commands.Cog):
    possible_settings: list[str] = []

    def __init__(self, bot):
        self.bot = bot

    if len(possible_settings) > 0:
        @app_commands.command(name=create_command("settings"), description="Change settings for server")
        @commands.has_permissions(administrator=True)
        async def change_settings(self, interaction: discord.Interaction, toggle: Literal["Enable", "Disable"],
                                  setting_change: Literal[tuple(possible_settings)]):
            if not interaction.user.guild_permissions.administrator:
                await respond_message(message="Hey! you can't do that!", interaction=interaction, ephemeral=True)
                return

            action = False
            if toggle == "Enable":
                action = True

            await respond_message(message=f"Setting \"{setting_change}\" change to \"{toggle}\" requested!", interaction=interaction, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Settings(bot))
    print("Settings is loaded")