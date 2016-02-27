import requests
import MashupMap.models as models
from MashupMap import db


def get_artist(artist_name):
    artist = models.Artist.query.filter_by(name=artist_name).first()
    if artist is not None:
        return artist

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
    artwork = artist_json.get('artworkUrl60')

    if artist_id is None or artist_name is None:
        return None

    artist = models.get_or_create_by_id(
        db.session,
        models.Artist,
        artist_id,
        name=artist_name_norm,
        imageURL=artwork
        )

    return artist
