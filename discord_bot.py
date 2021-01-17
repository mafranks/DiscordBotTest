'''
Main file for discord bot. Functionality TBD.
'''

import os
import random
from pathlib import Path
from dotenv import load_dotenv
import discord

# Providing the path to a .env file that contains the credentials
load_dotenv(dotenv_path=Path('.', '.env'))

# Pull in the credentials
BOT_TOKEN = os.getenv('BOT_TOKEN')
GUILD_NAME = os.getenv('GUILD_NAME')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Intents gives the bot permissions
intents = discord.Intents.all()

# Connect to the Discord server (guild)
client = discord.Client(intents=intents)

def display_server_information(guild):
    '''Display the server information'''
    # Print the bot and guild information
    print(f'{client.user} is connected to:\n\t{guild.name} (id: {guild.id})')

def display_users(guild):
    '''Display the users on the server'''
    # Find and print all of the guild members
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@client.event
async def on_ready():
    '''
    Main function to view options on the CLI
    '''
    # Loop through all the servers and look for one that matches the GUILD_NAME
    guild = discord.utils.get(client.guilds, name=GUILD_NAME)
    display_server_information(guild)
    display_users(guild)

@client.event
async def on_member_join(member):
    '''Welcome new members'''
    await member.create_dm()
    await member.dm_channel.send(f"Hello {member.name}, welcome to the server.")

@client.event
async def on_message(message):
    '''Handle events for posted messages'''
    # Ignore messages from the bot to avoid a loop
    if message.author == client.user:
        return

    brooklyn_99_quotes = [
        'Bingpot!',
        'Terry loves yogurt.',
        'Cool. Cool cool cool cool cool cool cool cool.',
        'Cool cool cool, tight tight tight.',
        'No doubt, no doubt.',
        'Title of your sex tape.',
        'If I die, turn my tweets into a book.',
        "I'm playing Kwazy Cupcakes, I'm hydrated as hell, and I'm listening to Sheryl Crow.  \
            I've got my own party going on.",
        'OK, no hard feelings, but I hate you.  Not joking.  Bye.',
        "Captain, hey!  Welcome to the murder.",
        "Aw man.  All the orange ssoda spilled out of my cereal.",
        "I'm a detective.  I will detect.",
    ]

    if message.content == '99!':
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(response)

client.run(BOT_TOKEN)
