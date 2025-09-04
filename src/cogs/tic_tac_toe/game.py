class Game:
  """A class for Tic Tac Toe games.

  Some basic logic is included for playing and checking if someone won.

  Attributes:
      board           The current board with all the pieces
      turn            If True, the Host has their turn, otherwise it's the opponent
      host_id         The user id of the host of the game
      opponent_id     The user id of the opponent for the game
  """
  def __init__(self, host_id:int, opponent_id:int, board:[int] = None):
    self.board: list[int] = board if not board is None else [0] * 9
    self.turn = False
    self.host_id = host_id
    self.opponent_id = opponent_id

  def play(self, position:int, player:bool) -> bool:

    # Checks if play should be allowed by checking if position is valid and if it's the players turn
    if self.board[position] != 0: return False
    if self.turn != player: return False

    # Saves the play
    self.board[position] = 1 if player else 2
    return True

  def get_turn(self) -> int:
    return self.host_id if self.turn else self.opponent_id

  def get_board(self) -> [int]:
    return self.board.copy()

  def check_horizontal(self) -> int:
    for row in range(0,3):
      if self.board[row*3] != 0:
        win:bool = True
        match = self.board[row*3]
        for col in range(1,3):
          if self.board[row * 3 + col] != match:
            win = False
            break
        if win:
          return match
    return 0

  def check_vertical(self) -> int:
    for col in range(0,3):
      if self.board[col] != 0:
        win:bool = True
        match = self.board[col]
        for row in range(1,3):
          if self.board[row * 3 + col] != match:
            win = False
            break
        if win:
          return match
    return 0

  def check_diagonal(self) -> int:
    if self.board[0] != 0:
      match:int = self.board[0]
      win:bool = True
      for i in range(1,3):
        if self.board[i*4+1] != match:
          win = False
          break
      if win:
        return match
    if self.board[2] != 0:
      match: int = self.board[2]
      win: bool = True
      for i in range(1, 3):
        if self.board[i * 2 + 2] != match:
          win = False
          break
      if win:
        return match
    return 0

  def game_screen(self) -> tuple[int, str]:
    screen:list[str] = []
    option:int = 0
    iteration:int = 1
    turn:bool = True
    screen.append(" ")
    for tile in self.board:
      screen.append(" ")
      if tile == "":
        if turn:
          option += 1
          screen.append(f"{option}")
        else:
          screen.append(" ")
      else:
        screen.append("X" if tile == 0 else "O")
      if iteration % 3 == 0 and iteration != 9:
        screen.append("\n -----------\n ")
      elif iteration != 9:
        screen.append(" |")
      else:
        screen.append("\n")
      iteration += 1
    return option, "".join(screen)

  def did_win(self) -> int:
    did_win:int = self.check_horizontal()
    did_win += self.check_vertical()
    did_win += self.check_diagonal()
    if did_win > 2 or did_win < 0:
      return -1
    return did_win

    