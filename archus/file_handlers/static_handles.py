import os

class StaticFileHandler:
    def __init__(self, static_dir='static'):
        self.static_dir = static_dir

    def serve_file(self, filename):
        file_path = os.path.join(self.static_dir, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                return file.read()
        return None