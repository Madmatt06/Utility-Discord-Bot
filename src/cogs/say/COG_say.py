import discord
from discord.ext import commands
from discord import app_commands
from src.cogs.bot_library import send_message, respond_message, create_command


class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    say_name: str = create_command("say")
    @app_commands.command(name=say_name, description="allows the bot to say things")
    @app_commands.choices()
    async def say(self, interaction: discord.Interaction, say: str):
        if not interaction.user.guild_permissions.administrator:
            return
        await send_message(message=say, channel=interaction.channel)
        await respond_message(message="Done", interaction=interaction, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Say(bot))
    print("say is loaded")