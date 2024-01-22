#!/usr/bin/python3

import unittest
from models import FileStorage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import os


class TestFileStorage(unittest.TestCase):
    def setUp(self):
        self.file_storage = FileStorage()

    def tearDown(self):
        del self.file_storage
        self.remove_file_if_exists("file.json")

    def test_all_method(self):
        objects_dict = self.file_storage.all()
        self.assertIsInstance(objects_dict, dict)
        self.assertEqual(objects_dict, self.file_storage._FileStorage__objects)

    def test_new_method(self):
        new_object = BaseModel()
        self.file_storage.new(new_object)
        key = self.get_object_key(new_object)
        self.assertIn(key, self.file_storage._FileStorage__objects)
        self.assertEqual(self.file_storage._FileStorage__objects[key], new_object)

    def test_save_and_reload_methods(self):
        # Create and save objects
        obj1 = BaseModel()
        obj2 = User()
        obj3 = State()
        self.file_storage.new(obj1)
        self.file_storage.new(obj2)
        self.file_storage.new(obj3)
        self.file_storage.save()

        # Check if the file is created
        self.assertTrue(os.path.exists("file.json"))

    def remove_file_if_exists(self, filename):
        try:
            os.remove(filename)
        except FileNotFoundError:
            pass

    def get_object_key(self, obj):
        return "{}.{}".format(obj.__class__.__name__, obj.id)


if __name__ == '__main__':
    unittest.main()

