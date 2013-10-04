import mock
from pcgen import settings
from pcgen.parser import read_lst_file, SpellObject

from pcgen.testcase import TestCase


class TestSpellObject(TestCase):

    def setUp(self):
        self.test_spells = settings.DATADIR.child("core_rulebook").child("pfcr_spells.lst")
        self.test_lines = read_lst_file(self.test_spells)

    def _get_line_and_check(self, ln, name):
        testline = self.test_lines[ln]
        self.assertTrue(testline.startswith("%s\t" % name), "Line %d is not %s: %s" % (ln + 1, name, self.test_lines[ln]))
        return testline

    def test_parse_keyword_returns_correct_tuple(self):
        tuple = SpellObject().parseKeyword("SCHOOL:Evocation")
        self.assertEquals(tuple, ("school", "Evocation"))

    def test_parse_keyvalue_sets_school_when_given(self):
        blank = SpellObject()
        blank.processKeyValue(("school", "Evocation"))
        self.assertEquals(blank.school, "Evocation")

    def test_parse_list_keyvalue_sets_list(self):
        blank = SpellObject()
        blank.processListKeyValue(("type", "Arcane.Divine"))
        self.assertEquals(blank.type, ["Arcane", "Divine"])

    def test_parse_line_calls_parse_keyword_and_process_key_value_once_for_each_keyword(self):
        blank = SpellObject()
        mock_keyword = blank.parseKeyword = mock.Mock(return_value=[("school", "Evocation"), ("spellres", "No")])
        mock_parsekey = blank.processKeyValue = mock.Mock()

        blank.parseLine("Acid Splash\tSCHOOL:Evocation\t\tSPELLRES:No")

        mock_keyword.assert_has_calls([mock.call("SCHOOL:Evocation"),
                                       mock.call("SPELLRES:No")])
        mock_parsekey.assert_hash_calls([mock.call(("school", "Evocation")),
                                         mock.call(("spellres", "No"))])

    def test_no_line_in_testdata_gives_an_error_parsing(self):
        objects = map(SpellObject, self.test_lines)

    def test_alarm_object_has_correct_type_list(self):
        testline = self._get_line_and_check(5, "Alarm")
        alarm = SpellObject(testline)

        self.assertEquals(alarm.name, "Alarm")
        self.assertEquals(alarm.type, ["Arcane", "Divine"])

        # self.print_class_keywords(alarm)

    def test_bane_object_has_correct_descriptor_list(self):
        testline = self._get_line_and_check(31, "Bane")
        bane = SpellObject(testline)
        self.assertEquals(bane.descriptor, ["Fear", "Mind-Affecting"])

        # self.print_class_keywords(bane)

    def test_banishment_has_correct_classes_dict(self):
        testline = self._get_line_and_check(32, "Banishment")
        banishment = SpellObject(testline)
        self.assertEquals(banishment.classes, {"Cleric": 6, "Sorcerer": 7, "Wizard": 7})

        # self.print_class_keywords(banishment)

    def test_acid_splash_object_has_correct_attributes(self):
        testline = self._get_line_and_check(2, "Acid Splash")
        acid_splash = SpellObject(testline)

        self.assertEquals(acid_splash.name, "Acid Splash")
        self.assertEquals(acid_splash.desc, "You fire a small orb of acid at the target dealing 1d3 points of acid damage.")
        self.assertEquals(acid_splash.school, "Conjuration")
        self.assertEquals(acid_splash.descriptor, ["Acid"])
        self.assertEquals(acid_splash.spellres, "No")
        self.assertEquals(acid_splash.refdoc, None)
        self.assertEquals(acid_splash.subschool, "Creation")
        self.assertEquals(acid_splash.type, ["Arcane"])
        self.assertEquals(acid_splash.comps, ["V", "S"])
        self.assertEquals(acid_splash.classes, {"Sorcerer": 0, "Wizard": 0})

        # self.print_class_keywords(acid_splash)

    def print_class_keywords(self, object):
        import sys
        print >>sys.stderr, "\n\n%s\n" % object.name.upper()
        for keyword in object.keywords:
            print >>sys.stderr, "'%s' -> '%s'" % (keyword, getattr(object, keyword))