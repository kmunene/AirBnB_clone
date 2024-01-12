#!/usr/bin/python3
import json
from os.path import exists
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """
    A simple file-based storage system for serializing
    and deserializing objects.

    Attributes:
        __file_path (str): Path to the JSON file used for storage.
        __objects (dict): Dictionary to store serialized objects.

    Methods:
        all(self): Returns a dictionary containing all
        stored objects.
        new(self, obj): Adds a new object to the storage
        dictionary.
        save(self): Serializes and saves the stored objects
        to the JSON file.
        reload(self): Deserializes and reloads objects from
        the JSON file.

    Usage:
        This class is intended to be used as a singleton
        for storing and retrieving
        instances of classes derived from BaseModel. It
        provides methods to save
        objects to a JSON file and reload them as needed.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        Retrieve all stored objects.

        Returns:
            dict: A dictionary containing all stored objects.
        """
        return FileStorage.__objects

    def new(self, obj):
        """
        Add a new object to the storage dictionary.

        Parameters:
            obj: An instance of a class derived from BaseModel.
        """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """
        Serialize and save the stored objects to the JSON file.
        """
        serialized_objects = {key: obj.to_dict() for key,
                              obj in FileStorage.__objects.items()}
        with open(FileStorage.__file_path, 'w') as file:
            json.dump(serialized_objects, file)

    def reload(self):
        """
        Deserialize and reload objects from the JSON file.
        """
        try:
            with open(FileStorage.__file_path, 'r') as file:
                loaded_objects = json.load(file)
                for key, obj_dict in loaded_objects.items():
                    class_name, obj_id = key.split('.')
                    obj_dict['__class__'] = class_name
                    class_obj = globals()[class_name]
                    instance = class_obj(**obj_dict)
                    FileStorage.__objects[key] = instance
        except FileNotFoundError:
            pass
