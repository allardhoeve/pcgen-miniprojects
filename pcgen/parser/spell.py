
from pcgen.parser.lstobject import LstObject


class SpellObject(LstObject):

    class_keywords = ['bonus',
                      'casttime',
                      'choose',
                      'classes',
                      'comps',
                      'cost',
                      'domains',
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

    class_keywords_skip = ['tempbonus']

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
        elif keyword in self.class_keywords_skip:
            return
        elif keyword.startswith("pre"):
            return
        else:
            super(SpellObject, self).processKeyValue(tuple)

    def processClassKeyValue(self, tuple):
        (keyword, value) = tuple

        classes = {}
        groups = value.split("|")

        for group in groups:
            (names, level) = group.split("=", 1)

            leveltokens = level.split("[")  # preconditions on the level exist
            level = leveltokens[0]

            for name in names.split(","):
                classes[name] = int(level)

        self.classes = classes

    def __repr__(self):
        return "<Spell [%s]>" % self.name