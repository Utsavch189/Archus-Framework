from .service import index,about

urls=[
    {'path': '/', 'method': ['GET'], 'handler': index},
    {'path': 'about', 'method': ['GET'], 'handler': about},
]