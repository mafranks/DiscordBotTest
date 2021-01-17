'''
Main file for discord bot. Functionality TBD.
'''

import os
from pathlib import Path
from dotenv import load_dotenv
import discord

# Providing the path to a .env file that contains the credentials
load_dotenv(dotenv_path=Path('.', '.env'))

# Pull in the credentials
BOT_TOKEN = os.getenv('BOT_TOKEN')
GUILD_NAME = os.getenv('GUILD_NAME')

# Intents gives the bot permissions
intents = discord.Intents.all()

# Connect to the Discord server (guild)
client = discord.Client(intents=intents)

def display_server_information(guild):
    '''Display the server information'''
    # Print the bot and guild information
    print(f'{client.user} is connected to:\n\t{guild.name} (id: {guild.id})')
    menu(guild)

def display_users(guild):
    '''Display the users on the server'''
    # Find and print all of the guild members
    members = '\n - '.join([member.name for member in guild.members])
    '''
    The list comprehension [member.name for member in guild.members] could also be
    written like this:

    members = []
    for member in guild.members:
        members.append('\n - '.join(member.name))
    '''
    print(f'Guild Members:\n - {members}')
    menu(guild)

def menu(guild):
    '''Display the menu'''
    print(f"\n\n{30 * '-'}")
    print(f'Please make a selection and {client.user} will comply:')
    print(30 * '-')
    print("[1] Display Server Information")
    print("[2] Display Users")
    print(f"{30 * '-'}\n\n")

    ## Get input ###
    choice = input('Enter your numerical choice from above: ')

    ### Convert string to int type ##
    choice = int(choice)

    ### Take action as per selected menu-option ###
    if choice == 1:
        display_server_information(guild)
    elif choice == 2:
        display_users(guild)
    else:    ## default ##
        print("Invalid number. Select one of the available options.")

@client.event
async def on_ready():
    '''
    Define the guild and call the menu when the bot connects to the server (guild)
    '''
    # Loop through all the servers and look for one that matches the GUILD_NAME
    guild = discord.utils.find(lambda guild: guild.name == GUILD_NAME, client.guilds)

    menu(guild)

client.run(BOT_TOKEN)
