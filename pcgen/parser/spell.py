
from pcgen.parser.lstobject import LstObject


class SpellObject(LstObject):

    class_keywords = ['bonus',
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

    def processKeyValue(self, tuple):
        (keyword, value) = tuple

        if keyword in ["type"]:
            self.processListKeyValue(tuple, ".")
        elif keyword in ["descriptor"]:
            self.processListKeyValue(tuple, "|")
        elif keyword in ["comps"]:
            self.processListKeyValue(tuple, ", ")
        elif keyword in ["classes"]:
            self.processClassKeyValue(tuple)
        else:
            super(SpellObject, self).processKeyValue(tuple)

    def processClassKeyValue(self, tuple):
        (keyword, value) = tuple

        classes = {}
        groups = value.split("|")

        for group in groups:
            (names, level) = group.split("=")
            for name in names.split(","):
                classes[name] = int(level)

        self.classes = classes
