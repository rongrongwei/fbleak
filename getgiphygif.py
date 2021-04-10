import requests
import json
from SECRET import giphyapikey

def get_giphy_gif(query):
    URL = f"https://api.giphy.com/v1/gifs/search?api_key={giphyapikey}&q={query}&limit=1&offset=0&rating=g&lang=en"
    s = requests.session()
    response = s.get(URL)
    if response.status_code == 200:
        giphy_url = json.loads(response.content)['data'][0]['embed_url']
    else:
        giphy_url = 'https://giphy.com/embed/YQitE4YNQNahy'

    return giphy_url
