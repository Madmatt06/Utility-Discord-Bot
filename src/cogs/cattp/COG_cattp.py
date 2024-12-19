import discord
from discord.ext import commands
from discord import app_commands
from random import randint


class Cattp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="cattp", description="Random HTTP code cat style")
    async def cattp(self, interaction: discord.Interaction):
        http_codes = [100, 101, 102, 103, 200, 201, 202, 203, 204, 205, 206, 207, 208, 214, 226, 300, 301, 302, 303,
                      304, 305, 307, 308, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414,
                      415, 416, 417, 418, 421, 422, 423, 424, 425, 426, 428, 429, 431, 444, 450, 451, 497, 498, 499,
                      500, 501, 502, 503, 504, 506, 507, 508, 509, 510, 511, 521, 522, 523, 525, 530, 599]
        http_code = http_codes[randint(0, len(http_codes) - 1)]
        await interaction.response.send_message("https://http.cat/" + str(http_code))


async def setup(bot):
    await bot.add_cog(Cattp(bot))
    print("cattp is loaded")