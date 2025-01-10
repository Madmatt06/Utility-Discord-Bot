import discord
from discord import app_commands, Interaction
from discord.ext import commands

from src.cogs.bot_library import create_command, respond_message, edit_message, create_text
from src.cogs.staff_notify import COG_staff_notify

class Buttons(discord.ui.View):
    def __init__(self, *, timeout=None, bot:discord.ClientUser.bot):
        super().__init__(timeout=timeout)
        self.bot = bot
    @discord.ui.button(label="Pin Message",style=discord.ButtonStyle.green)
    async def accept_button(self,interaction:discord.Interaction, button:discord.ui.Button):
        #Todo: Look in to passing in a message object or ids directly in the init function instead of this sketchy decoding
        target_message: str = interaction.message.content
        print(f"Decoding bot message for ids \"{target_message}\"")
        starter = "https://discord.com/channels/"
        starting_id: int = target_message.find(starter)
        repeat_message_link: str = target_message[starting_id:]
        if repeat_message_link.endswith(")"):
            repeat_message_link = repeat_message_link[:-1]
        target_message = target_message[starting_id + len(starter):]
        next_seperator: int = target_message.find("/")
        guild_id: str = target_message[:next_seperator]
        target_message = target_message[next_seperator + 1:]
        next_seperator = target_message.find("/")
        channel_id: str = target_message[:next_seperator]
        target_message = target_message[next_seperator + 1:]
        ending: int = 0
        for letter in target_message:
            if letter.isdigit():
                ending += 1
            else:
                break
        message_id: str = target_message[:ending]
        print(f"Getting message with guild \"{guild_id}\", Channel \"{channel_id}\", and message id \"{message_id}\"")
        channel: discord.TextChannel = self.bot.get_channel(int(channel_id))
        message_to_pin: discord.Message = await channel.fetch_message(int(message_id))
        try:
            await message_to_pin.pin(reason=create_text("Pin request accepted"))
        except discord.errors.HTTPException as error:
            print(f"Recieved error when attempting to pin {error.code} with explanation {await error.response.text()}")
            if error.code == 50021:
                button.disabled = True
                await edit_message(edit="I could not pin this message", message=interaction.message, view=self)
                await interaction.response.defer()
                return
            await edit_message(edit="Something went wrong", message=interaction.message)
            await interaction.response.defer()
            return
        self.clear_items()
        await edit_message(edit=f"Message Pinned! {repeat_message_link}", message=interaction.message, view=self)
        await interaction.response.defer()
    @discord.ui.button(label="Decline Request",style=discord.ButtonStyle.danger)
    async def decline_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        repeat_message_link:str = ""
        target_message: str = interaction.message.content
        print(f"Extracting discord message link \"{target_message}\"")
        starter = "https://discord.com/channels/"
        starting_id: int = target_message.find(starter)
        if starting_id != -1:
            repeat_message_link = target_message[starting_id:]
            if repeat_message_link.endswith(")"):
                repeat_message_link = repeat_message_link[:-1]
        else:
            print(f"No Message link was left in request. Repeat is {repeat_message_link}")
        self.clear_items()
        await edit_message(edit=f"Pin request declined {repeat_message_link}", message=interaction.message, view=self)
        await interaction.response.defer()



class RequestPin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ctx_menu:app_commands.ContextMenu = app_commands.ContextMenu(name="Request Pin", callback=self.request_pin)
        self.bot.tree.add_command(self.ctx_menu)

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(self.ctx_menu.name, type=self.ctx_menu.type)

    #TODO: Add a check to make sure user can't pin it themself, prevent spam, and auto deny requests on system messages (causes crash)
    async def request_pin(self, interaction: Interaction, message: discord.Message):
        staff_cog:COG_staff_notify = self.bot.get_cog("Staff")
        if staff_cog is None:
            await respond_message(message="Something has gone wrong!", interaction=interaction, ephemeral=True)
            print("request_pin has failed to get staff_notify cog!")
            return
        sent:bool = await staff_cog.notify_staff(message=f"Someone has requested a message to be pinned. https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}", guild_id=interaction.guild_id, view=Buttons(bot=self.bot))
        if not sent:
            await respond_message(
                message="The owner hasn't set up some features yet. Ask the server admins to setup a staff notification chat to use this command!",
                interaction=interaction, ephemeral=True)
            return
        await  respond_message(message="Request sent!", interaction=interaction, ephemeral=True)


async def setup(bot):
    await bot.add_cog(RequestPin(bot))
    print("Request Pin is loaded")