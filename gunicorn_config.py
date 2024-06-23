# gunicorn_config.py

bind = '0.0.0.0:8000'  # Bind to localhost on port 8000
workers = 4  # Number of worker processes
worker_connections = 1000  # Number of connections per worker
timeout = 30  # Timeout for handling requests
