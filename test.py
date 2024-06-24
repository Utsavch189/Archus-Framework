from marshmallow import Schema, fields, ValidationError, validates, validates_schema,pre_load,post_load
from marshmallow.validate import Length, Range, Email

class Serializer(Schema):

    def serialize(self,data):
        print("data",super().load(data))
        data=super().load(data)
        classname=self.__class__.__name__

        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
        
        def __repr__(self):
            field_strings = [f"{key}={getattr(self, key)!r}" for key in fields]
            return f"{classname}({', '.join(field_strings)})"
        
        
        attrs = {'__init__': __init__,'__repr__': __repr__}

        for key,values in data.items():
            attrs[key] = values
        
        
        
        dynamic_class = type(classname, (object,), attrs)
        return dynamic_class

    def get_data(self,data):
        try:
            data=super().load(data)
            return data
        except ValidationError as e:
            raise Exception(str(e))


class RequestSchema(Serializer):
    name = fields.String(required=True, validate=Length(min=2, max=50))
    age = fields.Integer(required=True, validate=Range(min=0, max=120))

    @pre_load
    def preprocess_name(self, data, **kwargs):
        if 'name' in data:
            data['name'] = data['name'].upper()
        return data

    @validates('name')
    def validate_name(self, value):
        if not value.isalpha():
            raise ValidationError("Name must contain only alphabetic characters.")
    
    @validates('age')
    def validate_age(self, value):
        if value<18:
            raise ValidationError("Age must have at least 18")

data={
    "name":"utsav",
    "age":22
}
try:
    s=RequestSchema()
    data=s.get_data(data)
    print(data)
except ValidationError as e:
    print(e)