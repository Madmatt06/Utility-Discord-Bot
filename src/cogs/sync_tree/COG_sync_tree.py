from discord.ext import commands
from discord import app_commands,Interaction
from src.cogs.defaults import *
from src.cogs.bot_library import respond_message,edit_message
import src.settings as settings
import time

class SyncTree(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_sync:float = time.time()

    @app_commands.command(name="sync_tree", description="Syncs the cogs with the guild. ONLY FOR ADMINS")
    async def sync_tree(self, interaction: Interaction):
        if not interaction.user.guild_permissions.administrator and str(interaction.user.id) != settings.BOT_OWNER_ID:
            await respond_message(message=PERM_ERROR, interaction=interaction, ephemeral=True)
            return

        if (time.time() - self.last_sync) < 30:
            await respond_message(
                message="sync_tree unavailable. Please wait at least 30 seconds between sync_tree calls.",
                interaction=interaction, ephemeral=True)
            return

        await respond_message(message="Syncing...", interaction=interaction, ephemeral=True)
        await self.bot.tree.sync()
        print("Command tree synced.")
        message = await interaction.original_response()
        await edit_message(edit="Done", message=message)
        self.last_sync = time.time()


async def setup(bot):
    await bot.add_cog(SyncTree(bot))
    print("sync_tree is loaded")