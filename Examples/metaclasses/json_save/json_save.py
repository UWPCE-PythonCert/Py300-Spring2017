#!/usr/bin/env python3

"""
json_save

metaclass based system for saving objects in a JSON format

This could be useful, but it's kept simple to shoe the use of metaclasses

The idea is that you subclass from JsonSavable, and then you get an object
that be saved and reloaded to/from JSON

"""

import json

class Savable():

    @staticmethod
    def to_json(val):
        """
        returns a json-compatible version of val

        should be overridden in savable types that are not json compatible.
        """
        return val

    @staticmethod
    def to_python(val):
        """
        convert from a json version to the python version

        Must be overridden if not a one-to-one match

        This is where validation could be added as well.
        """
        return val


class Int(Savable):
    default = 0

    @staticmethod
    def to_python(val):
        """
        Convert a number to a python integer
        """
        return int(val)


class Float(Savable):
    default = 0.0

    @staticmethod
    def to_python(val):
        """
        Convert a number to a python float
        """
        return float(val)


class String(Savable):
    default = ""


class Tuple(Savable):
    """
    this assumes that whatever is in the tuple is Savable as well
    """
    default = ()

    @staticmethod
    def to_python(val):
        """
        Convert a array to a tuple -- json only has one array type,
        which matches to a list.
        """
        return tuple(val)


class List(Savable):
    """
    this assumes that whatever in in the list is Savable as well
    """
    default = []

    @staticmethod
    def to_python(val):
        """
        Convert an array to a list -- json only has one array type,
        which matches to a list, so this isn't really required --
        but it is her for completeness sake
        """
        return tuple(val)


class Dict(Savable):
    """
    this assumes that whatever in the dict is Savable as well
    """
    default = {}


class MetaJsonSavable(type):
    """
    The metaclass for creating JsonSavable object

    Deriving from type makes it a metaclass!
    """
    def __init__(cls, name, bases, attr_dict):
        # it gets the class object as the first param.
        # and then the same parameters as the type() factory function
        # you want to call the regular type initilizer:
        super().__init__(name, bases, attr_dict)
        print("in MetaJsonSavable __init__")
        print(cls, name, bases)
        print("attributes of the wrapped class are:", attr_dict.keys())
        # here's where we work with the class attributes:
        # cls._attrs_to_save = [] # keep a list of the attributes to save
        for key, attr in attr_dict.items():
            if isinstance(attr, Savable):
                cls._attrs_to_save[key] = attr


class JsonSavable(metaclass=MetaJsonSavable):
    """
    mixing for JsonSavable objects
    """

    _attrs_to_save = {}  # these will the atrributes that get saved and
                         # reconstructed from json.

    def __new__(cls, *args, **kwargs):
        """
        This adds instance attributes to assure they are all there, even if
        they are not set in the subclasses __init__
        """
        # create the instance
        obj = super().__new__(cls)
        # set the instance attributes to defaults
        for attr, typ in cls._attrs_to_save.items():
            setattr(obj, attr, typ.default)
        return obj

    def __init__(self):
        print ("in JsonSavable __init__")

    def to_json_dict(self):
        """
        converts this object to a json-compatible dict.

        returns the dict
        """
        dic = {}
        for attr, typ in self._attrs_to_save.items():
            dic[attr] = typ.to_json(getattr(self, attr))
        return dic

    @classmethod
    def from_json_dict(cls, dic):
        """
        creates an instance of this class populated by the contents of
        the json compatible dict

        the object is created with __new__ before setting the attributes
        Then __init__ is called, in case there is any additional initialization
        that has to go on.
        """
        # create a new object
        obj = cls.__new__(cls)
        for attr, typ in cls._attrs_to_save.items():
            setattr(obj, attr, typ.to_python(dic[attr]))
        # make sure it gets initialized
        obj.__init__()
        return obj

    def to_json(self, fp=None, indent=4):
        """
        Converts the object to JSON

        :param fp=None: an open file_like object to write the json to.
                        If it is None, then a string with the JSON
                        will be returned as a string

        :param indent=4: The indentation level desired in the JSON
        """
        if fp is None:
            return json.dumps(self.to_json_dict(), indent=indent)
        else:
            json.dump(self.to_json_dict(), fp, indent=indent)

    def __str__(self):
        msg = ["{} object, with attributes:".format(self.__class__)]
        for attr in self._attrs_to_save.keys():
            msg.append("{}: {}".format(attr, getattr(self, attr)))
        return "\n".join(msg)


# Example of using it.
class MyClass(JsonSavable):

    x = Int()
    y = Float()

    def __init__(self, x=None):
        print("in MyClass.__init__", x)
        if x is not None:
            self.x = x
        print("attrs_to_save", self._attrs_to_save)

# create one:
print("about to create a subclass")
mc = MyClass(5)

print(mc)

print(mc.to_json_dict())

# re-create it from the dict:
print(MyClass.from_json_dict(mc.to_json_dict()))

print (mc.to_json())





