#!/usr/bin/python3
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
from models import storage

class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand class implements a command-line interpreter for managing AirBnB objects.

    The commands include creating, displaying, updating, and deleting instances of various classes.
    Custom commands like <class name>.count(), <class name>.all(), and <class name>.show(<id>) are also supported.
    """
    prompt = "(hbnb) "

    def default(self, line):
        """
        Handle unknown commands, allowing for custom commands like <class name>.count(),
        <class name>.all(), and <class name>.show(<id>)
        """
        tokens = line.split('.')
        if len(tokens) == 2:
            class_name, method = tokens
            classes = [BaseModel, User, State, City, Amenity, Place, Review]
            try:
                class_type = next(cls for cls in classes if cls.__name__ == class_name)
                if method == 'count()':
                    count = sum(1 for obj in storage.all().values()
                                if isinstance(obj, class_type))
                    print(count)

                elif method == 'all()':
                    all_objs = storage.all()
                    if class_name not in (cls.__name__ for cls in classes):
                        print("** class doesn't exist **")
                    else:
                        print('[', end="")
                        obj_list = [f'"{all_objs[obj]}"' for obj in all_objs if obj.startswith(f"{class_name}.")]
                        for index, obj_str in enumerate(obj_list):
                            print(obj_str, end="")
                            if index < len(obj_list) - 1:
                                print(', ', end="")
                        print(']')
                elif method.startswith('show("') and method.endswith('")'):
                    obj_id = method[len('show("'):-2]
                    key = f"{class_name}.{obj_id}"

                    if key in models.storage.all():
                        print(models.storage.all()[key])
                    else:
                        print("** no instance found **")
                elif method.startswith('destroy("') and method.endswith('")'):
                    obj_id = method[len('destroy("'):-2]
                    key = f"{class_name}.{obj_id}"
                    
                    if key in models.storage.all():
                        del(models.storage.all()[key])
                    else:
                        print("** no instance found **")
                elif method.startswith('update("') and method.endswith('")') or method.endswith(')'):
                    if method.endswith('")'):
                        match_attr = re.match(r'update\("(.+)", "(.+)", "(.+)"\)', method)
                        match_dict = re.match(r'update\("(.+)", (\{.*\})', method)
                    elif method.endswith(')'):
                        match_attr = re.match(r'update\("(.+)", "(.+)", (.+)\)', method)
                        match_dict = re.match(r'update\("(.+)", (\{.*\})', method)
                    if match_attr:
                        obj_id, atrr_name, atrr_value = match_attr.groups()
                        key = f"{class_name}.{obj_id}"

                        if key not in storage.all():
                            print("** no instance found **")
                            return

                        obj = storage.all()[key]
                        if hasattr(obj, atrr_name):
                            setattr(obj, atrr_name, type(getattr(obj, atrr_name))(atrr_value))
                            storage.save()
                        else:
                            setattr(obj, atrr_name, atrr_value)
                            storage.save()
                    elif match_dict:
                        obj_id, attr_dict_str = match_dict.groups()
                        obj_id = obj_id.replace('"', '')
                        key = f"{class_name}.{obj_id}"

                        if key not in storage.all():
                            print("** no instance found **")
                            return
                        
                        obj = storage.all()[key]
                        attr_dict = eval(attr_dict_str)
                        for attr_name, attr_value in attr_dict.items():
                            if hasattr(obj, attr_name):
                                setattr(obj, attr_name, type(getattr(obj, attr_name))(attr_value))
                            else:
                                setattr(obj, attr_name, attr_value)
                        storage.save()
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
                class_type = next(cls for cls in classes if cls.__name__ == arg)
                new_instance = class_type()
                storage.save()
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

        all_objs = storage.all()
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
                obj_list = [f'"{all_objs[obj]}"' for obj in all_objs if obj.startswith(f"{arg}.")]
                for index, obj_str in enumerate(obj_list):
                    print(obj_str, end="")
                    if index < len(obj_list) - 1:
                        print(', ', end="")
                print(']')


    def do_update(self, arg):
        """
        Update an instance based on its ID with either attribute name and value
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

            if key not in storage.all():
                print("** no instance found **")
                return

            if length <= 1:
                print("** attribute name missing **")
                return
            
            attr_name = rest[1]

            if length <= 2:
                print("** value missing **")
                return
            
            attr_value = rest[2]

            obj = storage.all()[key]

            if hasattr(obj, attr_name):
                setattr(obj, attr_name, type(getattr(obj, attr_name))(attr_value))
                storage.save()
            else:
                setattr(obj, attr_name, attr_value)
                storage.save()

        
if __name__ == "__main__":
    HBNBCommand().cmdloop()