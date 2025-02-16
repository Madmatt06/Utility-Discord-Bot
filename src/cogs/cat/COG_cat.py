from discord.ext import commands
from discord import app_commands
import requests
import discord
from io import BytesIO

from src.cogs.bot_library import create_command


class Cat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # TODO: Make faster by caching next image. Might actually not be needed since saving cat image in memory seems to be faster
    @app_commands.command(name=create_command("cat"), description="Generates a cat")
    async def cat(self, interaction: discord.Interaction):
        # Gets a cat image and saves it to a BytesIO object. Then sends it.
        img_data = requests.get("https://genrandom.com/api/cat").content
        image_simul_file = BytesIO(img_data)
        image_file = discord.File(image_simul_file)
        image_file.filename = "cat.png"
        image_file.description = "A random cat picture!"
        await interaction.response.send_message(file=image_file)
        image_simul_file.close()


async def setup(bot):
    await bot.add_cog(Cat(bot))
    print("cat is loaded")