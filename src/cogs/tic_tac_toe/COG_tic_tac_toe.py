import discord
from discord.ext import commands
from discord import app_commands, Interaction
from src.cogs.bot_library import respond_message, create_command, edit_message, send_message, followup_message
from src.cogs.tic_tac_toe.board import Board
from src.cogs.tic_tac_toe.game import Game


class TicTacToe(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.guilds: dict[int, dict[int, Game]] = {}

  tic_tac_toe = app_commands.Group(name=create_command('tic tac toe'), description='All commands for tic tac toe games')

  @tic_tac_toe.command(name=create_command('start'), description='Allows you to start a game against someone')
  async def start(self, interaction: Interaction, opponent: discord.Member):
    await respond_message(message=f'Starting game against opponent {opponent.name}', interaction=interaction,
                          ephemeral=True)
    message: Interaction.original_response = await interaction.original_response()
    current_guild: int = interaction.guild_id
    if not current_guild in self.guilds:
      self.guilds[current_guild] = {}
    host_id: int = interaction.user.id
    if host_id in self.guilds[current_guild]:
      existing_opponent = interaction.guild.get_member(self.guilds[current_guild][host_id].opponent_id).mention
      await edit_message(edit=f'You are already the host of a game against {existing_opponent}', message=message)
      return
    self.guilds[current_guild][host_id] = Game(host_id=host_id, opponent_id=opponent.id)
    _, screen = self.guilds[current_guild][host_id].game_screen()
    print(f'rendering game to channel.\n{screen}')
    game_screen = Board(game=self.guilds[current_guild][host_id], update_request=self.update_request)
    await send_message(message=f'{interaction.user.mention} Vs {opponent.mention}. {interaction.user.mention} goes first', channel=message.channel, view=game_screen)
    print('Finished Game Creation')
    print(self.guilds)

  @tic_tac_toe.command(name=create_command('resume'), description='Allows you to resume a game if the last game '
                                                                  'interaction has expired')
  async def resume(self, interaction: Interaction):
    await respond_message(message=f'Resuming game', interaction=interaction, ephemeral=True)
    message: Interaction.original_response = await interaction.original_response()
    current_guild: int = interaction.guild_id
    if not current_guild in self.guilds:
      self.guilds[current_guild] = {}
    host_id: int = interaction.user.id
    if not host_id in self.guilds[current_guild]:
      await edit_message(edit=f'You are not currently hosting any games in this server.', message=message)
      return
    game = self.guilds[current_guild][host_id]
    game_screen = Board(game=game, update_request=self.update_request)
    await send_message(message=f'<@{game.get_turn()}>', channel=interaction.channel, view=game_screen)

  @tic_tac_toe.command(name=create_command('get games'), description='Allows you to see what games you are currently '
                                                                     'included in and who you are against')
  async def get_games(self, interaction: Interaction):
    await interaction.response.defer(thinking=True, ephemeral=True)
    current_guild:int = interaction.guild_id
    host_id:int = interaction.user.id
    if not current_guild in self.guilds:
      self.guilds[current_guild] = {}
    if not host_id in self.guilds[current_guild]:
      await followup_message(message='I couldn\'t find any games hosted by you', interaction=interaction, ephemeral=True)
      return
    await followup_message(message=f'You have a game against <@{self.guilds[current_guild][host_id].opponent_id}>', interaction=interaction, ephemeral=True)

  @tic_tac_toe.command(name=create_command('stop game'), description='Allows the host to end the game prematurely. Currently does not update all screens to show that.')
  async def stop_game(self, interaction: Interaction):
    await respond_message(message='Ending any existing games', interaction=interaction, ephemeral=True)
    self.update_request(guild=interaction.guild_id, user=interaction.user.id)
  def update_request(self, guild:int, user:int) -> bool:
    # Todo: Implement a method to update all existing screens.
    self.guilds[guild].pop(user)
    return True


async def setup(bot):
  await bot.add_cog(TicTacToe(bot))
  print('Tic Tac Toe is loaded')
