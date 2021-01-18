'''
Main file for discord bot. Functionality TBD.
'''

# TODO - Add Google Search
# TODO - Add meme making
# TODO - Add stock prices
# TODO - Add logging

import os
import random
from pathlib import Path
import json
import logging
from dotenv import load_dotenv
import discord
import requests
import text_blobs

# Set up the logging formatting can't use f-strings
logger = logging.getLogger('discord_bot')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('discord_bot.log')
file_handler.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.info('Seting up the Environment varibles')
load_dotenv(dotenv_path=Path('.', '.env'))

logger.info('Pulling in the credentials')
BOT_TOKEN = os.getenv('BOT_TOKEN')
GUILD_NAME = os.getenv('GUILD_NAME')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
X_RAPIDAPI_KEY = os.getenv('X_RAPIDAPI_KEY')

logger.info('Providing permissions to the bot')
intents = discord.Intents.all()

logger.info('Connecting to the Discord server (guild)')
client = discord.Client(intents=intents)

def display_server_information(guild):
    '''Display the server information'''
    logger.info('Printing the bot and guild information')
    print(f'{client.user} is connected to:\n\t{guild.name} (id: {guild.id})')

def display_users(guild):
    '''Display the users on the server'''
    logger.info('Finding and printing all of the guild members')
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

def get_weather(message):
    '''Query Open Weather Map API for the provided city'''
    logger.info('Using the Open Weather Map API to pull weather info')
    error_message = 'Improper formatting. Example:  weather! indianaplis,us'
    if len(message.content.split(' ')) != 2:
        logger.debug('Incorrect format for weather request.')
        return message.content, error_message
    city_country = message.content.split(' ')[1]
    if len(city_country.split(',')) != 2:
        logger.debug('Incorect format for weather request')
        return message.content, error_message

    url = "https://community-open-weather-map.p.rapidapi.com/forecast"

    querystring = {"q":city_country, "units":'"imperial"'}

    headers = {
        'x-rapidapi-key': X_RAPIDAPI_KEY,
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code == 200:
        logger.info('Received 200 response from Weather API')
        json_data = json.loads(response.text)
        temp_info = json_data['list'][0]['main']
        return city_country, temp_info
    if response.status_code == 429:
        logger.info('Hit rate limit for Weather API.')
        return city_country, "Weather API Rate Limit Reached. Try again later."
    return city_country, response.status_code

@client.event
async def on_ready():
    '''
    Main function to view options on the CLI
    '''
    logger.info('Looping through all the servers and looking for GUILD_NAME')
    guild = discord.utils.get(client.guilds, name=GUILD_NAME)
    display_server_information(guild)
    display_users(guild)

@client.event
async def on_member_join(member):
    '''Welcome new members'''
    logger.info('New member joined.  Sending welcome message.')
    await member.create_dm()
    await member.dm_channel.send(f"Hello {member.name}, welcome to the server.")

@client.event
async def on_message(message):
    '''Handle events for posted messages'''
    # Ignore messages from the bot to avoid a loop
    if message.author == client.user:
        return

    if message.content.startswith('99!'):
        logging.info('Brooklyn 99 quote functionality was called')
        response = random.choice(text_blobs.BROOKLYN_99_QUOTES)
        await message.channel.send(response)

    if message.content.startswith('weather!'):
        logging.info('Weather request was received')
        city_country, response = get_weather(message)
        if city_country == message.content:
            logging.debug('Recevied error for weather request')
            await message.channel.send(response) #In this case response is the error message
        elif isinstance(response, int):
            logging.debug('API request returned a %i status code.', response)
            await message.channel.send(f"API Request returned a {response} status code.")
        elif isinstance(response, str):
            logging.info('Received error for weather request: %s', response)
            await message.channel.send(response)
        else:
            # Temp info is returned in Kelvin for some unknown reason so we must convert
            temp_fahrenheit = round(32 + ((int(response['temp']) - 273.15) * 1.8), 2)
            await message.channel.send(f"Current temp in {city_country} is {temp_fahrenheit}° F")
            logging.info('Weather response successfully processed')

    if message.content.startswith('help!'):
        await message.channel.send(text_blobs.HELP_MENU)

client.run(BOT_TOKEN)
