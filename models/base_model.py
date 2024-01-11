from datetime import datetime
from models import storage

import uuid

class BaseModel:
    def __init__(self, *args, **kwargs):
        if kwargs:
            
            for key, value in kwargs.items():
                
                if key == '__class__':
                    continue

                elif key in ['created_at', 'updated_at']:
                    setattr(self, key, datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f'))
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            storage.new(self)
            storage.save()

    def __str__(self):
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()



    def to_dict(self):
        my_dict = self.__dict__.copy()

        my_dict['__class__'] = self.__class__.__name__

        my_dict['created_at'] = self.created_at.isoformat()
        my_dict['updated_at'] = self.updated_at.isoformat()

        return my_dict
