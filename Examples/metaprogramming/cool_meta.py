class CoolMeta(type):

    def __new__(meta, name, bases, dct):
        print('Creating class', name)
        return super().__new__(meta, name, bases, dct)

    def __init__(cls, name, bases, dct):
        print('Initializing class', name)
        super().__init__(name, bases, dct)

    def __call__(cls, *args, **kwargs):
        print('calling CoolMeta to instantiate ', cls)
        #obj = type.__call__(cls, *args, **kwargs)
        obj = type.__call__(cls, *args, **kwargs)
        print(obj)
        return obj


class CoolClass(metaclass=CoolMeta):
    def __init__(self):
        print('And now my CoolClass object exists')


print('everything loaded, instantiate a coolclass object now')

foo = CoolClass()
