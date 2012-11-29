
from lstobject import LstObject
import re

class SpellObject(LstObject):

    name = None
    school = None
    refdoc = None

    def __init__(self, line = None):
        if not line is None:
            self.parseLine(line)

    def parseLine(self, line):
        fields = re.split('\t+', line)
        self.name = fields[0]
        del fields[0]

        map(self.processKeyValue,
                map(self.parseKeyword, fields))

    def parseKeyword(self, keyword):
        (key, value) = keyword.split(':', 1)
        return (key, value)

    def processKeyValue(self, tuple):
        keyword = tuple[0]
        value = tuple[1]

        if keyword == "SCHOOL":
            self.school = value
        if keyword == "DESCRIPTOR":
            self.descriptor = value
        if keyword == "REFDOC":
            self.refdoc = valuet



