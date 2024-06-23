class Middleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        def custom_start_response(status, headers, exc_info=None):
            return start_response(status, headers, exc_info)

        response = self.app(environ, custom_start_response)
        return response
