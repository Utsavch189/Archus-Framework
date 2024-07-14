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
        f"{project_name}/gunicorn_config.py",
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
        f"{project_name}/templates/index.html",
        f"{project_name}/.gitignore",
        f"{project_name}/static/.gitkeep",
        f"{project_name}/media/.gitkeep",
    ]

    file_contents=[
# f"{project_name}/app/__init__.py"
'''from app.app import application''',

# f"{project_name}/app/app.py"
'''
from app.api.v1.routes import v1_urls
from app.templating.routes import urls
\nfrom archus import Archus
from archus.middleware import CORSMiddleware, LoggingMiddleware, SecurityHeadersMiddleware, GlobalExceptionHandlerMiddleware
\nfrom config import BASE_DIR
\n\napplication = Archus(BASE_DIR=BASE_DIR)
\napplication.add_middleware(CORSMiddleware)
application.add_middleware(LoggingMiddleware)
application.add_middleware(SecurityHeadersMiddleware)
application.add_middleware(GlobalExceptionHandlerMiddleware)
\napplication.register_blueprint("/", urls)
application.register_blueprint("/api/v1", v1_urls)
''',

# f"{project_name}/gunicorn_config.py"
'''
workers = 4  # Number of worker processes
timeout = 30  # Timeout for handling requests
bind = '0.0.0.0:8000'  # Bind to localhost on port 8000
worker_connections = 1000  # Number of connections per worker
''',

# f"{project_name}/app/api/__init__.py"
'''\n''',

# f"{project_name}/app/api/v1/__init__.py"
'''\n''',

# f"{project_name}/app/api/v1/routes.py"
'''
from .service import index
\n\nv1_urls = [
\t{'path': '/', 'method': ['GET'], 'handler': index},
]
''',

# f"{project_name}/app/api/v1/serializer.py"
'''\n''',

# f"{project_name}/app/api/v1/service.py"
'''
from archus.status import HTTPStatus
from archus.response import Response
\n\ndef index(request):
\treturn Response(HTTPStatus.OK, { "message": "Archus is up & running" })
''',

# f"{project_name}/app/templating/__init__.py"
'''\n''',

# f"{project_name}/app/templating/routes.py"
'''
from .service import index
\n\nurls = [
\t{'path': '/', 'method': ['GET'], 'handler': index}
]
''',

# f"{project_name}/app/templating/service.py"
'''
def index(request):
\treturn {'template': 'index.html'}
''',

# f"{project_name}/config.py"
'''
from pathlib import Path
\n\nBASE_DIR = Path(__file__).resolve().parent
\n# Server Key\n# Secret key (use your random key for security)"
KEY = "928635e70a014b41bfd38a66cf6a1939"
\n# SMTP
# SMTP_USE_TLS = True  # will automatically detect port 587
# SMTP_USE_TLS = True  # will automatically detect port 465
SMTP_SERVER = ''
SMTP_USERNAME = ''
SMTP_PASSWORD = ''
SMTP_USE_TLS = True
SMTP_USE_SSL = False
\n# CORS
ALLOWED_ORIGINS = ['*']
ALLOWED_HEADERS = ['Content-Type']
ALLOWED_METHODS = ['OPTIONS', 'POST', 'PUT', 'PATCH', 'DELETE']
\n# Throttling
MAX_REQUESTS = 10
PERIOD = 60  # Seconds
\n# Dirs
LOG_DIR = "log"
MEDIA_DIR = "media"
STATIC_DIR = "static"
TEMPLATE_DIR = "templates"
''',

# f"{project_name}/run.py"
'''
from app import application
\n\nif __name__ == "__main__":
\tapplication.run()
''',

# f"{project_name}/templates/index.html"
'''
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
</head>

<body>
  <h1>Hello World</h1>
</body>

</html>
''',

# f"{project_name}/.gitignore"
'''
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class
# C extensions
*.so
# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST
# PyInstaller
# Usually these files are written by a python script from a template
# before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec
# Installer logs
pip-log.txt
pip-delete-this-directory.txt
# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/
# Translations
*.mo
*.pot
# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
# Flask stuff:
instance/
.webassets-cache
# Scrapy stuff:
.scrapy
# Sphinx documentation
docs/_build/
# PyBuilder
.pybuilder/
target/
# Jupyter Notebook
.ipynb_checkpoints
# IPython
profile_default/
ipython_config.py
# pyenv
# For a library or package, you might want to ignore these files since the code is
# intended to run in multiple environments; otherwise, check them in:
#.python-version
# pipenv
# According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
# However, in case of collaboration, if having platform-specific dependencies or dependencies
# having no cross-platform support, pipenv may install dependencies that don't work, or not
# install all needed dependencies.
# Pipfile.lock
# poetry
# Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
# This is especially recommended for binary packages to ensure reproducibility, and is more
# commonly ignored for libraries.
# https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
# poetry.lock
# pdm
# Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
# pdm.lock
# pdm stores project-wide configurations in .pdm.toml, but it is recommended to not include it
# in version control.
# https://pdm.fming.dev/latest/usage/project/#working-with-version-control
.pdm.toml
.pdm-python
.pdm-build/
# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/
# Celery stuff
celerybeat-schedule
celerybeat.pid
# SageMath parsed files
*.sage.py
# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
# Spyder project settings
.spyderproject
.spyproject
# Rope project settings
.ropeproject
# mkdocs documentation
/site
# mypy
.mypy_cache/
.dmypy.json
dmypy.json
# Pyre type checker
.pyre/
# pytype static type analyzer
.pytype/
# Cython debug symbols
cython_debug/
# PyCharm
# JetBrains specific template is maintained in a separate JetBrains.gitignore that can
# be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
# and can be added to the global gitignore or merged into this file.  For a more nuclear
# option (not recommended) you can uncomment the following to ignore the entire idea folder.
#.idea/
''',

# f"{project_name}/static/.gitkeep"
'''\n''',

# f"{project_name}/templates/.gitkeep"
'''\n''',

# f"{project_name}/media/.gitkeep"
'''\n'''
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

if __name__=="__main__":
    main()
