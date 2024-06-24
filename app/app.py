from archus import Archus
from archus.middleware import LoggingMiddleware, SecurityHeadersMiddleware,CORSMiddleware,ThrottleMiddleWare

from app.api.v1.routes import v1_urls
from app.api.v2.routes import v2_urls
from app.templating.routes import urls

application = Archus()

application.add_middleware(SecurityHeadersMiddleware)
application.add_middleware(ThrottleMiddleWare)
application.add_middleware(CORSMiddleware)
application.add_middleware(LoggingMiddleware)



application.register_blueprint("/api/v1",v1_urls)
application.register_blueprint("/api/v2",v2_urls)
application.register_blueprint("/",urls)