
from pcgen.parser.lstobject import LstObject


class SpellObject(LstObject):

    class_keywords = ['casttime',
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
                      'spellres',
                      'subschool',
                      'targetarea',
                      'tempdesc',
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
        elif keyword in ["classes", "domains"]:
            self.processSpellListKeyValue(tuple)
        elif keyword in self.class_keywords_skip:
            return
        elif keyword.startswith("pre"):
            return
        else:
            super(SpellObject, self).processKeyValue(tuple)

    def processSpellListKeyValue(self, tuple):
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
