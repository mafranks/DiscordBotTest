'''
Main file for discord bot. Functionality TBD.
'''

import os
import random
from pathlib import Path
import json
from dotenv import load_dotenv
import discord
import requests

# Providing the path to a .env file that contains the credentials
load_dotenv(dotenv_path=Path('.', '.env'))

# Pull in the credentials
BOT_TOKEN = os.getenv('BOT_TOKEN')
GUILD_NAME = os.getenv('GUILD_NAME')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
X_RAPIDAPI_KEY = os.getenv('X_RAPIDAPI_KEY')

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

def get_weather(message):
    '''Query Open Weather Map API for the provided city'''
    error_message = 'Improper formatting. Example:  weather! indianaplis,us'
    if len(message.content.split(' ')) != 2:
        return message.content, error_message
    city_country = message.content.split(' ')[1]
    if len(city_country.split(',')) != 2:
        return message.content, error_message

    url = "https://community-open-weather-map.p.rapidapi.com/forecast"

    querystring = {"q":city_country, "units":'"imperial"'}

    headers = {
        'x-rapidapi-key': X_RAPIDAPI_KEY,
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code == 200:

        json_data = json.loads(response.text)
        # Example first entry of the response.  Can add more info to the output later
        '''
        {'cod': '200', 'message': 0, 'cnt': 40, 'list': [{'dt': 1610928000,
        'main': {'temp': 272.2, 'feels_like': 267.25, 'temp_min': 271.34,
        'temp_max': 272.2, 'pressure': 1008, 'sea_level': 1008, 'grnd_level': 983,
        'humidity': 88, 'temp_kf': 0.86}, 'weather': [{'id': 600, 'main': 'Snow',
        'description': 'light snow', 'icon': '13n'}], 'clouds': {'all': 94},
        'wind': {'speed': 3.72, 'deg': 257}, 'visibility': 3498, 'pop': 0.55,
        'snow': {'3h': 0.19}, 'sys': {'pod': 'n'}, 'dt_txt': '2021-01-18 00:00:00'}]}
        '''
        temp_info = json_data['list'][0]['main']
        return city_country, temp_info
    if response.status_code == 429:
        return city_country, "Weather API Rate Limit Reached. Try again later."
    return city_country, response.status_code

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

    if message.content.startswith('99!'):
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(response)

    if message.content.startswith('weather!'):
        city_country, response = get_weather(message)
        if city_country == message.content:
            await message.channel.send(response) #In this case response is the error message
        elif isinstance(response, int):
            await message.channel.send(f"API Request returned a {response} status code.")
        elif isinstance(response, str):
            await message.channel.send(response)
        else:
            # Temp info is returned in Kelvin for some unknown reason so we must convert
            temp_fahrenheit = round(32 + ((int(response['temp']) - 273.15) * 1.8), 2)
            await message.channel.send(f"Current temp in {city_country} is {temp_fahrenheit}° F")

    if message.content.startswith('help!'):
        help_menu = '''
        HELP MENU:
        
        99! - returns a random Brooklyn 99 quote
            Example: 99!

        weather! - returns the current temperature for a city
            Example: weather! indianapolis,us
            Note: Must specify city and 2 digit country code with no spaces in between

        help! - displays this help menu
            Example: help!
        '''
        await message.channel.send(help_menu)

client.run(BOT_TOKEN)
