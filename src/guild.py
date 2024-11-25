from nickuser import NickUser
from setting import setting

# This is the basic data model for keeping track of users and their assigned nicknames
class guild:
  def __init__(self, guild:int, settings:setting, userNicks:dict) -> None:
    self.guild:int = guild
    self.settings:setting = settings
    self.userNicks:dict = userNicks
