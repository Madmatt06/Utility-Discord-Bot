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

    async def respond_message(message:str,interaction:discord.Interaction, ephemeral:bool):
        if settings.PREFIX:
            await interaction.response.send_message(f"{settings.PREFIX} ({message})", ephemeral=ephemeral)
        else:
            await interaction.response.send_message(message, ephemeral=ephemeral)

    async def edit_message(edit:str, message:discord.Interaction.original_response):
        if settings.PREFIX:
            await message.edit(content=f"{settings.PREFIX} ({edit})")
        else:
            await message.edit(content=edit)

    async def send_message(message:str,channel:discord.Interaction.channel):
        if settings.PREFIX:
            await channel.send(f"{settings.PREFIX} ({message})")
        else:
            await channel.send(message)

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
        await respond_message(message="pong",interaction=interaction, ephemeral=True)

    @bot.tree.command(name="sync_tree", description="Syncs the commands with the guild. ONLY FOR ADMINS")
    async def sync_tree(interaction:discord.Interaction):
        if not interaction.user.guild_permissions.administrator and str(interaction.user.id) != settings.BOT_OWNER_ID:
            await respond_message(message=PERM_ERROR,interaction=interaction, ephemeral = True)
            return
        await respond_message(message="Syncing...",interaction=interaction, ephemeral = True)
        await bot.tree.sync()
        print('Command tree synced.')
        message = await interaction.original_response()
        await edit_message(edit="Done", message=message)
    
    @bot.tree.command(name="force_nick", description="Allows you to force a user with permission to change nick to have a specific name")
    @app_commands.choices()
    @commands.has_permissions(manage_nicknames = True)
    async def force_nick(interaction:discord.Interaction, username: discord.Member, nick:str):
        if not interaction.user.guild_permissions.manage_nicknames:
            await respond_message(message=PERM_ERROR,interaction=interaction, ephemeral=True)
            return
        if not interaction.user.guild_permissions.administrator:
            respond_message(message=PERM_ERROR,interaction=interaction, ephemeral= True)
            return
        await respond_message(message="Editing name",interaction=interaction, ephemeral=True)
        message = await interaction.original_response()
        for user in nick_users_checkin:
            if user.user.id == username.id:
                await edit_message(edit="There is already a nickname lock for this user",message=message)
                return
        nick_users_checkin.append(nick_user(user=username,nick=nick))
        await username.edit(nick = nick)
        await edit_message(edit="Done", message=message)

    @bot.tree.command(name="remove_nick_lock", description="Allows you remove a locked nickname")
    @app_commands.choices()
    @commands.has_permissions(manage_nicknames = True)
    async def remove_lock_nick(interaction:discord.Interaction, username: discord.Member):
        if(not interaction.user.guild_permissions.administrator):
            await respond_message(message=PERM_ERROR,interaction=interaction, ephemeral= True)
            return
        await respond_message(message= "Removing...",interaction=interaction, ephemeral= True)
        message = await interaction.original_response()
        i = 0
        for user in nick_users_checkin:
            if user.user.id == username.id:
                nick_users_checkin.pop(i)
                await edit_message(edit="Done", message= message)
                return
            i+= 1
        await edit_message(edit="No Locks found for user", message=message)

    @bot.tree.command(name="say", description="allows the bot to say things")
    @app_commands.choices()
    async def say(interaction:discord.Interaction, say: str):
        await send_message(message=say, channel=interaction.channel)
        await respond_message(message="Done",interaction=interaction, ephemeral=True)

    @bot.tree.command(name="stop", description="Shutsdown the bot")
    async def stop(interaction:discord.Interaction):
        if(not interaction.user.guild_permissions.administrator and settings.BOT_OWNER_ID != str(interaction.user.id)):
            await respond_message(message="Hey! you can't do that!",interaction=interaction, ephemeral=False)
            return
        print(interaction.user.id)
        await respond_message(message="Shutting down...",interaction=interaction, ephemeral=True)
        await bot.close()
        print("Bot has shutdown.")
        sys.exit()

    bot.run(settings.DISCORD_API_SECRET)

if __name__ == "__main__":
    run()