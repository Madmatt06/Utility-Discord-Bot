import discord
from discord.ext import commands
from discord import app_commands
from src.cogs.bot_library import send_message, respond_message, create_command
from src.settings import SAY_PERMS, BOT_OWNER_ID


class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    if SAY_PERMS != "4":
        @app_commands.command(name=create_command("say"), description="allows the bot to say things")
        @app_commands.choices()
        async def say(self, interaction: discord.Interaction, say: str):
            if not interaction.user.id == BOT_OWNER_ID and SAY_PERMS == "0":
                return
            if not interaction.user.guild_permissions.administrator and SAY_PERMS == "1":
                return
            if not interaction.user.id == BOT_OWNER_ID and not interaction.user.guild_permissions.administrator and SAY_PERMS == "2":
                return
            await send_message(message=say, channel=interaction.channel)
            await respond_message(message="Done", interaction=interaction, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Say(bot))
    print("say is loaded")