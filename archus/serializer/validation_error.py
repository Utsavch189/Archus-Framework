class ValidationError(Exception):
    def __init__(self, message, field_name=None):
        super().__init__(message)
        self.field_name = field_name