from .service import auth

v2_urls=[
    {'path': '/auth', 'method': ['GET'], 'handler': auth}
]
