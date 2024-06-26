from .status import HTTPStatus
import json
from datetime import datetime


class Response:
    def __init__(self, status:HTTPStatus, body, content_type='text/plain',headers:list=None):
        self.status = self.get_status_message(status)
        if content_type=="application/json" or type(body)==dict:
            self.body=self.toJson(body)
            self.headers = [('Content-Type', "application/json"),('Content-Length', str(len(self.body.encode('utf-8'))))]
            if headers:
                for h in headers:
                    self.headers.append(h)
        else:
            self.body = body
            self.headers = [('Content-Type', content_type),('Content-Length', str(len(self.body)))]
            if headers:
                for h in headers:
                    self.headers.append(h)

    def __iter__(self):
        yield self.body

    @staticmethod
    def get_status_message(status:HTTPStatus):
        status = f"{status.value[0]} {status.value[1]}"
        return status
    
    def toJson(self,body):
        return json.dumps({**body , **{"timestamp":str(int(datetime.timestamp(datetime.now()))),"status":self.status}})