from archus.response import Response
from archus.status import HTTPStatus

def handel_user(request):
    return Response(HTTPStatus.OK,{"message":"working"})

def handel_me(request):
    print(request.json)
    return Response(HTTPStatus.OK,{"message":"hello its me"})