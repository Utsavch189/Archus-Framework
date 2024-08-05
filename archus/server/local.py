from waitress import serve
from datetime import datetime

def run_local(app,host:str,port:int)->None:
    try:
        print(f"Dev Server Running on http://{host}:{port} at {datetime.now()}")
        serve(app,host=host,port=port)
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        exit()