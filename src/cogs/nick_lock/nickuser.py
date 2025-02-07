from discord import User

class NickUser:
  """A Basic data model for keeping tacks of assigned nicknames
    
  Stores a userID and the nickname assigned to the users.
  """
    
  def __init__(self, user:int, nick:str) -> None:
    self.user = user
    self.nick = nick
