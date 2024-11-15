from discord import User

# This is the basic data model for keeping track of users and their assigned nicknames
class nick_user:
    def __init__(self, user:User, nick:str) -> None:
        self.user = user
        self.nick = nick