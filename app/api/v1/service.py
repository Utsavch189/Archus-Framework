from archus.response import Response
from archus.status import HTTPStatus
from archus.exceptions import ArchusException
from .serializer import UserSerializer

def handel_user(request):
    # raise ArchusException(status=HTTPStatus.NOT_ACCEPTABLE,message="user not exists!")
    return Response(HTTPStatus.OK,{"message":"working"})

def handel_me(request):
    serializer=UserSerializer()
    data=serializer.deserialize(request.json)
    return Response(HTTPStatus.OK,{"message":"hello its me","data":data})