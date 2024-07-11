from ..response import Response
from ..status import HTTPStatus
from ..exceptions import ArchusException
from .main import Middleware

class GlobalExceptionHandlerMiddleware(Middleware):
    def __init__(self, app,BASE_DIR=None):
        super().__init__(app,BASE_DIR=BASE_DIR)

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