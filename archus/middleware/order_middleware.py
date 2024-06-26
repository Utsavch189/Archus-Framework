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
        ThrottleMiddleWare:4,
        GlobalExceptionHandlerMiddleware:5
    }

def check_middleware_stack(middleware_stack:List[Middleware]):
    prev_seq=0
    req_order=middleware_stack_order()

    for middleware in middleware_stack:
        seq_no=req_order[middleware]
        if seq_no<prev_seq:
            raise Exception(f"{middleware} is missplaced. Stack should be [SecurityHeadersMiddleware,CORSMiddleware,LoggingMiddleware,ThrottleMiddleWare,GlobalExceptionHandlerMiddleware]")
        prev_seq=seq_no