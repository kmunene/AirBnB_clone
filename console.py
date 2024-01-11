#!/usr/bin/python3
import cmd
import models
from models.base_model import BaseModel
from models import storage

class HBNBCommand(cmd.Cmd):
    """
    Command-line interpreter for the HBNB project.

    Attributes:
        prompt (str): The command prompt string.

    Methods:
        do_quit(self, arg): Quit command to exit the program.
        do_EOF(self, arg): EOF command to exit the program.
        emptyline(self): Empty line should not execute anything.
        do_create(self, arg): Create command to instantiate and save a new object.
        do_show(self, arg): Show command to display the string representation of an object.
        do_destroy(self, arg): Destroy command to remove an object from storage.

    Usage:
        Run this script to enter the interactive command-line interface for the HBNB project.
        Use various commands to create, display, and delete objects stored in the system.
    """

    prompt = "(hbnb) "

    def do_quit(self, arg):
        """
        Quit command to exit the program.
        """
        return True

    def do_EOF(self, arg):
        """
        EOF command to exit the program.
        """
        return True

    def emptyline(self):
        """
        Empty line should not execute anything.
        """
        pass

    def do_create(self, arg):
        """
        Create command to instantiate and save a new object.

        Parameters:
            arg (str): The command argument specifying the class name.

        Notes:
            If the class name is missing, a message will be printed.
            If the class doesn't exist, a message will be printed.
        """
        if not arg:
            print("** class name missing **")
        else:
            try:
                new_instance = BaseModel()
                """save from storage goes here"""
                print(new_instance.id)
            except NameError:
                print("** class doesn't exist **")

    def do_show(self, arg):
        """
        Show command to display the string representation of an object.

        Parameters:
            arg (str): The command argument specifying the class name and object ID.

        Notes:
            If the class name is missing, a message will be printed.
            If the class or instance doesn't exist, a message will be printed.
        """
        if not arg:
            print("** class name missing **")
        try:
            class_name, class_id = arg.split(" ")
            key = f"{class_name}.{class_id}"

            if key in models.storage.all():
                print(models.storage.all()[key])
            else:
                print("** no instance found **")
        except NameError:
            print("** class doesn't exist **")
        except ValueError:
            print("** instance id missing **")

    def do_destroy(self, arg):
        """
        Destroy command to remove an object from storage.

        Parameters:
            arg (str): The command argument specifying the class name and object ID.

        Notes:
            If the class name is missing, a message will be printed.
            If the class or instance doesn't exist, a message will be printed.
        """
        if not arg:
            print("** class name missing **")
        try:
            class_name, class_id = arg.split(" ")
            key = f"{class_name}.{class_id}"

            if key in models.storage.all():
                del models.storage.all()[key]
                """save the changes here"""
            else:
                print("** no instance found **")
        except ValueError:
            print("** instance id missing **")
        except NameError:
            print("** class doesn't exist **")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
