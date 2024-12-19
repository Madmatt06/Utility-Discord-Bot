from src.cogs.nick_lock.nickuser import NickUser


# This is the basic data model for keeping track of users and their assigned nicknames
class Guild:
  guild:int
  enabled:bool
  user_nicks:dict[int, NickUser]

  def __init__(self, guild:int, enabled:bool = False, user_nicks:dict[int, NickUser] = None) -> None:
    self.guild:int = guild
    self.enabled:bool = enabled
    if user_nicks is None:
      self.user_nicks:dict[int, NickUser] = {}
    else:
      self.user_nicks:dict[int, NickUser] = user_nicks
