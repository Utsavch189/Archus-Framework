from archus.middleware.main import Middleware

class CORSMiddleware(Middleware):
    def __init__(self, app, allowed_origins=None, allowed_methods=None, allowed_headers=None):
        super().__init__(app)
        self.allowed_origins = allowed_origins or ['*']
        self.allowed_methods = allowed_methods or ['GET', 'POST', 'OPTIONS','PUT','DELETE','PATCH']
        self.allowed_headers = allowed_headers or ['Content-Type']

    def __call__(self, environ, start_response):
        def custom_start_response(status, headers, exc_info=None):
            origin = environ.get('HTTP_ORIGIN', '')
            if origin in self.allowed_origins or '*' in self.allowed_origins:
                headers.append(('Access-Control-Allow-Origin', origin))
            headers.append(('Access-Control-Allow-Methods', ', '.join(self.allowed_methods)))
            headers.append(('Access-Control-Allow-Headers', ', '.join(self.allowed_headers)))
            return start_response(status, headers, exc_info)

        if environ['REQUEST_METHOD'] == 'OPTIONS':
            response_body = b''
            status = '200 OK'
            headers = [
                ('Content-Length', '0'),
            ]
            origin = environ.get('HTTP_ORIGIN', '')
            if origin in self.allowed_origins or '*' in self.allowed_origins:
                headers.append(('Access-Control-Allow-Origin', origin))
            headers.append(('Access-Control-Allow-Methods', ', '.join(self.allowed_methods)))
            headers.append(('Access-Control-Allow-Headers', ', '.join(self.allowed_headers)))
            start_response(status, headers)
            return [response_body]

        return super().__call__(environ, custom_start_response)
