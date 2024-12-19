from discord.ext import commands
from discord import app_commands
import requests
import discord


class Cat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # TODO: Make faster by caching next image.
    @app_commands.command(name="cat", description="Generates a cat")
    async def cat(self, interaction: discord.Interaction):
        img_data = requests.get("https://genrandom.com/api/cat").content
        with open('image_name.jpg', 'wb') as image:
            image.write(img_data)
        with open('image_name.jpg', 'rb') as image:
            imageFile = discord.File(image)
            await interaction.response.send_message(file=imageFile)


async def setup(bot):
    await bot.add_cog(Cat(bot))
    print("cat is loaded")