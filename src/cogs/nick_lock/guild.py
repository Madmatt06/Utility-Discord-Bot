from src.cogs.nick_lock.nickuser import NickUser


class Guild:
  """A simple model to store guild ids and data

  Stores the guild ids, if they have nick_lock enabled, and what users have an active nick lock
  """

  def __init__(self, guild:int, enabled:bool = False, user_nicks:dict[int, NickUser] = None) -> None:
    self.guild:int = guild
    self.enabled:bool = enabled
    self.user_nicks:dict[int, NickUser] = {} if user_nicks is None else user_nicks
