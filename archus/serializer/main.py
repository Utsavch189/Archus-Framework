from archus.serializer.field import Field
from archus.serializer.validation_error import ValidationError
import json
from archus.exceptions import ArchusException
from archus.status import HTTPStatus

class ArchusSerializer:
    def __init__(self,partial=False, **fields):
        self._fields = fields
        self._error={}
        self._has_error=False
        self._partial=partial


    def is_valid(self, data):

        for _field_name, _field in self._fields.items():
            _value = data.get(_field_name, _field.default)
            try:
                _field.validate(_value, _field_name,partial=self._partial)
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
                validated_value = field.validate(value, field_name,partial=self._partial)
                validated_data[field_name] = validated_value
            return validated_data
        else:
            raise ArchusException(status=HTTPStatus.UNPROCESSABLE_ENTITY,message=self.errors)

    def serialize(self, data):
        validated_data = self.validated_data(data)
        return json.dumps(validated_data)

    def deserialize(self, data):
        parsed_data = json.loads(data)
        return self.validated_data(parsed_data)