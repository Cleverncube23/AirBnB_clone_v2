#!/usr/bin/python3
"""Define Holberton BnB console"""
import cmd
import sys
import shlex
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.city import City
from models.state import State
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.__init__ import storage


class HBNBCommand(cmd.Cmd):
    """
        Starting point of command interpreter
    """

    prompt = "(hbnb) "

    def emptyline(self):
        """pass and do nothing with input line"""
        pass

    def do_quit(self, args):
        """Exit the program"""
        return True

    def do_EOF(self, args):
        """Exit the program with EOF (Ctrl+D)"""
        return True

    def do_create(self, arg):
        """
        Creates a new instance of a specified class with given parameters.

        Usage: create <Class name> <param 1> <param 2> <param 3>...
        Params: <key name>=<value>
                String values: "<value>" (escape internal quotes with backslash)
                Float values: <unit>.<decimal>
                Integer values: <number>
        """
        try:
            args = shlex.split(arg)
            if len(args) == 0:
                print("** class name missing **")
                return

            class_name = args[0]
            if class_name not in ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]:
                print("** class doesn't exist **")
                return

            params = {}
            for param in args[1:]:
                if '=' not in param:
                    continue

                key, value = param.split('=', 1)
                key = key.replace('_', ' ')  # Replace underscores with spaces
                try:
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1].replace('\\"', '"')  # Unescape double quotes
                    elif '.' in value:
                        value = float(value)
                    else:
                        value = int(value)
                    params[key] = value
                except ValueError:
                    continue

            new_instance = eval(f'{class_name}()')
            for key, value in params.items():
                setattr(new_instance, key, value)

            new_instance.save()
            print(new_instance.id)

        except Exception as e:
            print(f"** {e} **")

    def do_show(self, args):
        """Prints string reps of instance based on class name and ID."""
        args = shlex.split(args)
        if len(args) == 0:
            print("** class name missing **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        storage.reload()
        object_dict = storage.all()

        try:
            eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return

        keys = args[0] + "." + args[1]
        try:
            value = object_dict[keys]
            print(value)
        except KeyError:
            print("** no instance found **")

    def do_count(self, args):
        """Counts number of instances."""
        object_list = []
        storage.reload()
        objects = storage.all()

        try:
            if len(args) != 0:
                eval(args)
        except NameError:
            print("** class doesn't exist **")
            return

        for value in objects.values():
            if len(args) != 0 and isinstance(value, eval(args)):
                object_list.append(value)
            elif len(args) == 0:
                object_list.append(value)

        print(len(object_list))

    def do_destroy(self, args):
        """Deletes instance based on class name and id."""
        args = shlex.split(args)
        if len(args) == 0:
            print("** class name missing **")
            return
        elif len(args) == 1:
            print("** instance id missing **")
            return

        class_name = args[0]
        instance_id = args[1]

        storage.reload()
        object_dict = storage.all()

        keys = class_name + "." + instance_id
        try:
            del object_dict[keys]
            storage.save()
        except KeyError:
            print("** no instance found **")

    def do_update(self, args):
        """Updates instance based on name and ID passed in."""
        storage.reload()
        args = shlex.split(args)
        if len(args) == 0:
            print("** class name missing **")
            return
        elif len(args) == 1:
            print("** instance id missing **")
            return
        elif len(args) == 2:
            print("** attribute name missing **")
            return
        elif len(args) == 3:
            print("** value missing **")
            return

        class_name = args[0]
        instance_id = args[1]
        attribute_name = args[2]
        attribute_value = args[3]

        object_dict = storage.all()
        keys = class_name + "." + instance_id

        try:
            instance = object_dict[keys]
        except KeyError:
            print("** no instance found **")
            return

        try:
            attribute_type = type(getattr(instance, attribute_name))
            attribute_value = attribute_type(attribute_value)
        except AttributeError:
            pass

        setattr(instance, attribute_name, attribute_value)
        instance.save()

    def do_all(self, args):
        """Prints string reps of all instances."""
        object_list = []
        storage.reload()
        objects = storage.all()

        try:
            if len(args) != 0:
                eval(args)
        except NameError:
            print("** class doesn't exist **")
            return

        for value in objects.values():
            if len(args) != 0 and isinstance(value, eval(args)):
                object_list.append(value.__str__())
            elif len(args) == 0:
                object_list.append(value.__str__())

        print(object_list)

if __name__ == "__main__":
    """Start point for loop."""
    HBNBCommand().cmdloop()
