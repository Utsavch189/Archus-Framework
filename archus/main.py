from .router import Router
from .request import Request
from .response import Response
from jinja2 import Environment, FileSystemLoader, select_autoescape,TemplateNotFound
from .status import HTTPStatus
import mimetypes
from archus.file_handlers import StaticFileHandler,MediaFileHandler
from archus.middleware.order_middleware import check_middleware_stack
from archus.exceptions import ArchusException
from archus.middleware import Middleware
from datetime import datetime
from archus.docs import index

import os,sys

try:
    import config
except Exception as e:
    print(e)

class Archus:
    def __init__(self):
        self._router = Router()
        self._middleware = []
        self._dir=None

        self.BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        sys.path.append(self.BASE_DIR)
        
        self._router.add_route(
            path="/docs",
            method=['GET'],
            handler=index
        )

        if config.KEY=="":
            raise Exception("Application Key Not Found!")
        
        _static_dir=self.BASE_DIR+"/"+config.STATIC_DIR or self.BASE_DIR+"/"+"static"
        _media_dir=self.BASE_DIR+"/"+config.MEDIA_DIR or self.BASE_DIR+"/"+"media"
        _template_dir=self.BASE_DIR+"/"+config.TEMPLATE_DIR or self.BASE_DIR+"/"+"templates"

        self._template_env = Environment(
            loader=FileSystemLoader(_template_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )

        self._static_handler=StaticFileHandler(_static_dir)
        self._media_handler=MediaFileHandler(_media_dir)


    def route(self, path:str, method:str):
        def wrapper(handler):
            self._router.add_route(path, method, handler)
            return handler
        return wrapper
    
    def register_blueprint(self, prefix, blueprint):
        for route in blueprint:
            route_path = route['path']
            full_path = f"{prefix}{route_path}"
            self._router.add_route(full_path, route['method'], route['handler'])
        return self

    def add_middleware(self, middleware_cls:Middleware):
        self._middleware.append(middleware_cls)
        if self._middleware:
            check_middleware_stack(self._middleware)

    def _apply_middleware(self, app):
        for middleware_cls in reversed(self._middleware):
            _app = middleware_cls(app)
        return _app
    
    def redirect(self, location, status=HTTPStatus.FOUND):
        header = [('Location', location),('redirection',True)]
        return Response(status, '',content_type='text/html; charset=utf-8', headers=header)

    def _serve_static(self, request):
        filename = request.path.split('/')[len(request.path.split('/'))-1]
        content = self._static_handler.serve_file(filename)
        if content:
            content_type, _ = mimetypes.guess_type(filename)
            if content_type is None:
                content_type = 'application/octet-stream'
            if content_type=='application/x-css':
                content_type='text/css'
            return Response(HTTPStatus.OK, content, content_type)
        else:
            return Response(HTTPStatus.NOT_FOUND, 'Not Found')
    
    def _serve_media(self, request):
        filename = request.path.split('/')[len(request.path.split('/'))-1]
        content = self._media_handler.serve_file(filename)
        if content:
            content_type, _ = mimetypes.guess_type(filename)
            if content_type is None:
                content_type = 'application/octet-stream'
            return Response(HTTPStatus.OK, content, content_type)
        else:
            return Response(HTTPStatus.NOT_FOUND, 'Not Found')


    def _render_template(self, template_name,dir=None, **context):
        try:

            if dir:
                _template_env = Environment(
                    loader=FileSystemLoader(self.BASE_DIR+"/"+dir),
                    autoescape=select_autoescape(['html', 'xml'])
                )
                _template = _template_env.get_template(template_name)
                _rendered_content = _template.render(**context).encode('utf-8')
                return Response(HTTPStatus.OK, _rendered_content, 'text/html; charset=utf-8')
        
            _template = self._template_env.get_template(template_name)
            _rendered_content = _template.render(**context).encode('utf-8')
            return Response(HTTPStatus.OK, _rendered_content, 'text/html; charset=utf-8')
        except TemplateNotFound:
            return Response(HTTPStatus.NOT_FOUND, 'Template Not Found')
    
    def _app(self,environ, start_response):
        try:
            _request = Request(environ)
            if _request.path.startswith('/static/'):
                _response = self._serve_static(_request)

            elif _request.path.startswith('/media/'):
                _response = self._serve_media(_request)
            
            elif _request.path == '/favicon.ico': 
                _response = self._serve_static(_request)

            else:
                _response = self._router.handle_request(_request)
                if isinstance(_response, dict) and 'template' in _response:
                    _response=self._render_template(_response['template'], **_response.get('context', {}))

                elif isinstance(_response, dict) and 'docs' in _response:
                    _response=self._render_template(_response['docs'],dir="archus/docs", **_response.get('context', {}))

            start_response(_response.status, _response.headers)

            if type(_response.body)==str:
                return [_response.body.encode()]
            
            return [_response.body]
        
        except ArchusException as e:
            raise e
        
        except Exception as e:
            raise ArchusException(message=f"Unexpected error: {str(e)}",status=HTTPStatus.INTERNAL_SERVER_ERROR)

    def __call__(self, environ, start_response):
        _app = self._apply_middleware(self._app)
        return _app(environ, start_response)
    
    def run(self,dev:bool=True,host:str="127.0.0.1",port:int=8000,gunicron_command:list=['gunicorn','-c', 'gunicorn_config.py',  'app:application' ]):
        import subprocess
        if dev:
            from waitress import serve

            try:
                print(f"Dev Server Running on http://{host}:{port} at {datetime.now()}")
                serve(self,host=host,port=port)
            except Exception as e:
                print(e)

        else:
            try:
                subprocess.run(gunicron_command, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error running Gunicorn: {e}")
            except KeyboardInterrupt:
                exit()
