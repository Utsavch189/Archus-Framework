from ..status import HTTPStatus

class ArchusException(Exception):

    def __init__(self, *args: object,status:HTTPStatus,message=None) -> None:
        self.status = status
        if message:
            self.message=message
        else:
            self.message=status.value[1]
        super().__init__(self.message)
    
    def to_dict(self):
        return {"message": self.message}