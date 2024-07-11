from .main import Middleware

class CSPMiddleware(Middleware):
    def __init__(self, app,BASE_DIR=None):
        super().__init__(app,BASE_DIR=BASE_DIR)
        self.default_policies = {
            "default-src": ["'self'"],
            "script-src": ["'self'", "'unsafe-eval'", "'unsafe-inline'"],
            "style-src": ["'self'", "'unsafe-inline'", "cdn.jsdelivr.net"],
            "img-src": ["'self'", "blob:", "data:"],
            "font-src": ["'self'"],
            "object-src": ["'none'"],
            "base-uri": ["'self'"],
            "form-action": ["'self'"],
            "frame-ancestors": ["'none'"],
            "upgrade-insecure-requests": []
        }

    def __call__(self, environ, start_response):
        def custom_start_response(status, headers, exc_info=None):
            if not any(header[0].lower() == 'content-security-policy' for header in headers):
                headers.append(('Content-Security-Policy', self._build_policy()))
            return start_response(status, headers, exc_info)
        
        return super().__call__(environ, custom_start_response)

    def _build_policy(self):
        policy_parts = []
        for key, values in self.default_policies.items():
            policy_parts.append(f"{key} " + " ".join(values))
        return "; ".join(policy_parts)