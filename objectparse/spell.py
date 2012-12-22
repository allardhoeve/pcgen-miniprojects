
from lstobject import LstObject
import re

class SpellObject(LstObject):

    _keywords = ['bonus',
                 'casttime',
                 'choose',
                 'classes',
                 'comps',
                 'domains',
                 'desc',
                 'descriptor',
                 'duration',
                 'item',
                 'name',
                 'range',
                 'refdoc',
                 'saveinfo',
                 'school',
                 'sourcepage',
                 'spellres',
                 'subschool',
                 'targetarea',
                 'tempdesc',
                 'type',
                 'variants']

    def __init__(self, line = None):

        self._initialize_keywords()
        self._initialize_attributes()

        if not line is None:
            self.parseLine(line)

        super(LstObject, self).__init__()

    def _initialize_keywords(self):
        #self.keywords = super(SpellObject, self)._keywords
        self.keywords = list(set(super(SpellObject, self).keywords + self._keywords))

    def _initialize_attributes(self):
        for keyword in self.keywords:
            setattr(self, keyword, None)

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

        if keyword in self.keywords:
            setattr(self, keyword, value)
        else:
            raise AttributeError("SpellLst object has no attribute '%s'" % keyword)

