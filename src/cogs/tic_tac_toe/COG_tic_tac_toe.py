import discord
from discord.ext import commands
from discord import app_commands,Interaction
from src.cogs.bot_library import respond_message, create_command
from src.cogs.tic_tac_toe.game import Game


class TicTacToe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guilds:dict[int,dict[int,Game]] = {}

    tic_tac_toe = app_commands.Group(name=create_command("tic tac toe"), description="All commands for tic tac toe games")
    @tic_tac_toe.command(name=create_command("start"), description="Allows you to start a game against someone")
    async def start(self, interaction: Interaction, opponent: discord.Member):
        await respond_message(message=f"Starting game against opponent {opponent.name}", interaction=interaction, ephemeral=True)
        if not interaction.guild_id in self.guilds

    @tic_tac_toe.command(name=create_command("resume"), description="Allows you to resume a game if the last game interaction has expired")
    async def resume(self, interaction: Interaction):
        await respond_message(message=f"Resuming game", interaction=interaction, ephemeral=True)

    @tic_tac_toe.command(name=create_command("get games"), description="Allows you to see what games you are currently included in and who you are against")
    async def get_games(self, interaction: Interaction):
        await respond_message(message=f"Getting game info", interaction=interaction, ephemeral=True)


async def setup(bot):
    await bot.add_cog(TicTacToe(bot))
    print("Tic Tac Toe is loaded")