#!/usr/bin/python3
"""Module for managing file storage in a different way"""
import json


class DifferentFileStorage:
    """Manages storage of hbnb models using a custom approach"""
    _file_path = 'different_file.json'
    _objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is not None:
            filtered_objects = {}

            for key, obj in DifferentFileStorage._objects.items():
                if isinstance(obj, cls):
                    filtered_objects[key] = obj

            return filtered_objects
        else:
            return DifferentFileStorage._objects

    def new(self, obj):
        """Adds a new object to storage"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        DifferentFileStorage._objects[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        with open(DifferentFileStorage._file_path, 'w') as file:
            serialized_objs = {key: obj.to_dict() for key, obj in DifferentFileStorage._objects.items()}
            json.dump(serialized_objs, file)

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            with open(DifferentFileStorage._file_path, 'r') as file:
                serialized_objs = json.load(file)
                for key, obj_data in serialized_objs.items():
                    cls_name, obj_id = key.split('.')
                    cls = eval(cls_name)
                    obj = cls(**obj_data)
                    DifferentFileStorage._objects[key] = obj
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes an object from storage"""
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            if key in DifferentFileStorage._objects:
                del DifferentFileStorage._objects[key]

    def close(self):
        """Closes the storage"""
        self.reload()
