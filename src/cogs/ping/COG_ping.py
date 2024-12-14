from discord.ext import commands


class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(ping(bot))
    print("ping is loaded")