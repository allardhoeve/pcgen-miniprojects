
import re


class LstObject(object):

    class_keywords = []

    general_keywords = [
        "bonus",
        "desc",
        "define",
        "key",
        "outputname",
        'sourcedate',
        'sourcefile',
        'sourcelink',
        'sourcelong',
        'sourcepage',
        'sourceshort',
        'sourceweb',
        'type',
    ]

    lstline = None

    keywords = []

    def __init__(self, line=None, source=None):
        self._initialize_keywords()
        self._initialize_attributes()

        if line is not None:
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

        if key.startswith('!'):
            key = key[1:]

        return key.lower(), value

    def processKeyValue(self, tup):
        (keyword, value) = tup

        if keyword == "desc":
            self.processDescKeyValue(tup)
        elif keyword in self.keywords:
            setattr(self, keyword, value)
        else:
            keywords = sorted(list(set(self.class_keywords) | set(self.general_keywords)))
            raise AttributeError("%s object has no attribute '%s':\n%s" % (self.__class__.__name__,
                                                                           keyword,
                                                                           keywords))

    def processDescKeyValue(self, tup):
        (keyword, value) = tup
        tokens = value.split("|")
        self.desc = tokens[0]

    def processListKeyValue(self, tup, sep="."):
        (keyword, value) = tup

        setattr(self, keyword, value.split(sep))
