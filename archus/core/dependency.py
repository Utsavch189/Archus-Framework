from inspect import signature
from ..serializer import ArchusSerializer


def resolve_handler_dependencies(handler,request):
    dependencies = {}
    sig = signature(handler)

    for param in sig.parameters.values():
        if issubclass(param.annotation, ArchusSerializer):
            serializer_class = param.annotation
            serializer = serializer_class()
            data = serializer.deserialize(request.json)
            dependencies[param.name] = data

    return dependencies
