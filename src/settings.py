import os
from dotenv import load_dotenv

# Loads all the necessary settings from .env

load_dotenv()

DISCORD_API_SECRET = os.getenv('DISCORD_API_TOKEN')
BOT_OWNER_ID = os.getenv('BOT_OWNER_ID')
PREFIX = os.getenv('PREFIX_MESSAGE')
COMMAND_SEPERATOR = os.getenv('COMMAND_SEPERATOR')
SAY_PERMS = os.getenv('SAY_PERMS')
