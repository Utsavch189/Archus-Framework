from collections import defaultdict, deque
import time
from ..status import HTTPStatus
from ..response import Response
from .main import Middleware
from datetime import datetime,timedelta
import os,sys

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(root_dir)

try:
    import config
except Exception as e:
    print(e)


CLIENT_REQUESTS=defaultdict(lambda: deque(maxlen=config.MAX_REQUESTS))

class ThrottleMiddleWare(Middleware):
    def __init__(self,app, max_requests:int=2, period:int=60, cleanup_interval:int=65):
        super().__init__(app)
        self.max_requests = config.MAX_REQUESTS or max_requests
        self.period = config.PERIOD or period
        self.cleanup_interval = cleanup_interval
        self.last_cleanup_time = time.time()

    def __call__(self, environ, start_response):
        self.cleanup_expired_requests()
        
        client_ip = environ.get('REMOTE_ADDR', '')  # Get client IP
        # print(CLIENT_REQUESTS)
        current_time = time.time()

        if len(CLIENT_REQUESTS[client_ip]) >= self.max_requests-1:
            response= Response(HTTPStatus.TOO_MANY_REQUESTS, {"message":'Rate limit exceeded'})
            start_response(response.status, response.headers)
            return [response.body.encode()]
            
            
        CLIENT_REQUESTS[client_ip].append(current_time)

        def custom_start_response(status, headers, exc_info=None):
            return start_response(status, headers, exc_info)

        response=super().__call__(environ, custom_start_response)
        return response


    def cleanup_expired_requests(self):
        try:
            current_time = time.time()
            if current_time - self.last_cleanup_time >= self.cleanup_interval:
                for client_ip in list(self.client_requests.keys()):
                    CLIENT_REQUESTS[client_ip] = deque(filter(lambda ts: ts >= current_time - self.period, self.client_requests[client_ip]), maxlen=self.max_requests)
                self.last_cleanup_time = current_time
        except Exception as e:
            print(e)
