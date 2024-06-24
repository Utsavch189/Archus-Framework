from archus.response import Response
from archus.status import HTTPStatus

def index(request):
    context = {
            'title': 'Home Page',
            'heading': 'Welcome to my Framework!',
            'items': ['Item 1', 'Item 2', 'Item 3']
        }
    return {'template': 'index.html', 'context': context}

def about(request):
    return {'template': 'about.html'}