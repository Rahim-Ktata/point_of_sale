
from enum import Enum

class BasicEnum(str,Enum):

    @classmethod
    def getPossibleValues(cls):
        return [val.value for val in cls]

    @classmethod
    def isValidEnumValue(cls,field):
        for val in cls:
            if field.strip().upper() == val.value.upper():
                return val

        return None
