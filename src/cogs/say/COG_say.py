from discord.ext import commands


class say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(say(bot))
    print("say is loaded")