from nick_user import nick_user
from setting import setting

# This is the basic data model for keeping track of users and their assigned nicknames
class guild:
  def __init__(self, guild:int, settings:setting = setting(), userNicks:dict = dict()) -> None:
    self.guild = guild
    self.settings = settings
    self.userNicks:dict = userNicks
