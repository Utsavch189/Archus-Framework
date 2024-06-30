import json
from urllib.parse import parse_qs
from cgi import FieldStorage
from io import BytesIO


class Request:
    def __init__(self, environ):
        self.method = environ['REQUEST_METHOD']
        self.path = environ['PATH_INFO']
        self.query_params = parse_qs(environ['QUERY_STRING'])
        self.headers = self._parse_all_headers(environ)
        self.http_headers = self._parse_http_headers(environ)
        self.cookies = self._parse_cookies(environ)
        self.body = self._read_body(environ)
        self.form = self._parse_form(environ)
        self.files = self._parse_files(environ)
        self.json = self._parse_json(environ)
        self.data = self._parse_data(environ)

    def _parse_all_headers(self, environ):
        headers = {}
        for key, value in environ.items():
            headers[key.lower()] = value
        return headers
    
    def _parse_http_headers(self, environ):
        headers = {}
        for key, value in environ.items():
            if key.startswith('HTTP_'):
                headers[key[5:].replace('_', '-').lower()] = value
        return headers

    def _parse_cookies(self, environ):
        cookies = {}
        cookie_string = environ.get('HTTP_COOKIE', '')
        for cookie in cookie_string.split(';'):
            cookie = cookie.strip()
            if '=' in cookie:
                key, value = cookie.split('=', 1)
                cookies[key.strip()] = value.strip()
        return cookies


    def _read_body(self, environ):
        try:
            content_length = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError, TypeError):
            content_length = 0
        return environ['wsgi.input'].read(content_length)

    def _parse_form(self, environ):
        form = {}
        if self.method != 'GET' and environ.get('CONTENT_TYPE', '').startswith('application/x-www-form-urlencoded'):
            form_data = parse_qs(self.body.decode())
            for key, value in form_data.items():
                form[key] = value[0]
        return form

    def _parse_files(self, environ):
        files = {}
        if self.method != 'GET' and 'multipart/form-data' in environ.get('CONTENT_TYPE', ''):
            fs = FieldStorage(fp=BytesIO(self.body), environ=environ, keep_blank_values=True)
            for key in fs.keys():
                file_item = fs[key]
                if isinstance(file_item, FieldStorage) and file_item.filename:
                    files[key] = {
                        'filename': file_item.filename,
                        'file':file_item.file.read(),
                        'type': file_item.type,
                        'size': file_item.length
                    }
        return files


    def _parse_json(self,environ):
        if environ.get('CONTENT_TYPE', '').startswith('application/json'):
            try:
                return self.body.decode()
            except ValueError:
                return None
        return None
    
    def _parse_data(self,environ):
        if environ.get('CONTENT_TYPE', '').startswith('application/json'):
            try:
                return json.loads(self.body.decode())
            except ValueError:
                return None
        return None

    def get_header(self, header_name, default=None):
        return self.headers.get(header_name.lower(), default)

    def get_cookie(self, cookie_name, default=None):
        return self.cookies.get(cookie_name, default)

    def get_form_param(self, param_name, default=None):
        return self.form.get(param_name, default)

    def get_file(self, file_name):
        return self.files.get(file_name, None)
