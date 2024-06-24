from archus.response import Response
from archus.status import HTTPStatus

def auth(request):
    return Response(HTTPStatus.OK,{"message":"login"})