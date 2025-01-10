import discord
from discord.ext import commands
from discord import app_commands
import requests
from src.cogs.bot_library import respond_message, create_command


class BadJoke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name=create_command("bad joke"), description="Get a bad joke!")
    async def bad_joke(self, interaction: discord.Interaction):
        headers = {'Accept': 'application/json'}
        response = requests.get(url= "https://icanhazdadjoke.com/", headers=headers)
        data = response.json()
        await respond_message(message=data["joke"], interaction=interaction, ephemeral= False)



async def setup(bot):
    await bot.add_cog(BadJoke(bot))
    print("bad_joke is loaded")