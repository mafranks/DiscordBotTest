'''
Main file for discord bot. Functionality TBD.
'''

import os
from pathlib import Path
from dotenv import load_dotenv
import discord

# Providing the path to a .env file that contains the credentials
load_dotenv(dotenv_path=Path('.', '.env'))

# Intents gives the bot permissions
intents = discord.Intents.all()
BOT_TOKEN = os.getenv('BOT_TOKEN')
GUILD_NAME = os.getenv('GUILD NAME')

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD_NAME:
            break
    print(
        f'{client.user} is connected to:\n'
        f'\t{guild.name}(id: {guild.id})'
        )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

client.run(BOT_TOKEN)

