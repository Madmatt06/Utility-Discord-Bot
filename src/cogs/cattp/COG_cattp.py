from discord.ext import commands


class cattp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(cattp(bot))
    print("cattp is loaded")