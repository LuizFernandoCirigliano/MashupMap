import requests


def get_artist(artist_name):
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

    response = response.get('results')

    return response[0].get('artistName')
