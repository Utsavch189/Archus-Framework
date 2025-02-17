from inspect import signature
from ..serializer import ArchusSerializer
from ..exceptions import ArchusException
from ..status import HTTPStatus

def resolve_handler_dependencies(handler,request):
    dependencies = {}
    sig = signature(handler)

    for param in sig.parameters.values():
        if issubclass(param.annotation, ArchusSerializer):
            serializer_class = param.annotation
            serializer = serializer_class()
            if not request.json:
                raise ArchusException(HTTPStatus.UNPROCESSABLE_ENTITY,message=serializer.deserialize({}))
            data = serializer.deserialize(request.json)
            dependencies[param.name] = data

    return dependencies
