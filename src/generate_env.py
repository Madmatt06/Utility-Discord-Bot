import dotenv

from src.settings import SAY_PERMS

if __name__ == '__main__':
  DISCORD_API_TOKEN:str = ''
  BOT_OWNER_ID:str = ''
  PREFIX_MESSAGE:str = ''
  SAY_PERMS:str = '0'
  COMMAND_SEPERATOR = '_'
  LOG_FILE = 'false'
  answer = input('Would you like to set the enviroment keys now? (y/n) ')
  if answer.lower() == 'y' or answer.lower() == 'yes':
    DISCORD_API_TOKEN = input('Please type your bot token: ')
    BOT_OWNER_ID = input('Please type the discord id for the bot owner: ')
    PREFIX_MESSAGE = input('Please type the prefix you would like for messages (leave blank for nothing): ')
    COMMAND_SEPERATOR = input('Please enter the seperator you would like for your commands (sync:seperator:tree): ')
    check_say_perms = input('Please select the permission requirements for the say command (0: bot owner, 1: admins, 2: admins and bot owner, 3: everyone, 4: disabled. default: 0): ')
    try:
      check_say_perms = int(check_say_perms)
      if check_say_perms >= 0 and check_say_perms <= 4:
        SAY_PERMS = str(check_say_perms)
      else:
        print('Unknown value entered. Using default')
    except:
      print('Unknown value entered. Using default')
    do_log_file = input('Do you want to log to a file? (This will disable most of the console output) (y/N): ')
    if do_log_file == 'y':
      LOG_FILE = 'true'
    else:
      LOG_FILE = 'false'


  dotenv.set_key('.env', 'DISCORD_API_TOKEN', DISCORD_API_TOKEN)
  dotenv.set_key('.env', 'BOT_OWNER_ID', BOT_OWNER_ID)
  dotenv.set_key('.env', 'PREFIX_MESSAGE', PREFIX_MESSAGE)
  dotenv.set_key('.env', 'COMMAND_SEPERATOR', COMMAND_SEPERATOR)
  dotenv.set_key('.env', 'SAY_PERMS', SAY_PERMS)
  dotenv.set_key('.env', 'LOG_FILE', LOG_FILE)