# SERVER KEY
"""
SECRET KEY.
USE YOUR RANDOM KEY FOR SECURITY.
"""
KEY="928635e70a014b41bfd38a66cf6a1939"

# SMTP
"""
SMTP_USE_TLS=True WILL AUTOMATICALLY DETECT PORT 587.
SMTP_USE_SSL=TRUE WILL AUTOMATICALLY DETECT PORT 465.
"""

SMTP_SERVER = 'smtp.gmail.com'
SMTP_USE_TLS=True
SMTP_USE_SSL=False
SMTP_USERNAME = 'utsavpokemon9000chatterjee@gmail.com'
SMTP_PASSWORD = 'nzlettvkyviafplp'

# CORS
ALLOWED_ORIGINS=['*']
ALLOWED_METHODS=[ 'POST', 'OPTIONS','PUT','DELETE','PATCH']
ALLOWED_HEADERS=['Content-Type']

# Throttling
MAX_REQUESTS=10
PERIOD=60 # Seconds

# Dirs
TEMPLATE_DIR="templates"
STATIC_DIR="static"
MEDIA_DIR="media"
LOG_DIR="log"