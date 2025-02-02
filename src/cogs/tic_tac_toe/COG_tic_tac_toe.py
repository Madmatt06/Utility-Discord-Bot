import discord
from discord.ext import commands
from discord import app_commands,Interaction
from src.cogs.bot_library import respond_message, create_command


class TicTacToe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    tic_tac_toe = app_commands.Group(name=create_command("tic tac toe"), description="All commands for tic tac toe games")
    @tic_tac_toe.command(name=create_command("start game"), description="allows you to start a game against someone")
    async def ping(self, interaction: Interaction, opponent: discord.Member):
        await respond_message(message=f"Starting game against opponent {opponent.name}", interaction=interaction, ephemeral=True)


async def setup(bot):
    await bot.add_cog(TicTacToe(bot))
    print("Tic Tac Toe is loaded")