import discord
from discord.ext import commands
from discord import app_commands
from nickuser import NickUser

class nick_lock:
    def __init__(self, bot):
    @bot.tree.command(name="force_nick",
                      description="Allows you to force a user with permission to change nick to have a specific name")
    @app_commands.choices()
    @commands.has_permissions(manage_nicknames=True)
    async def force_nick(interaction: discord.Interaction, username: discord.Member, nick: str):

        # TODO: Check that this is correct permission checking. Looks very strange
        # Permission checks
        if not interaction.user.guild_permissions.manage_nicknames:
            await respond_message(message=PERM_ERROR, interaction=interaction, ephemeral=True)
            return
        if not interaction.user.guild_permissions.administrator:
            await respond_message(message=PERM_ERROR, interaction=interaction, ephemeral=True)
            return

        # Runs if user has permission

        guild_id: int = interaction.guild_id

        # Checks to see if the guild already exists in bots data base
        if not guild_id in guilds:
            add_guild(guild_id)

        current_guild: guild = guilds[guild_id]

        print(guild_id)
        if current_guild.settings.rude_features == False:
            await settings_denial(interaction=interaction)
            return

        await respond_message(message="Editing name", interaction=interaction, ephemeral=True)

        message = await interaction.original_response()

        is_edited = username.id in current_guild.userNicks

        current_guild.userNicks[username.id] = NickUser(username.id, nick)

        await username.edit(nick=nick)
        if not is_edited:
            await edit_message(edit="Nickname lock set", message=message)
        else:
            await edit_message(edit="Existing Nickname lock edited", message=message)

    @bot.tree.command(name="remove_nick_lock", description="Allows you remove a locked nickname")
    @app_commands.choices()
    @commands.has_permissions(manage_nicknames=True)
    async def remove_lock_nick(interaction: discord.Interaction, username: discord.Member):
        if (not interaction.user.guild_permissions.administrator):
            await respond_message(message=PERM_ERROR, interaction=interaction, ephemeral=True)
            return

        guild_id: int = interaction.guild_id
        if not guild_id in guilds:
            add_guild(guild_id)

        current_guild: guild = guilds[guild_id]

        # Checks server settings
        if not current_guild.settings.rude_features:
            await settings_denial(interaction=interaction)
            return

        await respond_message(message="Removing...", interaction=interaction, ephemeral=True)
        message = await interaction.original_response()

        if not username.id in current_guild.userNicks:
            await edit_message(edit="No Locks found for user", message=message)
            return

        current_guild.userNicks.pop(username.id)
        await edit_message(edit="Done", message=message)
