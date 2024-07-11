class Middleware:
    def __init__(self, app,BASE_DIR=None):
        self.app = app
        self.BASE_DIR=BASE_DIR

    def __call__(self, environ, start_response):

        response = self.app(environ, start_response)
        return response
