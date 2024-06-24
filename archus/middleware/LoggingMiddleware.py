from archus.middleware.main import Middleware

class LoggingMiddleware(Middleware):
    def __init__(self, app):
        super().__init__(app)

    def __call__(self, environ, start_response):
        # print(f"Request: {environ['REQUEST_METHOD']} {environ['PATH_INFO']}")

        def custom_start_response(status, headers, exc_info=None):
            # print(f"Response status: {status}")
            return start_response(status, headers, exc_info)

        response=super().__call__(environ, custom_start_response)
        return response