from gateway import generate_comparison
from getgiphygif import get_giphy_gif
import random

FUN_GIF_CATEGORIES = {
    'LOW':['Happy!', 'Joy', 'Cheers'],
    'MIDDLE':['meh', 'mediocre'],
    'HIGH':['high score', 'ruh roh', 'whoops', 'yikes'],
    'UNKNOWN':['shrug', 'idk', 'idk lol', 'uhhhhhhhh', 'hmmmmmmm']
}

THRESHOLDS = {
    'LOW':25,
    'HIGH':75
}

def make_name_response(name_query):
    response = {}
    response['base_data'] = generate_comparison(name_query)
    response = make_fun_gifs(response)
    return response
    
def make_fun_gifs(response):

    perc = response['base_data']['ratio_percentile']
    if perc == 'unknown':
        perc_gif_q = random.choice(FUN_GIF_CATEGORIES['UNKNOWN'])

    elif float(perc) >= THRESHOLDS['LOW']:
        if float(perc) <= THRESHOLDS['HIGH']:
            perc_gif_q = random.choice(FUN_GIF_CATEGORIES['MIDDLE'])

        else:
            perc_gif_q = random.choice(FUN_GIF_CATEGORIES['HIGH'])

    else:
        perc_gif_q = random.choice(FUN_GIF_CATEGORIES['LOW'])

    perc_gif = get_giphy_gif(perc_gif_q)

    response['gif'] = {
        'percentile_gif':perc_gif
    }
    
    return response

if __name__ == "__main__":
    print(make_name_response('wei'))