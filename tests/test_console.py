#!/usr/bin/python3
"""
Unit tests for the HBNBCommand class in the console module
"""

import os
import sys
import unittest
from console import HBNBCommand
import unittest
from unittest.mock import patch
from io import StringIO
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class testHBNBCommand(unittest.TestCase):
    """Test cases"""

    classes = [BaseModel, User, State, City, Amenity, Place, Review]

    def setUp(self):
        """Cleans storage data."""
        FileStorage._FileStorage__objects.clear()

        file_path = FileStorage._FileStorage__file_path
        if os.path.isfile(file_path):
            os.remove(file_path)

    def test_prompt_string(self):
        """Checks HBNBCommand class prompt"""
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_empty_line(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("\n")

            self.assertEqual("", f.getvalue().strip())

    def test_help(self):
        """Tests the help command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help")
        output = """
Documented commands (type help <topic>):
========================================
EOF  all  create  destroy  help  quit  show  update

"""
        self.assertEqual(output, f.getvalue())

    def test_help_quit(self):
        """
        Test help command for quit.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help quit")
        output = "Quit command to exit the program"
        self.assertEqual(output, f.getvalue().strip())

    def test_help_EOF(self):
        """
        Test help command for EOF.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help EOF")
        output = "EOF command to exit the program"
        self.assertEqual(output, f.getvalue().strip())

    def test_help_create(self):
        """
        Test help command for create.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help create")
        output = "Create a new instance of a class and print its ID"
        self.assertEqual(output, f.getvalue().strip())

    def test_help_show(self):
        """
        Test help command for show.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help show")
        output = "Display information about a specific instance"
        self.assertEqual(output, f.getvalue().strip())

    def test_help_destroy(self):
        """
        Test help command for destroy.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help destroy")
        output = "Delete a specific instance"
        self.assertEqual(output, f.getvalue().strip())

    def test_help_all(self):
        """
        Test help command for all.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help all")
        output = "Display all instances or instances of a specific class"
        self.assertEqual(output, f.getvalue().strip())

    def test_help_update(self):
        """
        Test help command for update.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help update")
        output = "Update an instance based on its ID"
        self.assertEqual(output, f.getvalue().strip())

    def test_create(self):
        """
        Test create command.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"create BaseModel")
            output = f.getvalue().strip()

            self.assertTrue(output)

    def test_show(self):
        """
        Test show command.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"create BaseModel")
            output = f.getvalue().strip()

            with patch('sys.stdout', new=StringIO()) as fs:
                HBNBCommand().onecmd(f"show BaseModel {output}")
                show_output = fs.getvalue().strip()

            self.assertIn(output, show_output)

    def test_destroy(self):
        """
        Test destroy command.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"create BaseModel")
            output = f.getvalue().strip()

            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"destroy BaseModel {output}")

            with patch('sys.stdout', new=StringIO()) as fs:
                HBNBCommand().onecmd(f"show BaseModel {output}")
                show_output = fs.getvalue().strip()

            results = '"** no instance found **"'
            self.assertIn(show_output, results)

    def test_all(self):
        """
        Test all command.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"create BaseModel")
            output = f.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f2:
            HBNBCommand().onecmd(f"create User")
            user_output = f2.getvalue().strip()

            with patch('sys.stdout', new=StringIO()) as f_all:
                HBNBCommand().onecmd("all")
                all_output = f_all.getvalue().strip()

            with patch('sys.stdout', new=StringIO()) as f_base:
                HBNBCommand().onecmd("all BaseModel")
                base_output = f_base.getvalue().strip()

            self.assertIn(output, all_output)
            self.assertIn(user_output, all_output)
            self.assertIn(output, base_output)

    def test_update(self):
        """
        Test update command.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"create BaseModel")
            output = f.getvalue().strip()
            update_str = f'update BaseModel {output} name "John"'

            with patch('sys.stdout', new=StringIO()) as f_all:
                HBNBCommand().onecmd(f"{update_str}")

            with patch('sys.stdout', new=StringIO()) as fs:
                HBNBCommand().onecmd(f"show BaseModel {output}")
                show_output = fs.getvalue().strip()

            updated = "'name': 'John'"
            self.assertIn(updated, show_output)

    def test_create_errors(self):
        """
        Test create command with errors.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"create")
            output = f.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f2:
            HBNBCommand().onecmd(f"create MyModel")
            output2 = f2.getvalue().strip()

            self.assertEqual(output, "** class name missing **")
            self.assertEqual(output2, "** class doesn't exist **")

    def test_show_errors(self):
        """
        Test show command with errors.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show")
            output = f.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f2:
            HBNBCommand().onecmd("show MyModel")
            output2 = f2.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f3:
            HBNBCommand().onecmd(f"show BaseModel")
            output3 = f3.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f4:
            HBNBCommand().onecmd("show BaseModel 1123")
            output4 = f4.getvalue().strip()

            self.assertEqual(output, "** class name missing **")
            self.assertEqual(output2, "** class doesn't exist **")
            self.assertEqual(output3, "** instance id missing **")
            self.assertEqual(output4, "** no instance found **")

    def test_destroy_errors(self):
        """
        Test destroy command with errors.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy")
            output = f.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f2:
            HBNBCommand().onecmd("destroy MyModel")
            output2 = f2.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f3:
            HBNBCommand().onecmd(f"destroy BaseModel")
            output3 = f3.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f4:
            HBNBCommand().onecmd("destroy BaseModel 1123")
            output4 = f4.getvalue().strip()

            self.assertEqual(output, "** class name missing **")
            self.assertEqual(output2, "** class doesn't exist **")
            self.assertEqual(output3, "** instance id missing **")
            self.assertEqual(output4, "** no instance found **")

    def test_all_erors(self):
        """
        Test all command with errors.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"all MyModel")
            output = f.getvalue().strip()

            self.assertEqual(output, "** class doesn't exist **")

    def test_update_errors(self):
        """
        Test update command with errors.
        """
        with patch('sys.stdout', new=StringIO()) as fc:
            HBNBCommand().onecmd("create BaseModel")
            id = fc.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update")
            output = f.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f2:
            HBNBCommand().onecmd("update MyModel")
            output2 = f2.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f3:
            HBNBCommand().onecmd(f"update BaseModel")
            output3 = f3.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f4:
            HBNBCommand().onecmd("update BaseModel 1123")
            output4 = f4.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f5:
            HBNBCommand().onecmd(f"update BaseModel {id}")
            output5 = f5.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f6:
            HBNBCommand().onecmd(f"update BaseModel {id} name")
            output6 = f6.getvalue().strip()

            self.assertEqual(output, "** class name missing **")
            self.assertEqual(output2, "** class doesn't exist **")
            self.assertEqual(output3, "** instance id missing **")
            self.assertEqual(output4, "** no instance found **")
            self.assertEqual(output5, "** attribute name missing **")
            self.assertEqual(output6, "** value missing **")

    def test_user_all(self):
        """
        Test all command for User class.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"create User")
            output = f.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f2:
            HBNBCommand().onecmd(f"create User")
            user_output = f2.getvalue().strip()

            with patch('sys.stdout', new=StringIO()) as f_all:
                HBNBCommand().onecmd("User.all()")
                all_output = f_all.getvalue().strip()

            self.assertIn(output, all_output)
            self.assertIn(user_output, all_output)

    def test_user_count(self):
        """
        Test count command for User class.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"create User")
            output = f.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f2:
            HBNBCommand().onecmd(f"create User")
            user_output = f2.getvalue().strip()

            with patch('sys.stdout', new=StringIO()) as f_all:
                HBNBCommand().onecmd("User.count()")
                all_output = f_all.getvalue().strip()

            self.assertEqual(all_output, '2')

    def test_user_show(self):
        """
        Test show command for User class.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"create User")
            output = f.getvalue().strip()

            with patch('sys.stdout', new=StringIO()) as f2:
                HBNBCommand().onecmd(f'User.show("{output}")')
                user_output = f2.getvalue().strip()

            with patch('sys.stdout', new=StringIO()) as f_all:
                HBNBCommand().onecmd('User.show("bar"")')
                e_output = f_all.getvalue().strip()

            self.assertIn(output, user_output)
            self.assertEqual(e_output, "** no instance found **")

    def test_user_destroy(self):
        """
        Test destroy command for User class.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"create User")
            output = f.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f2:
            HBNBCommand().onecmd(f"create User")
            user_output = f2.getvalue().strip()

            with patch('sys.stdout', new=StringIO()) as f_all:
                HBNBCommand().onecmd(f'User.destroy("{output}")')
                all_output = f_all.getvalue().strip()

            with patch('sys.stdout', new=StringIO()) as f_all:
                HBNBCommand().onecmd("User.count()")
                all_output = f_all.getvalue().strip()

            self.assertEqual(all_output, '1')

    def test_user_update(self):
        """
        Test update command for User class.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"create User")
            output = f.getvalue().strip()
            update_str = f'User.update("{output}", "name", "John")'

            with patch('sys.stdout', new=StringIO()) as f_all:
                HBNBCommand().onecmd(f"{update_str}")

            with patch('sys.stdout', new=StringIO()) as fs:
                HBNBCommand().onecmd(f"show User {output}")
                show_output = fs.getvalue().strip()

            updated = "'name': 'John'"
            self.assertIn(updated, show_output)

    def test_user_update_dict(self):
        """
        Test update command with dictionary for User class.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"create User")
            output = f.getvalue().strip()
            dict_ = {"name": "John", "food": "Rice"}
            update_str = f'User.update("{output}", {dict_})'

            with patch('sys.stdout', new=StringIO()) as f_all:
                HBNBCommand().onecmd(f"{update_str}")

            with patch('sys.stdout', new=StringIO()) as fs:
                HBNBCommand().onecmd(f"show User {output}")
                show_output = fs.getvalue().strip()

            updated = "'name': 'John'"
            updated2 = "'food': 'Rice'"
            self.assertIn(updated, show_output)
            self.assertIn(updated2, show_output)


if __name__ == "__main__":
    unittest.main()
