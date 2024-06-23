from .status import HTTPStatus
import json
from datetime import datetime
from typing import Union,Dict


class Response:
    def __init__(self, status:HTTPStatus, body:Union[Dict|str], content_type='text/plain'):
        self.status = self.get_status_message(status)
        if content_type=="application/json" or type(body)==dict:
            self.body=self.toJson(body)
            self.headers = [('Content-Type', "application/json"),('Content-Length', str(len(self.body.encode('utf-8'))))]

        else:
            self.body = body
            self.headers = [('Content-Type', content_type),('Content-Length', str(len(self.body)))]
    
    def __iter__(self):
        yield self.body

    @staticmethod
    def get_status_message(status:HTTPStatus):
        status = f"{status.value[0]} {status.value[1]}"
        return status
    
    def toJson(self,body):
        return json.dumps({**body , **{"timstamp":str(int(datetime.timestamp(datetime.now())))}})