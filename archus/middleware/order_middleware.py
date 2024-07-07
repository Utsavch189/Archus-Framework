from .CorsMiddleware import CORSMiddleware
from .GlobalExceptionMiddleware import GlobalExceptionHandlerMiddleware
from .LoggingMiddleware import LoggingMiddleware
from .SecurityMiddleware import SecurityHeadersMiddleware
from .ThrottleMiddleware import ThrottleMiddleWare
from .main import Middleware
from typing import List,Dict

def middleware_stack_order()->Dict[Middleware,int]:
    return {
        SecurityHeadersMiddleware:1,
        CORSMiddleware:2,
        LoggingMiddleware:3,
        GlobalExceptionHandlerMiddleware:4
    }


def check_middleware_stack(middleware_stack:List[Middleware]):
    req_order=middleware_stack_order()
    max_order=max([values for key,values in req_order.items()])
    prev_seq=0

    for middleware in middleware_stack:
        seq_no=req_order.get(middleware)
        if seq_no==None:
            if prev_seq<max_order:
                raise Exception(f"{middleware} is missplaced. Place it at very bottom.")
        else:
            if seq_no<prev_seq:
                raise Exception(f"{middleware} is missplaced. Stack should be [SecurityHeadersMiddleware,CORSMiddleware,LoggingMiddleware,GlobalExceptionHandlerMiddleware,ThrottleMiddleWare,CustomMiddlewares]")

            prev_seq=seq_no