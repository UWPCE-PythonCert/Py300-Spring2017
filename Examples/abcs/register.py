# demo of registering with an ABC

import collections.abc


@collections.abc.Sequence.register
class MyKindOfSequence():

    def __init__(self, an_iterable):
        self.contents = list(an_iterable)

    def __len__(self):
        return len(self.contents)

# now make one:
s = MyKindOfSequence((3,6,4,8))

