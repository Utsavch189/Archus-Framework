from archus.response import Response
from archus.status import HTTPStatus
from archus.exceptions import ArchusException
from archus.middleware.main import Middleware

class GlobalExceptionHandlerMiddleware(Middleware):
    def __init__(self, app):
        super().__init__(app)

    def __call__(self, environ, start_response):
        try:
            return super().__call__(environ, start_response)
        
        except ArchusException as e:
            response = Response(
                status=e.status,
                body=e.to_dict(),
                content_type="application/json"
            )
            start_response(response.status, response.headers)
            return [response.body.encode()]
        
        except Exception as e:
            response = Response(
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
                body={"type": "Internal Server Error","message":str(e)},
                content_type="application/json"
            )
            start_response(response.status, response.headers)
            return [response.body.encode()]