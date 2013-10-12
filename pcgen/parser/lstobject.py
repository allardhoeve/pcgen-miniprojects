
import re


class LstObject(object):

    general_keywords = [
        "desc",
        "key",
        "outputname",
        'sourceweb',
        'sourcelong',
        'sourcefile'
    ]

    listline = None

    keywords = []

    def __init__(self, line=None, source=None):
        self._initialize_keywords()
        self._initialize_attributes()

        if not line is None:
            self.parseLine(line)
            self.lstline = line

        if source:
            self.sourcelong = source['sourcelong']
            self.sourcefile = source['sourcefile']

    def _initialize_keywords(self):
        self.keywords = self.general_keywords + self.class_keywords
        self.keywords = list(set(self.keywords))

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
        return (key.lower(), value)

    def processKeyValue(self, tuple):
        (keyword, value) = tuple

        if keyword == "desc":
            self.processDescKeyValue(tuple)
        elif keyword in self.keywords:
            setattr(self, keyword, value)
        else:
            raise AttributeError("SpellLst object has no attribute '%s'" % keyword)

    def processDescKeyValue(self, tuple):
        (keyword, value) = tuple
        tokens = value.split("|")
        self.desc = tokens[0]

    def processListKeyValue(self, tuple, sep="."):
        (keyword, value) = tuple

        setattr(self, keyword, value.split(sep))

