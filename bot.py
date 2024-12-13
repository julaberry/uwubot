import discord
from discord.ext import tasks, commands
from discord import app_commands
from environs import Env
import uwuify

env = Env()
env.read_env()

roles = []
channels = []

class UwuClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

	# Set up global commands
    async def setup_hook(self):
        await self.tree.sync()

    async def UwUify(self, message):
        embed = discord.Embed(title=f'<@{message.author.id}>', description = uwuify.uwu(message.content))
        await message.reply(embed=embed)
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
                uwuify(message)
        elif roles: # only role restriction
             if bool(set(userRoles) & set(roles)):
                  uwuify(message)
        elif channels: #only channel restriction
             if msgChannel in channels:
                  uwuify(message)

intents = discord.Intents.default()
client = UwuClient(intents=intents)


def refresh():
    global roles
    global channels
    with open(env("ROLES")) as f:
        roles = [int(line.split(',')) for line in f]
    with open(env("CHANNELS")) as f:
        channels = [int(line.split(',')) for line in f]

refresh()

@client.tree.command(name='Update_Config')
async def updateConfig(interaction: discord.Interaction):
	refresh()

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

def main():
	try:
		client.run(env("DISCORD_TOKEN"))
	except KeyboardInterrupt:
		pass
if __name__ == '__main__':
	main()