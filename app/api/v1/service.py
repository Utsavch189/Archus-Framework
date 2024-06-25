from archus.response import Response
from archus.status import HTTPStatus
from archus.exceptions import ArchusException

def handel_user(request):
    # raise ArchusException(status=HTTPStatus.NOT_ACCEPTABLE,message="user not exists!")
    return Response(HTTPStatus.OK,{"message":"working"})

def handel_me(request):
    print(request.json)
    return Response(HTTPStatus.OK,{"message":"hello its me"})