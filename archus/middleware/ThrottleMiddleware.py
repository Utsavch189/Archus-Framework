from collections import defaultdict, deque
import time
from archus.status import HTTPStatus
from archus.response import Response
from archus.middleware.main import Middleware

class ThrottleMiddleWare(Middleware):
    def __init__(self,app, max_requests:int=2, period:int=60, cleanup_interval:int=3600):
        super().__init__(app)
        self.max_requests = max_requests
        self.period = period
        self.cleanup_interval = cleanup_interval
        self.client_requests = defaultdict(lambda: deque(maxlen=max_requests))
        self.last_cleanup_time = time.time()

    def __call__(self, environ, start_response):
        self.cleanup_expired_requests()
        
        client_ip = environ.get('REMOTE_ADDR', '')  # Get client IP
        print(self.client_requests)
        current_time = time.time()

        if len(self.client_requests[client_ip]) >= self.max_requests:
            return Response(HTTPStatus.TOO_MANY_REQUESTS, 'Rate limit exceeded')

        self.client_requests[client_ip].append(current_time)

        def custom_start_response(status, headers, exc_info=None):
            return start_response(status, headers, exc_info)

        response=super().__call__(environ, custom_start_response)
        return response


    def cleanup_expired_requests(self):
        current_time = time.time()
        if current_time - self.last_cleanup_time >= self.cleanup_interval:
            for client_ip in list(self.client_requests.keys()):
                self.client_requests[client_ip] = deque(filter(lambda ts: ts >= current_time - self.period, self.client_requests[client_ip]), maxlen=self.max_requests)
            self.last_cleanup_time = current_time
