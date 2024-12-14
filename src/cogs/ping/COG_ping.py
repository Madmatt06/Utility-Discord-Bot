from discord.ext import commands
from discord import app_commands,Interaction
from src.cogs.bot_library import respond_message

class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="allows you to test if the bot is functioning")
    async def ping(self, interaction: Interaction):
        await respond_message(message="pong", interaction=interaction, ephemeral=True)


async def setup(bot):
    await bot.add_cog(ping(bot))
    print("ping is loaded")