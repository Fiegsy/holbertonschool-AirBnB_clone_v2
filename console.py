#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.state import State
from models.city import City
from models.user import User
from models.place import Place


class HBNBCommand(cmd.Cmd):
    """Contains the functionality for the HBNB console"""

    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''
    classes = {'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City}

    def do_create(self, args):
        """Create an object of any class."""
        if not args:
            print("** class name missing **")
            return

        args = args.split()
        class_name = args[0]

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        params = {}
        for arg in args[1:]:
            if '=' not in arg:
                print("** invalid attribute format, use key=value **")
                return
            key, value = arg.split("=")
            params[key] = value.strip('"').replace("_", " ")

        try:
            new_instance = self.classes[class_name](**params)
            storage.new(new_instance)
            storage.save()
            print(new_instance.id)
        except Exception as e:
            print(f"Error creating instance: {e}")

    def do_show(self, args):
        """Show an individual object."""
        if not args:
            print("** class name missing **")
            return

        args = args.split()
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        obj_id = args[1]
        objs = storage.all()

        key = f"{args[0]}.{obj_id}"
        obj = objs.get(key)
        if obj:
            print(obj)
        else:
            print("** no instance found **")

    def do_destroy(self, args):
        """Destroy a specified object."""
        if not args:
            print("** class name missing **")
            return

        args = args.split()
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        obj_id = args[1]
        objs = storage.all()

        key = f"{args[0]}.{obj_id}"
        obj = objs.get(key)
        if obj:
            del objs[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_update(self, args):
        """Update a certain object with new info."""
        if not args:
            print("** class name missing **")
            return

        args = args.split()
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        obj_id = args[1]
        objs = storage.all()

        key = f"{args[0]}.{obj_id}"
        obj = objs.get(key)

        if not obj:
            print("** no instance found **")
            return

        if len(args) < 3:
            print("** attribute name missing **")
            return

        if len(args) < 4:
            print("** value missing **")
            return

        attr_name = args[2]
        attr_value = args[3].strip('"')

        if hasattr(obj, attr_name):
            attr_type = type(getattr(obj, attr_name))
            setattr(obj, attr_name, attr_type(attr_value))
            storage.save()
        else:
            print("** attribute doesn't exist **")

    def emptyline(self):
        """Override the emptyline method of CMD."""
        pass

    def do_quit(self, args):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, args):
        """EOF command to exit the program."""
        print()
        return True


if __name__ == "__main__":
    HBNBCommand().cmdloop()
