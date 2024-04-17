import json
from os.path import isfile


class FileStorage:
    """Class for serializing and deserializing Python objects"""

    __file_path = 'instance.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a list of objects of a specific class or all objects"""

        if cls is None:
            return list(self.__objects.values())
        else:
            return [obj for obj in self.__objects.values() if isinstance(obj, cls)]

    def new(self, obj):
        """Adds a new object to __objects"""

        key = '{}.{}'.format(obj.__class__.__name__, obj.id)
        value = obj.to_dict()
        self.__objects[key] = value

    def save(self):
        """Serializes __objects to the JSON file"""

        with open(self.__file_path, 'w+') as f:
            json.dump(self.__objects, f)

    def reload(self):
        """Deserializes the JSON file to __objects"""

        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        if isfile(self.__file_path):
            with open(self.__file_path, 'r') as f:
                obj_dict = json.load(f)
                for key, value in obj_dict.items():
                    class_name = value['__class__']
                    if class_name == 'BaseModel':
                        instance = BaseModel(**value)
                    elif class_name == 'User':
                        instance = User(**value)
                    elif class_name == 'State':
                        instance = State(**value)
                    elif class_name == 'City':
                        instance = City(**value)
                    elif class_name == 'Amenity':
                        instance = Amenity(**value)
                    elif class_name == 'Place':
                        instance = Place(**value)
                    elif class_name == 'Review':
                        instance = Review(**value)
                    self.__objects[key] = instance

    def delete(self, obj=None):
        """Deletes an object from __objects if it exists"""

        if obj is not None:
            key = '{}.{}'.format(obj.__class__.__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]
                self.save()  # Save changes after deletion
