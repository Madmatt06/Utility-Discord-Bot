from discord.ext import commands


class cat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(cat(bot))
    print("cat is loaded")