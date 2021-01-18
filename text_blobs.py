'''Location for all the text blurbs and lists required'''

BROOKLYN_99_QUOTES = [
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

HELP_MENU = '''

HELP MENU:

99! - returns a random Brooklyn 99 quote
    Example: 99!

weather! - returns the current temperature for a city
    Example: weather! indianapolis,us
    Note: Must specify city and 2 digit country code with no spaces in between

help! - displays this help menu
    Example: help!
'''

# Example first entry of the weather response.  Can add more info to the output later
'''
{'cod': '200', 'message': 0, 'cnt': 40, 'list': [{'dt': 1610928000,
'main': {'temp': 272.2, 'feels_like': 267.25, 'temp_min': 271.34,
'temp_max': 272.2, 'pressure': 1008, 'sea_level': 1008, 'grnd_level': 983,
'humidity': 88, 'temp_kf': 0.86}, 'weather': [{'id': 600, 'main': 'Snow',
'description': 'light snow', 'icon': '13n'}], 'clouds': {'all': 94},
'wind': {'speed': 3.72, 'deg': 257}, 'visibility': 3498, 'pop': 0.55,
'snow': {'3h': 0.19}, 'sys': {'pod': 'n'}, 'dt_txt': '2021-01-18 00:00:00'}]}
'''
