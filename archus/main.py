from .router import Router
from .request import Request
from .response import Response
from jinja2 import Environment, FileSystemLoader, select_autoescape,TemplateNotFound
from .status import HTTPStatus
import mimetypes
from archus.file_handlers import StaticFileHandler,MediaFileHandler
from archus.middleware.GlobalExceptionMiddleware import GlobalExceptionHandlerMiddleware
from archus.exceptions import ArchusException
from archus.middleware import Middleware
from datetime import datetime

class Archus:
    def __init__(self,media_dir:str="media",static_dir:str="static",template_dir:str="templates"):
        self.router = Router()
        self.middleware = []
        self.template_env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )

        self.static_handler=StaticFileHandler(static_dir)
        self.media_handler=MediaFileHandler(media_dir)
        self.middleware.append(GlobalExceptionHandlerMiddleware)

    def route(self, path:str, method:str):
        def wrapper(handler):
            self.router.add_route(path, method, handler)
            return handler
        return wrapper
    
    def register_blueprint(self, prefix, blueprint):
        for route in blueprint:
            route_path = route['path']
            full_path = f"{prefix}{route_path}"
            self.router.add_route(full_path, route['method'], route['handler'])
        return self

    def add_middleware(self, middleware_cls:Middleware):
        self.middleware.append(middleware_cls)

    def _apply_middleware(self, app):
        for middleware_cls in reversed(self.middleware):
            app = middleware_cls(app)
        return app
    
    def redirect(self, location, status=HTTPStatus.FOUND):
        header = [('Location', location),('redirection',True)]
        return Response(status, '',content_type='text/html; charset=utf-8', headers=header)

    def _serve_static(self, request):
        filename = request.path.split('/')[len(request.path.split('/'))-1]
        content = self.static_handler.serve_file(filename)
        if content:
            content_type, _ = mimetypes.guess_type(filename)
            if content_type is None:
                content_type = 'application/octet-stream'
            return Response(HTTPStatus.OK, content, content_type)
        else:
            return Response(HTTPStatus.NOT_FOUND, 'Not Found')
    
    def _serve_media(self, request):
        filename = request.path.split('/')[len(request.path.split('/'))-1]
        content = self.media_handler.serve_file(filename)
        if content:
            content_type, _ = mimetypes.guess_type(filename)
            if content_type is None:
                content_type = 'application/octet-stream'
            return Response(HTTPStatus.OK, content, content_type)
        else:
            return Response(HTTPStatus.NOT_FOUND, 'Not Found')


    def _render_template(self, template_name, **context):
        try:
            template = self.template_env.get_template(template_name)
            rendered_content = template.render(**context).encode('utf-8')
            return Response(HTTPStatus.OK, rendered_content, 'text/html; charset=utf-8')
        except TemplateNotFound:
            return Response(HTTPStatus.NOT_FOUND, 'Template Not Found')
    
    def _app(self,environ, start_response):
        try:
            request = Request(environ)
            if request.path.startswith('/static/'):
                response = self._serve_static(request)

            elif request.path.startswith('/media/'):
                response = self._serve_media(request)

            else:
                response = self.router.handle_request(request)
                if isinstance(response, dict) and 'template' in response:
                    response=self._render_template(response['template'], **response.get('context', {}))

            start_response(response.status, response.headers)

            if type(response.body)==str:
                return [response.body.encode()]
            
            return [response.body]
        
        except ArchusException as e:
            raise e
        
        except Exception as e:
            raise ArchusException(message=f"Unexpected error: {str(e)}",status=HTTPStatus.INTERNAL_SERVER_ERROR)

    def __call__(self, environ, start_response):
        app = self._apply_middleware(self._app)
        return app(environ, start_response)
    
    def run(self,dev:bool=True,host:str="127.0.0.1",port:int=8000):
        import subprocess
        if dev:
            try:
                command = [
                    'pip', 
                    'install', 
                    'waitress'
                ]
                subprocess.run(command, check=True)
            except subprocess.CalledProcessError as e:
                print(str(e))
            except Exception as e:
                print(str(e))

            from waitress import serve

            try:
                print(f"Dev Server Running on http://{host}:{port} at {datetime.now()}")
                serve(self,host=host,port=port)
            except Exception as e:
                print(e)

        else:
            try:
                command = [
                    'pip', 
                    'install', 
                    'gunicorn'
                ]
                subprocess.run(command, check=True)
            except subprocess.CalledProcessError as e:
                print(str(e))
            except Exception as e:
                print(str(e))

            command = [
                'gunicorn', 
                '-c', 
                'gunicorn_config.py',  
                'app:application' 
            ]

            try:
                subprocess.run(command, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error running Gunicorn: {e}")
            except KeyboardInterrupt:
                exit()
