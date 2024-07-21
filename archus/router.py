import re
from .response import Response
from .status import HTTPStatus
from .exceptions import ArchusException
from .core import resolve_handler_dependencies

class Router:
    def __init__(self):
        self.routes = []

    def add_route(self, path, method, handler):
        path_pattern = re.sub(r'<(\w+)>', r'(?P<\1>[^/]+)', path)
        if path.endswith('/') and len(path) > 1:
            path_pattern = path_pattern.rstrip('/') + '/?$'
        else:
            path_pattern = path_pattern + '/?$'
        path_regex = re.compile(f'^{path_pattern}$')
        self.routes.append((path_regex, method, handler))

    def handle_request(self, request):
        for path_regex, method, handler in self.routes:
            match = path_regex.match(request.path)
            if match:
                if (not request.method in method) and not request.headers.get('http_referer'):
                    return Response(HTTPStatus.METHOD_NOT_ALLOWED, 'Method Not Allowed')
                
                request.path_params = match.groupdict()
                dependencies = resolve_handler_dependencies(handler, request)
                return handler(request, **dependencies, **request.path_params)

        return Response(HTTPStatus.NOT_FOUND, 'Not Found')
