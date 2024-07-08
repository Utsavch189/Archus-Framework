from .validation_error import ValidationError

class Field:
    def __init__(self, required=False, data_type=None, default=None,validator=None,external_serializer=None):
        self.required = required
        self.data_type = data_type
        self.default = default
        self.validator=validator
        self.external_serializer=external_serializer

    def validate(self, value, field_name,partial=False):
        if not partial:
            if self.required and value is None:
                raise ValidationError(f"The field '{field_name}' is required.",field_name)
        if self.data_type and value is not None and not isinstance(value, self.data_type):
            raise ValidationError(f"Invalid data type for field '{field_name}'. Expected {self.data_type.__name__}.", field_name)

        if self.external_serializer and self.data_type==dict:
            self.external_serializer().validated_data(value)
        
        if self.external_serializer and self.data_type==list:
            for data in value:
                self.external_serializer().validated_data(data)

        if self.validator and value is not None:
            value=self.validator(value, field_name)
        return value