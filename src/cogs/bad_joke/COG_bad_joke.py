import discord
from discord.ext import commands
from discord import app_commands
import requests
from src.cogs.bot_library import respond_message


class bad_joke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="bad_joke", description="Get a bad joke!")
    async def bad_joke(self, interaction: discord.Interaction):
        headers = {'Accept': 'application/json'}
        response = requests.get(url= "https://icanhazdadjoke.com/", headers=headers)
        data = response.json()
        await respond_message(message=data["joke"], interaction=interaction, ephemeral= False)



async def setup(bot):
    await bot.add_cog(bad_joke(bot))
    print("bad_joke is loaded")