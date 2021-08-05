import os

GOOGLE_AUTH_CREDENTIALS = {
    'SCOPE': [
        'profile',
        'email',
    ],
    'AUTH_PARAMS': {
        'access_type': 'online',
    },
    'APP': {
        'client_id': '978963988712-pd6pvcoa3snpmt9kj74qkg7svv7bf815.apps.googleusercontent.com',
        'secret': os.environ.get('AUTH_GOOGLE_SECRET'),
    }
}
