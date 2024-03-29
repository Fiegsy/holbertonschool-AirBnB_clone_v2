#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Contains the functionality for the HBNB console"""

    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''
    classes = {'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review}

    def precmd(self, line):
        """Reformat command line for advanced command syntax."""
        if '.' in line and '(' in line and ')' in line:
            parts = line.split('(')
            cls_and_cmd = parts[0].split('.')
            if len(cls_and_cmd) == 2:
                cls, cmd = cls_and_cmd
                args = parts[1][:-1]
                line = f'{cmd} {cls} {args}'
        return line

    def postcmd(self, stop, line):
        """Print prompt after command execution."""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def emptyline(self):
        """Override the emptyline method of CMD."""
        pass

    def do_quit(self, line):
        """Exit the HBNB console."""
        return True

    def do_EOF(self, line):
        """Exit the HBNB console on EOF."""
        print()
        return True

    def do_create(self, args):
        """Create an object of any class."""
        if not args:
            print("** class name missing **")
            return

        cls_name, *attributes = args.split()
        if cls_name not in self.classes:
            print("** class doesn't exist **")
            return

        params = {}
        for attribute in attributes:
            if '=' not in attribute:
                print("** invalid attribute format, use key=value **")
                return
            key, value = attribute.split("=")
            params[key] = value.strip('"').replace("_", " ")

        try:
            new_instance = self.classes[cls_name](**params)
            storage.new(new_instance)
            print(new_instance.id)
            storage.save()
        except Exception as e:
            print(f"Error creating instance: {e}")

    def do_show(self, args):
        """Show an individual object."""
        cls_name, obj_id = self.parse_cls_and_id(args)
        if not cls_name or not obj_id:
            return
        key = f"{cls_name}.{obj_id}"
        obj = storage.get(cls_name, obj_id)
        if obj:
            print(obj)
        else:
            print("** no instance found **")

    def do_destroy(self, args):
        """Destroy a specified object."""
        cls_name, obj_id = self.parse_cls_and_id(args)
        if not cls_name or not obj_id:
            return
        key = f"{cls_name}.{obj_id}"
        obj = storage.get(cls_name, obj_id)
        if obj:
            del storage.all()[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, args):
        """Show all objects, or all objects of a class."""
        if args:
            cls_name = args.split()[0]
            if cls_name not in self.classes:
                print("** class doesn't exist **")
                return
            objects = [str(obj) for obj in storage.all().values()
                       if type(obj).__name__ == cls_name]
        else:
            objects = [str(obj) for obj in storage.all().values()]
        print(objects)

    def do_update(self, args):
        """Update a certain object with new info."""
        cls_name, obj_id, att_name, att_val = self.parse_update_args(args)
        if not cls_name or not obj_id or not att_name or not att_val:
            return
        key = f"{cls_name}.{obj_id}"
        obj = storage.get(cls_name, obj_id)
        if obj:
            setattr(obj, att_name, att_val)
            storage.save()
        else:
            print("** no instance found **")

    def parse_cls_and_id(self, args):
        """Parse class name and object ID."""
        parts = args.split()
        if len(parts) < 1:
            print("** class name missing **")
            return None, None
        cls_name = parts[0]
