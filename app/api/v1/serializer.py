from archus.serializer import ArchusSerializer,ValidationError,Field

"""
{
    "name":"Utsav",
    "pics":[
        {"name":"a.jpg"},
        {"name":"b.jpg"}
    ]
}
"""

class PicsSerializer(ArchusSerializer):

    def __init__(self, **fields):
        super().__init__(
            name=Field(required=True,data_type=str,validator=self.verify_picname)
        )
    
    @staticmethod
    def verify_picname(value,field):
        if value.split(".")[1] != 'jpg':
            raise ValidationError("only jpg pics are allowed!",field)
        return value

class UserSerializer(ArchusSerializer):

    def __init__(self, **fields):
        super().__init__(
            name=Field(required=True,data_type=str),
            pics=Field(required=True,data_type=list,validator=self.create_pics)
        )
    
    @staticmethod
    def create_pics(value,field):
        for v in value:
            PicsSerializer().validated_data(v)
        return value

