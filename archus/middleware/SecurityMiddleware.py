from .main import Middleware

class SecurityHeadersMiddleware(Middleware):
    def __init__(self, app,BASE_DIR=None):
        super().__init__(app,BASE_DIR=BASE_DIR)

    def __call__(self, environ, start_response):
        def custom_start_response(status, headers, exc_info=None):
            headers.append(('X-Content-Type-Options', 'nosniff'))
            headers.append(('X-Frame-Options', 'DENY'))
            headers.append(('X-XSS-Protection', '1; mode=block'))
            headers.append(('Strict-Transport-Security', 'max-age=31536000; includeSubDomains'))
            return start_response(status, headers, exc_info)
        
        response=super().__call__(environ, custom_start_response)
        return response