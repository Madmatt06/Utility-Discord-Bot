from code import interact
from typing import Callable

import discord.ui
from discord.ui import button
import weakref

from src.cogs.bot_library import respond_message, edit_message, edit_interaction
from src.cogs.tic_tac_toe import game

X = '❌'
O = '⭕'
BLANK = '⬜️'

WRONG_USER:str = 'This is not your game!'
NOT_TURN:str = 'It\'s not your turn!'
GAME_ENDED:str = 'This game has already ended!'
GAME_MISSING:str = 'This game could not be found.'
GAME_WIN:str = 'has won!'
UNEXPECTED_ERROR:str = 'Something went wrong!'
FAILED_UPDATE:str = 'Your play was accepted but the game screen could not be updated. Use /resume to load a new game screen'

class Board(discord.ui.View):
    def __init__(self, *, game: game, update_request:Callable[[int, int], bool], timeout=180):
        super().__init__(timeout=timeout)
        board = game.get_board()
        if board is None:
            board = [0] * 9
        instance = 0
        for tile in board:
            instance += 1
            tile_button = discord.ui.Button(label=X if tile == 1 else (O if tile == 2 else BLANK), custom_id=f'{instance}',disabled=tile!=0,row=int((instance-1)/3))
            tile_button.callback = self.handle_button_press
            self.add_item(tile_button)
        self.update_request = update_request
        self.game = weakref.ref(game)
        print('Game rendered')

    async def handle_button_press(self, interaction:discord.Interaction):
        if self.game() is None:
            await respond_message(message=GAME_MISSING, interaction=interaction, ephemeral=True)
            for child in self.children:
                if isinstance(child, discord.ui.Button):
                    child.disabled = True
            return
        if interaction.user.id != self.game().host_id and interaction.user.id != self.game().opponent_id:
            await respond_message(message=WRONG_USER, interaction=interaction, ephemeral=True)
            return
        if interaction.user.id != self.game().get_turn():
            await respond_message(message=NOT_TURN, interaction=interaction, ephemeral=True)
            return
        index = -1
        try:
            index = int(interaction.data['custom_id'])
        except ValueError:
            print(f'Interaction data for Tic Tac Toe game could not be converted to int. {interaction.data['custom_id']}')
            await respond_message(message=f'{UNEXPECTED_ERROR} [Value Error when converting interaction data]', interaction=interaction, ephemeral=True)
            return
        result = self.game().play(position=index-1, player=interaction.user.id)
        if not result:
            await respond_message(message=f'{UNEXPECTED_ERROR} [Request failed checks performed by game object]', interaction=interaction, ephemeral=True)

        state:int = self.game().did_win()
        board = self.game().get_board()
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                try:
                    tile_index:int = int(child.custom_id)
                except ValueError:
                    print(
                        f'Custom_id data for Tic Tac Toe game could not be converted to int. {child.custom_id}')
                    await respond_message(message=f'{FAILED_UPDATE} [Value Error when converting custom_id data]',
                                          interaction=interaction, ephemeral=True)
                    return
                if tile_index < 1 or tile_index > 9:
                    await respond_message(message=f'{FAILED_UPDATE} [Index out of range]')
                child.label = X if board[tile_index-1] == 1 else (O if board[tile_index-1] == 2 else BLANK)
                child.disabled = (board[tile_index-1] != 0 or state != 0)
        await edit_interaction(message=f'<@{state}> {GAME_WIN}' if state > 0 else ('Tie!' if state < 0 else f'<@{self.game().get_turn()}>'),
                               interaction=interaction, view=self)
        if state > 0 or state < 0:
            #Todo: Implement a method to update all existing screens.
            self.update_request(interaction.guild_id, state)