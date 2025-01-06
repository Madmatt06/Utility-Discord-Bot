import dotenv

if __name__ == "__main__":
  DISCORD_API_TOKEN:str = ""
  BOT_OWNER_ID:str = ""
  PREFIX_MESSAGE:str = ""
  answer = input("Would you like to set the enviroment keys now? (y/n) ")
  COMMAND_SEPERATOR = "_"
  if answer.lower() == "y" or answer.lower() == "yes":
    DISCORD_API_TOKEN = input("Please type your bot token: ")
    BOT_OWNER_ID = input("Please type the discord id for the bot owner: ")
    PREFIX_MESSAGE = input("Please type the prefix you would like for messages (leave blank for nothing): ")
    COMMAND_SEPERATOR = input("Please enter the seperator you would like for your commands (sync:seperator:tree): ")


  dotenv.set_key(".env", "DISCORD_API_TOKEN", DISCORD_API_TOKEN)
  dotenv.set_key(".env", "BOT_OWNER_ID", BOT_OWNER_ID)
  dotenv.set_key(".env", "PREFIX_MESSAGE", PREFIX_MESSAGE)
  dotenv.set_key(".env", "COMMAND_SEPERATOR", COMMAND_SEPERATOR)
