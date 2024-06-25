from archus.middleware.main import Middleware
import os,sys,json
from datetime import datetime

def write(message:str,status:str,path:str,client:str,error=False):
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        sys.path.append(root_dir)

        try:
            import config
        except Exception as e:
            print(e)

        LOG_DIR=config.LOG_DIR or "log"
        
        if not os.path.exists(LOG_DIR):
            os.mkdir(LOG_DIR)

        _now = datetime.now()
        _sub_dir = LOG_DIR+"/"+_now.strftime("%Y-%m-%d")

        if not os.path.exists(_sub_dir):
            os.mkdir(_sub_dir)

        _file_name=_sub_dir+"/"+_now.strftime("%H:%M")+'.log'
        
        level='ERROR' if error else 'INFO'

        log=f'{_now.strftime("%Y-%m-%d %H:%M:%S")} - {level} - {path} - {client} - {status} - {message}'
        print(log)

class LoggingMiddleware(Middleware):
    def __init__(self, app):
        super().__init__(app)

    def __call__(self, environ, start_response):

        # print(f"Request: {environ['REQUEST_METHOD']} {environ['PATH_INFO']}")

        def custom_start_response(status, headers, exc_info=None):
            return start_response(status, headers, exc_info)

        response=super().__call__(environ, custom_start_response)
        
        try:
            if isinstance(response, list) and len(response) > 0:
                tepm_res=json.loads(response[0].decode())
                status=tepm_res.get('status')
                write(
                    message=tepm_res.get('message',""),
                    status=status,
                    path=f"{environ['REQUEST_METHOD']} {environ['PATH_INFO']}",
                    client=environ.get('REMOTE_ADDR', '') ,
                    error=True if int(status.split(" ")[0])>=400 else False
                )
                pass
            
        except Exception as e:
            print(e)
        
        finally:
            return response