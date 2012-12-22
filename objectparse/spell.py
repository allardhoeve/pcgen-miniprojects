
from lstobject import LstObject
import re

class SpellObject(LstObject):

    desc = None

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
        keyword = tuple[0].lower()
        value = tuple[1]

        if keyword in ['casttime',
                       'comps',
                       'duration',
                       'name',
                       'range',
                       'refdoc',
                       'saveinfo',
                       'school',
                       'sourcepage',
                       'spellres',
                       'subschool',
                       'targetarea',
                       'type']:
            setattr(self, keyword.lower(), value)

        elif keyword == 'desc':
            if self.desc:
                self.desc = self.desc + value
            else:
                self.desc = value

        elif keyword == 'descriptor':
            self.descriptor = value

        elif keyword == 'classes':
            self.classes = value

        else:
            raise AttributeError("SpellLst object has no attribute %s" % keyword)

