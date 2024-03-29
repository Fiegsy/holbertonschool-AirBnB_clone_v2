import cmd
import sys
import shlex
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

    classes = {
        'BaseModel': BaseModel, 'User': User, 'Place': Place,
        'State': State, 'City': City, 'Amenity': Amenity,
        'Review': Review
    }

    

    def do_create(self, args):
        """Create an object of any class"""
        if not args:
            print("** class name missing **")
            return

        arg_list = shlex.split(args)

        class_name = arg_list[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

       
        params = {}
        for param in arg_list[1:]:
            key, value = param.split('=')
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]  
                value = value.replace('_', ' ')  
                params[key] = value

        
        obj = self.classes[class_name](**params)
        obj.save()
        print(obj.id)

    

if __name__ == "__main__":
    HBNBCommand().cmdloop()
