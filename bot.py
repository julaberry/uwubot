import discord
from discord.ext import tasks, commands
from discord import app_commands
from environs import Env
import asyncio

env = Env()
env.read_env()

roles = []
channels = []

# Thanks to print3d_pilot for the code
#Generates misery
def generateUwU(input_text):
    # the length of the input text
    length = len(input_text)
    # variable declaration for the output text
    output_text = ''
    # check the cases for every individual character
    for i in range(length):
        # initialize the variables
        current_char = input_text[i]
        previous_char = '&# 092;&# 048;'
        # assign the value of previous_char
        if i > 0:
            previous_char = input_text[i - 1]
            # change 'L' and 'R' to 'W'
        if current_char == 'L' or current_char == 'R':
            output_text += 'W'
        # change 'l' and 'r' to 'w'
        elif current_char == 'l' or current_char == 'r':
            output_text += 'w'
        # if the current character is 'o' or 'O'
        # also check the previous charatcer
        elif current_char == 'O' or current_char == 'o':
            if previous_char == 'N' or previous_char == 'n' or previous_char == 'M' or previous_char == 'm':
                output_text += "yo"
            else:
                output_text += current_char
                # if no case match, write it as it is
        else:
            output_text += current_char
    output_text = output_text.replace('th', 'ff')
    output_text = output_text.replace('Th', 'Ff')
    output_text = output_text.replace('tH', 'fF')
    output_text = output_text.replace('TH', 'FF')
    print (output_text)
    return output_text

class UwuClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

	# Set up global commands
    async def setup_hook(self):
        await self.tree.sync()

    async def UwUifyMessage(self, message):
        attachmentURLs = [atch.url for atch in message.attachments]
        mainEmbed = discord.Embed(description = f'{message.author.mention}\n{generateUwU(message.content)}')
        mainEmbed.set_thumbnail(url=message.author.display_avatar.url)
        embeds = [discord.Embed().set_image(url=atchurl) for atchurl in attachmentURLs]
        embeds.insert(0,mainEmbed)

        await message.reply(embeds=embeds)
        await asyncio.sleep(1)
        await message.delete()
		
    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return
        userRoles = [role.id for role in message.author.roles]
        msgChannel = message.channel.id
        if roles and channels: # both retrictions active
            if msgChannel in channels and bool(set(userRoles) & set(roles)):
                # DO THE THING
                await self.UwUifyMessage(message)
        elif roles: # only role restriction
             if bool(set(userRoles) & set(roles)):
                await self.UwUifyMessage(message)
        elif channels: #only channel restriction
             if msgChannel in channels:
                await self.UwUifyMessage(message)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = UwuClient(intents=intents)

def refresh():
    global roles
    global channels
    with open(env("ROLES")) as f:
        roles = []
        fcontent = f.read()
        if fcontent:
            roles = [int(x) for x in fcontent.split(',')]
    with open(env("CHANNELS")) as f:
        channels = []
        fcontent = f.read()
        if fcontent:
            channels = [int(x) for x in fcontent.split(',')]
    

refresh()

@client.tree.command(name='update_config')
async def updateConfig(interaction: discord.Interaction):
    refresh()
    await interaction.response.send_message(content="Configuration Refreshed", ephemeral=True)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

def main():
	try:
		client.run(env("TOKEN"))
	except KeyboardInterrupt:
		pass
if __name__ == '__main__':
	main()