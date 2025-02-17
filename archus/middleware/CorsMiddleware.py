from .main import Middleware
import os,sys

class CORSMiddleware(Middleware):
    def __init__(self, app, BASE_DIR=None,allowed_origins=None, allowed_methods=None, allowed_headers=None):
        super().__init__(app,BASE_DIR=BASE_DIR)

        sys.path.append(self.BASE_DIR)

        try:
            import config
        except ImportError:
            config = None

        self.allowed_origins = config.ALLOWED_ORIGINS #or ['*']
        self.allowed_methods = config.ALLOWED_METHODS #or ['GET', 'POST', 'OPTIONS','PUT','DELETE','PATCH']
        self.allowed_headers = config.ALLOWED_HEADERS  #or ['Content-Type']

    def __call__(self, environ, start_response):
        origin = environ.get('HTTP_ORIGIN', '')
    
        def custom_start_response(status, headers, exc_info=None):
            if origin in self.allowed_origins or '*' in self.allowed_origins:
                headers.append(('Access-Control-Allow-Origin', origin))
            headers.append(('Access-Control-Allow-Methods', ', '.join(self.allowed_methods)))
            headers.append(('Access-Control-Allow-Headers', ', '.join(self.allowed_headers)))
            return start_response(status, headers, exc_info)
    
        if environ['REQUEST_METHOD'] == 'OPTIONS':
            status = '200 OK'
            headers = [
                ('Content-Length', '0'),
                ('Access-Control-Allow-Origin', origin if origin in self.allowed_origins or '*' in self.allowed_origins else ''),
                ('Access-Control-Allow-Methods', ', '.join(self.allowed_methods)),
                ('Access-Control-Allow-Headers', ', '.join(self.allowed_headers)),
            ]
            start_response(status, headers)
            return [b'']
    
        return super().__call__(environ, custom_start_response)
