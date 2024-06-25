from archus.serializer.validation_error import ValidationError

class Field:
    def __init__(self, required=False, data_type=None, default=None,validator=None):
        self.required = required
        self.data_type = data_type
        self.default = default
        self.validator=validator

    def validate(self, value, field_name):
        if self.required and value is None:
            raise ValidationError(f"The field '{field_name}' is required.",field_name)
        if self.data_type and value is not None and not isinstance(value, self.data_type):
            raise ValidationError(f"Invalid data type for field '{field_name}'. Expected {self.data_type.__name__}.", field_name)

        if self.validator and value is not None:
            value=self.validator(value, field_name)
        return value