
from datetime import datetime

class TagInstance:
    """ An instance of a tag containing times and value. """

    def __init__(self, value:int, time=None, day=None):
        self.time = time or datetime.now().time()
        self.day = day or datetime.now().weekday()
        self.value = value

    def serialize(self):
        """ Serialize the tag in a deterministic manner for hashing. """
        pass

class TagRules:
    """ A class representing authorization rules """

    def __init__(self, maxvalue:int, time=None, day=None):
        self.time = time            # [begin, end] instances of datetime.time
        self.day = day              # bitmask [M,T,W,Th,F,S,Su] given by datetime.weekday()
        self.maxvalue = maxvalue    # integer in satoshis
        pass

    def validate(self, tag:TagInstance):
        """ Validate that the constraints in the tag are satisfied. """
        now = datetime.now()
        if self.time is not None and not (self.time[0] < now.time() < self.time[1]):
            raise TimeTagFailure()
        if self.day is not None and now().weekday() not in self.day:
            raise DayTagFailure()
        if self.maxvalue is not None and tag.value > self.maxvalue:
            raise ValueTagFailure()

        return True

    def serialize(self):
        """ Serialize the tag in a deterministic manner for hashing. """
        pass

class DayTagFailure(Exception):
    """ An exception class for when the day of week tag fails. """
    pass

class TimeTagFailure(Exception):
    """ An exception class for when the time of day tag fails. """
    pass

class ValueTagFailure(Exception):
    """ An exception class for when the value tag fails. """
    pass
