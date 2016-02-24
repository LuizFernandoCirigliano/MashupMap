import requests
from MashupMap.models import Artist

my_cache = {}


def get_artist(artist_name):
    if artist_name in my_cache:
        return my_cache.get(artist_name)

    r = requests.get(
        'https://itunes.apple.com/search',
        params={
            "term": artist_name,
            "limit": 1
        })
    if r.status_code != 200:
        raise NameError('API Error')

    response = r.json()
    if response.get('resultCount', 0) == 0:
        return None

    artist_json = response.get('results')[0]
    artist_name_norm = artist_json.get('artistName')
    artist_id = artist_json.get('artistId')
    artwork = artist_json.get('artworkUrl100')

    if artist_id is None or artist_name is None:
        return None

    new_artist = Artist(artist_id, artist_name_norm, artwork)
    my_cache[artist_name] = new_artist
    return new_artist
