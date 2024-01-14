#!/usr/bin/python3
"""Module for the entry of the console"""

import cmd
import re

import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand class implements a command-line interpreter
    for managing AirBnB objects.

    The commands include creating, displaying, updating,
    and deleting instances of various classes.
    Custom commands like <class name>.count(), <class name>.all(),
    and <class name>.show(<id>) are also supported.
    """
    prompt = "(hbnb) "
    classes = [BaseModel, User, State, City, Amenity, Place, Review]

    def handle_count(self, class_type):
        """
        Handle the <class name>.count() command.

        Parameters:
            class_type (type): The class type to count instances of.

        Prints:
            int: The count of instances of the specified class.
        """
        count = sum(1 for obj in models.storage.all().values()
                    if isinstance(obj, class_type))
        print(count)

    def handle_all(self, class_name):
        """
        Handle the <class name>.all() command.

        Parameters:
            class_name (str): The name of the class to retrieve instances of.

        Prints:
            str: A list of string representations of instances of
            the specified class.
        """
        all_objs = models.storage.all()
        if class_name not in (cls.__name__ for cls in self.classes):
            print("** class doesn't exist **")
        else:
            print('[', end="")
            obj_list = [f'"{all_objs[obj]}"' for obj in all_objs
                        if obj.startswith(f"{class_name}.")]
            for index, obj_str in enumerate(obj_list):
                print(obj_str, end="")
                if index < len(obj_list) - 1:
                    print(', ', end="")
            print(']')

    def handle_show(self, class_name, obj_id):
        """
        Handle the <class name>.show(<id>) command.

        Parameters:
            class_name (str): The name of the class to retrieve an instance of.
            obj_id (str): The ID of the instance to show.

        Prints:
            str: The string representation of the specified instance.
        """
        key = f"{class_name}.{obj_id}"
        if key in models.storage.all():
            print(models.storage.all()[key])
        else:
            print("** no instance found **")

    def handle_destroy(self, class_name, obj_id):
        """
        Handle the <class name>.destroy(<id>) command.

        Parameters:
            class_name (str): The name of the class to destroy an instance of.
            obj_id (str): The ID of the instance to destroy.
        """
        key = f"{class_name}.{obj_id}"
        if key in models.storage.all():
            del models.storage.all()[key]
        else:
            print("** no instance found **")

    def handle_update(self, class_name, obj_id, attr_name, attr_value):
        """
        Handle the <class name>.update(<id>, <attribute name>,
        <attribute value>) command.

        Parameters:
            class_name (str): The name of the class to update an instance of.
            obj_id (str): The ID of the instance to update.
            attr_name (str): The name of the attribute to update.
            attr_value (str): The new value for the attribute.
        """
        key = f"{class_name}.{obj_id}"
        if key in models.storage.all():
            obj = models.storage.all()[key]
            if hasattr(obj, attr_name):
                setattr(obj, attr_name,
                        type(getattr(obj, attr_name))(attr_value))
            else:
                setattr(obj, attr_name, attr_value)
            models.storage.save()
        else:
            print("** no instance found **")

    def handle_update_dict(self, class_name, obj_id, attr_dict_str):
        """
        Handle the <class name>.update(<id>, <dictionary>) command.

        Parameters:
            class_name (str): The name of the class to update an instance of.
            obj_id (str): The ID of the instance to update.
            attr_dict_str (str): The dictionary as a string with
            attribute names and values.
        """
        key = f"{class_name}.{obj_id}"
        if key in models.storage.all():
            obj = models.storage.all()[key]
            attr_dict = eval(attr_dict_str)
            for attr_name, attr_value in attr_dict.items():
                if hasattr(obj, attr_name):
                    setattr(obj, attr_name,
                            type(getattr(obj, attr_name))(attr_value))
                else:
                    setattr(obj, attr_name, attr_value)
            models.storage.save()
        else:
            print("** no instance found **")

    def default(self, line):
        """
        Handle unknown commands, allowing for custom commands
        like <class name>.count(),
        <class name>.all(), and <class name>.show(<id>)
        """
        tokens = line.split('.')
        if len(tokens) == 2:
            class_name, method = tokens
            try:
                class_type = next(cls for cls in
                                  self.classes if cls.__name__ == class_name)
                if method == 'count()':
                    self.handle_count(class_type)
                elif method == 'all()':
                    self.handle_all(class_name)
                elif method.startswith('show("') and method.endswith('")'):
                    obj_id = method[len('show("'):-2]
                    self.handle_show(class_name, obj_id)
                elif method.startswith('destroy("') and method.endswith('")'):
                    obj_id = method[len('destroy("'):-2]
                    self.handle_destroy(class_name, obj_id)
                elif (method.startswith('update("') and
                      method.endswith('")') or method.endswith(')')):
                    if method.endswith('")'):
                        match_attr = re.match(r'update\("(.+)", "(.+)",'
                                              r' "(.+)"\)', method)
                        match_dict = re.match(r'update\("(.+)",'
                                              r' (\{.*\})', method)
                    elif method.endswith(')'):
                        match_attr = re.match(r'update\("(.+)", "(.+)",'
                                              r' (.+)\)', method)
                        match_dict = re.match(r'update\("(.+)",'
                                              r' (\{.*\})', method)
                    if match_attr:
                        obj_id, attr_name, attr_value = match_attr.groups()
                        self.handle_update(class_name,
                                           obj_id, attr_name, attr_value)
                    elif match_dict:
                        obj_id, attr_dict_str = match_dict.groups()
                        obj_id = obj_id.replace('"', '')
                        self.handle_update_dict(class_name,
                                                obj_id, attr_dict_str)
                    else:
                        print("** invalid update format **")
                else:
                    print("*** Unknown method: {}".format(method))
            except StopIteration:
                print("** class doesn't exist **")
        else:
            print("*** Unknown syntax: {}".format(line))

    def do_quit(self, arg):
        """
        Quit command to exit the program
        """
        return True

    def do_EOF(self, arg):
        """
        EOF command to exit the program
        """
        print()
        return True

    def emptyline(self):
        """
        Empty line should not execute anything
        """
        pass

    def do_create(self, arg):
        """
        Create a new instance of a class and print its ID
        """
        classes = [BaseModel, User, State, City, Amenity, Place, Review]

        if not arg:
            print("** class name missing **")
        else:
            try:
                class_type = next(cls for cls in
                                  classes if cls.__name__ == arg)
                new_instance = class_type()
                models.storage.save()
                print(new_instance.id)
            except StopIteration:
                print("** class doesn't exist **")

    def do_show(self, arg):
        """
        Display information about a specific instance
        """
        classes = [BaseModel, User, State, City, Amenity, Place, Review]
        if not arg:
            print("** class name missing **")
        else:
            class_name, *rest = arg.split(" ")

            if not class_name:
                print("** class name missing **")
                return

            if class_name not in (cls.__name__ for cls in classes):
                print("** class doesn't exist **")
                return

            if not rest:
                print("** instance id missing **")
                return

            obj_id = rest[0]
            key = f"{class_name}.{obj_id}"

            if key in models.storage.all():
                print(models.storage.all()[key])
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        """
        Delete a specific instance
        """
        classes = [BaseModel, User, State, City, Amenity, Place, Review]
        if not arg:
            print("** class name missing **")
        else:
            class_name, *rest = arg.split(" ")

            if class_name not in (cls.__name__ for cls in classes):
                print("** class doesn't exist **")
                return

            if not rest:
                print("** instance id missing **")
                return

            obj_id = rest[0]
            key = f"{class_name}.{obj_id}"

            if key in models.storage.all():
                del(models.storage.all()[key])
            else:
                print("** no instance found **")

    def do_all(self, arg):
        """
        Display all instances or instances of a specific class
        """
        classes = [BaseModel, User, State, City, Amenity, Place, Review]

        all_objs = models.storage.all()
        if not arg:
            print('[', end="")
            for index, obj_id in enumerate(all_objs.keys()):
                obj = all_objs[obj_id]
                print(f'"{obj}"', end="")
                if index < len(all_objs) - 1:
                    print(', ', end="")
            print(']')
        else:
            if arg not in (cls.__name__ for cls in classes):
                print("** class doesn't exist **")
                return
            else:
                print('[', end="")
                obj_list = [f'"{all_objs[obj]}"' for obj in all_objs
                            if obj.startswith(f"{arg}.")]
                for index, obj_str in enumerate(obj_list):
                    print(obj_str, end="")
                    if index < len(obj_list) - 1:
                        print(', ', end="")
                print(']')

    def do_update(self, arg):
        """
        Update an instance based on its ID
        """
        classes = [BaseModel, User, State, City, Amenity, Place, Review]

        if not arg:
            print("** class name missing **")
        else:
            class_name, *rest = arg.split(" ")

            if class_name not in (cls.__name__ for cls in classes):
                print("** class doesn't exist **")
                return

            length = len(rest)

            if length == 0:
                print("** instance id missing **")
                return

            obj_id = rest[0]

            key = f"{class_name}.{obj_id}"

            if key not in models.storage.all():
                print("** no instance found **")
                return

            if length <= 1:
                print("** attribute name missing **")
                return

            attr_name = rest[1]

            if length <= 2:
                print("** value missing **")
                return

            attr_value = rest[2].strip('"')

            obj = models.storage.all()[key]

            if hasattr(obj, attr_name):
                setattr(obj, attr_name, type(getattr(obj, attr_name))
                        (attr_value))
                models.storage.save()
            else:
                setattr(obj, attr_name, attr_value)
                models.storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
