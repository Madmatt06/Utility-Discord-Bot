import settings
import discord
from discord.ext import commands
from discord import app_commands
from nick_user import nick_user
import sys

def run():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    bot = commands.Bot(command_prefix="#", intents = intents)
    nick_users_checkin:list[discord.User] = []
    PERM_ERROR = "Sorry! You dont have the proper permissions for that!"
    @bot.event
    async def on_ready():
        print(f"Bot Name: {bot.user}")
        print(f"Bot ID: {bot.user.id}")
        print("--------------------------------------")

    @bot.event
    async def on_member_update(memberBefore:discord.User, memberAfter:discord.User):
        for user_nick in nick_users_checkin:
            if memberBefore.id == user_nick.user.id and memberAfter.nick != user_nick.nick:
                await memberAfter.edit(nick=user_nick.nick)
                return

    @bot.tree.command(name="ping", description="allows you to test if the bot is functioning")
    async def ping(interaction:discord.Interaction):
        await interaction.response.send_message("pong", ephemeral=True)

    @bot.tree.command(name="sync_tree", description="Syncs the commands with the guild. ONLY FOR ADMINS")
    async def sync_tree(interaction:discord.Interaction):
        if not interaction.user.guild_permissions.administrator and str(interaction.user.id) != settings.BOT_OWNER_ID:
            await interaction.response.send_message(PERM_ERROR, ephemeral = True)
            return
        await interaction.response.send_message("Syncing...", ephemeral = True)
        await bot.tree.sync()
        print('Command tree synced.')
        message = await interaction.original_response()
        await message.edit(content="Done")
    
    @bot.tree.command(name="force_nick", description="Allows you to force a user with permission to change nick to have a specific name")
    @app_commands.choices()
    @commands.has_permissions(manage_nicknames = True)
    async def force_nick(interaction:discord.Interaction, username: discord.Member, nick:str):
        if not interaction.user.guild_permissions.manage_nicknames:
            await interaction.response.send_message(PERM_ERROR, ephemeral=True)
            return
        if not interaction.user.guild_permissions.administrator:
            interaction.response.send_message(PERM_ERROR, ephemeral= True)
            return
        await interaction.response.send_message("Editing name", ephemeral=True)
        message = await interaction.original_response()
        for user in nick_users_checkin:
            if user.user.id == username.id:
                await message.edit(content="There is already a nickname lock for this user")
                return
        nick_users_checkin.append(nick_user(user=username,nick=nick))
        await username.edit(nick = nick)
        await message.edit(content="Done")

    @bot.tree.command(name="remove_nick_lock", description="Allows you remove a locked nickname")
    @app_commands.choices()
    @commands.has_permissions(manage_nicknames = True)
    async def remove_lock_nick(interaction:discord.Interaction, username: discord.Member):
        if(not interaction.user.guild_permissions.administrator):
            await interaction.response.send_message(PERM_ERROR, ephemeral=True)
            return
        await interaction.response.send_message("Removing...", ephemeral= True)
        message = await interaction.original_response()
        i = 0
        for user in nick_users_checkin:
            if user.user.id == username.id:
                nick_users_checkin.pop(i)
                await message.edit(content="Done")
                return
            i+= 1
        await message.edit(content="No Locks found for user")

    @bot.tree.command(name="say", description="allows the bot to say things")
    @app_commands.choices()
    async def say(interaction:discord.Interaction, say: str):
        await interaction.channel.send(say)
        await interaction.response.send_message("Done", ephemeral=True)

    @bot.tree.command(name="stop", description="Shutsdown the bot")
    async def stop(interaction:discord.Interaction):
        if(not interaction.user.guild_permissions.administrator and settings.BOT_OWNER_ID != str(interaction.user.id)):
            await interaction.response.send_message("Hey! you can't do that!")
            return
        print(interaction.user.id)
        await interaction.response.send_message("Shutting down...", ephemeral=True)
        await bot.close()
        print("Bot has shutdown.")
        sys.exit()

    bot.run(settings.DISCORD_API_SECRET)

if __name__ == "__main__":
    run()