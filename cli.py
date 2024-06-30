import os
import sys
import argparse

def create_project_structure(project_name):
    # Define the folder structure
    folders = [
        f"{project_name}",
        f"{project_name}/app",
        f"{project_name}/app/api",
        f"{project_name}/app/api/v1",
        f"{project_name}/app/templating",
        f"{project_name}/static",
        f"{project_name}/templates",
        f"{project_name}/media"
    ]

    # Create the folders
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
    
    # Create some example files
    init_files = [
        f"{project_name}/app/__init__.py",
        f"{project_name}/app/app.py",
        f"{project_name}/app/gunicorn_config.py",
        f"{project_name}/app/api/__init__.py",
        f"{project_name}/app/api/v1/__init__.py",
        f"{project_name}/app/api/v1/routes.py",
        f"{project_name}/app/api/v1/serializer.py",
        f"{project_name}/app/api/v1/service.py",
        f"{project_name}/app/templating/__init__.py",
        f"{project_name}/app/templating/routes.py",
        f"{project_name}/app/templating/service.py",
        f"{project_name}/config.py",
        f"{project_name}/run.py",
        f"{project_name}/static/.gitkeep",
        f"{project_name}/templates/index.html",
        f"{project_name}/media/.gitkeep",
    ]

    file_contents=[
        # f"{project_name}/app/__init__.py"
        '''
        from app.app import application
        ''',

        # f"{project_name}/app/app.py"
        '''
        from archus import Archus\nfrom archus.middleware import LoggingMiddleware, SecurityHeadersMiddleware,CORSMiddleware,GlobalExceptionHandlerMiddleware

        \nfrom app.api.v1.routes import v1_urls\nfrom app.templating.routes import urls

        \napplication = Archus()

        \napplication.add_middleware(SecurityHeadersMiddleware)\napplication.add_middleware(CORSMiddleware)\napplication.add_middleware(LoggingMiddleware)\napplication.add_middleware(GlobalExceptionHandlerMiddleware)

        \napplication.register_blueprint("/api/v1",v1_urls)\napplication.register_blueprint("/",urls)
        '''
        ,

        # f"{project_name}/app/gunicorn_config.py"
        '''
        bind = '0.0.0.0:8000'  # Bind to localhost on port 8000\nworkers = 4  # Number of worker processes\nworker_connections = 1000  # Number of connections per worker\ntimeout = 30  # Timeout for handling requests
        ''',

        # f"{project_name}/app/api/__init__.py"
        '''
            # empty
        ''',

        # f"{project_name}/app/api/v1/__init__.py"
        '''
            # empty
        ''',

        # f"{project_name}/app/api/v1/routes.py"
        '''
        from .service import index\n\nv1_urls=[
        {'path': '/', 'method': ['GET'], 'handler': index}
    ]
        ''',

        # f"{project_name}/app/api/v1/serializer.py"
        '''
            # empty
        ''',

        # f"{project_name}/app/api/v1/service.py"
        '''
        from archus.response import Response\nfrom archus.status import HTTPStatus\n\ndef index(request):
        return Response(HTTPStatus.OK,{"message":"api is running..."})
        ''',

        # f"{project_name}/app/templating/__init__.py"
        '''
            # empty
        ''',

        # f"{project_name}/app/templating/routes.py"
        '''
        from .service import index\n\nurls=[
        {'path': '/', 'method': ['GET'], 'handler': index}
    ]
        ''',

        # f"{project_name}/app/templating/service.py"
        '''
        def index(request):\n\treturn {'template': 'index.html'}
        ''',

        # f"{project_name}/config.py"
        '''
        # SERVER KEY\n\n"SECRET KEY.USE YOUR RANDOM KEY FOR SECURITY."\nKEY="928635e70a014b41bfd38a66cf6a1939"\n\n# SMTP\n"SMTP_USE_TLS=True WILL AUTOMATICALLY DETECT PORT 587.SMTP_USE_SSL=TRUE WILL AUTOMATICALLY DETECT PORT 465."\n\nSMTP_SERVER = ''\nSMTP_USE_TLS=True\nSMTP_USE_SSL=False\nSMTP_USERNAME = ''\nSMTP_PASSWORD = ''\n\n# CORS\nALLOWED_ORIGINS=['*']\nALLOWED_METHODS=[ 'POST', 'OPTIONS','PUT','DELETE','PATCH']\nALLOWED_HEADERS=['Content-Type']\n\n# Throttling\nMAX_REQUESTS=10\nPERIOD=60 # Seconds\n\n# Dirs\nTEMPLATE_DIR="templates"\nSTATIC_DIR="static"\nMEDIA_DIR="media"\nLOG_DIR="log"
        ''',

        # f"{project_name}/run.py"
        '''
        from app import application\n\nif __name__=="__main__":\n\tapplication.run()
        '''
        
        # f"{project_name}/static/.gitkeep"
        '''

        ''',

        # f"{project_name}/templates/.gitkeep"
        '''

        ''',

        # f"{project_name}/media/.gitkeep"
        '''

        '''
    ]
    
    for i in range(0,len(init_files)):
        try:
            with open(init_files[i], 'w') as f:
                f.write(file_contents[i].strip())
        except:
            continue

    print(f"Project '{project_name}' created successfully!")

def main():
    parser = argparse.ArgumentParser(description="Archus CLI")
    parser.add_argument('command', choices=['createproject'], help="Command to run")
    parser.add_argument('project_name', help="Name of the project to create")

    args = parser.parse_args()

    if args.command == 'createproject':
        create_project_structure(args.project_name)

if __name__ == '__main__':
    main()
