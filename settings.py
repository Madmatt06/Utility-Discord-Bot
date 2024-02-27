import os
from dotenv import load_dotenv

# Loads all the neccesary settings from .env

load_dotenv()

DISCORD_API_SECRET = os.getenv("DISCORD_API_TOKEN")
BOT_OWNER_ID = os.getenv("BOT_OWNER_ID")