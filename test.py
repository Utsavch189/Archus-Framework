# from marshmallow import Schema, fields, ValidationError, validates, validates_schema,pre_load,post_load
# from marshmallow.validate import Length, Range, Email

# class Serializer(Schema):

#     def serialize(self,data):
#         print("data",super().load(data))
#         data=super().load(data)
#         classname=self.__class__.__name__

#         def __init__(self, **kwargs):
#             for key, value in kwargs.items():
#                 setattr(self, key, value)
        
#         def __repr__(self):
#             field_strings = [f"{key}={getattr(self, key)!r}" for key in fields]
#             return f"{classname}({', '.join(field_strings)})"
        
        
#         attrs = {'__init__': __init__,'__repr__': __repr__}

#         for key,values in data.items():
#             attrs[key] = values
        
        
        
#         dynamic_class = type(classname, (object,), attrs)
#         return dynamic_class

#     def get_data(self,data):
#         try:
#             data=super().load(data)
#             return data
#         except ValidationError as e:
#             raise Exception(str(e))


# class RequestSchema(Serializer):
#     name = fields.String(required=True, validate=Length(min=2, max=50))
#     age = fields.Integer(required=True, validate=Range(min=0, max=120))

#     @pre_load
#     def preprocess_name(self, data, **kwargs):
#         if 'name' in data:
#             data['name'] = data['name'].upper()
#         return data

#     @validates('name')
#     def validate_name(self, value):
#         if not value.isalpha():
#             raise ValidationError("Name must contain only alphabetic characters.")
    
#     @validates('age')
#     def validate_age(self, value):
#         if value<18:
#             raise ValidationError("Age must have at least 18")

# data={
#     "name":"utsav",
#     "age":22
# }
# try:
#     s=RequestSchema()
#     data=s.get_data(data)
#     print(data)
# except ValidationError as e:
#     print(e)


import json
from datetime import datetime

class ValidationError(Exception):
    def __init__(self, message, field_name=None):
        super().__init__(message)
        self.field_name = field_name

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

class Serializer:
    def __init__(self, **fields):
        self._fields = fields
        self._error={}
        self._has_error=False


    def is_valid(self, data):

        for _field_name, _field in self._fields.items():
            _value = data.get(_field_name, _field.default)
            try:
                _field.validate(_value, _field_name)
            except ValidationError as e:
                if self.errors.get(e.field_name):
                    self._error[e.field_name].append(str(e))
                else:
                    self._error[e.field_name]=[str(e)]
                self._has_error=True

        if self._has_error:
            return False
        else:
            return True
    
    @property
    def errors(self):
        return self._error

    def validated_data(self,data):
        if self.is_valid(data):
            validated_data = {}
            for field_name, field in self._fields.items():
                value = data.get(field_name, field.default)
                validated_value = field.validate(value, field_name)
                validated_data[field_name] = validated_value
            return validated_data
        else:
            return self.errors

    def serialize(self, data):
        validated_data = self.validated_data(data)
        return json.dumps(validated_data)

    def deserialize(self, data):
        parsed_data = json.loads(data)
        return self.validate(parsed_data)

class AddressSerializer(Serializer):
    def __init__(self):
        super().__init__(
            city=Field(required=True, data_type=str)
        )


# Define a custom serializer
class UserSerializer(Serializer):

    @staticmethod
    def verify_age(value,field):
        if value<18:
            raise ValidationError("age must be over 18",field)
        return value

    @staticmethod
    def verify_name(value,field):
        if len(value)>5:
            raise ValidationError("long names are not allowed",field)
        if value[0]=="J":
            raise ValidationError("first letter must not J",field)
        return value.lower()
    
    @staticmethod
    def validate_address_list(value, field_name):
        for address in value:
            AddressSerializer().validated_data(address)
        return value

    def __init__(self):
        super().__init__(
            name=Field(required=True, data_type=str,validator=self.verify_name),
            age=Field(required=True, data_type=int,validator=self.verify_age),
            email=Field(required=True, data_type=str),
            address=Field(required=True, data_type=list, validator=self.validate_address_list),
            created_at=Field(required=False, data_type=str, default=datetime.now().isoformat())
        )

# Example usage
serializer = UserSerializer()

data = {
    "name": "Aohn",
    "age": 20,
    "email": "john@example.com" ,
    "address":[
        {
            "city1":"a"
        },
        {
            "city2":"b"
        }
    ]
}

# Serialize the data

    
if serializer.is_valid(data):
    serialized_data = serializer.serialize(data)
    print("Serialized data:", serialized_data)
else:
    print("errors : ",serializer.errors)

# Deserialize the data
# try:
#     deserialized_data = serializer.deserialize(serialized_data)
#     print("Deserialized data:", deserialized_data)
# except ValidationError as e:
#     print(f"Validation error for field '{e.field_name}': {e}")

