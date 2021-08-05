import os

SPOTIFY_AUTH_CREDENTIALS = {
    'APP': {
        'client_id': 'a069d95aa15b4f7e9f99e8bb793c0705',
        'secret': os.environ.get('AUTH_SPOTIFY_SECRET'),
    }
}
