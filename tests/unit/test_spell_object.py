
import objectparse
import objectparse.test
from objectparse import SpellObject
import mock


class TestSpellObject(objectparse.test.TestCase):

    def setUp(self):
        self.testlines = objectparse.read_lst_file("testdata/pfcr_spells.lst")

    def test_parse_keyword_returns_correct_tuple(self):
        tuple = SpellObject().parseKeyword("SCHOOL:Evocation")
        self.assertEquals(tuple, ("SCHOOL", "Evocation"))

    def test_parse_keyvalue_sets_school_when_given(self):
        blank = SpellObject()
        blank.processKeyValue(("SCHOOL", "Evocation"))
        self.assertEquals(blank.school, "Evocation")

    def test_parse_line_calls_parse_keyword_and_process_key_value_once_for_each_keyword(self):
        blank = SpellObject()
        mock_keyword = blank.parseKeyword = mock.Mock(return_value=[("SCHOOL", "Evocation"), ("SPELLRES", "No")])
        mock_parsekey = blank.processKeyValue = mock.Mock()
        blank.parseLine("Acid Splash\tSCHOOL:Evocation\t\tSPELLRES:No")

        mock_keyword.assert_has_calls([mock.call("SCHOOL:Evocation"),
                                       mock.call("SPELLRES:No")])
        mock_parsekey.assert_hash_calls([mock.call(("SCHOOL", "Evocation")),
                                         mock.call(("SPELLRES", "No"))])

    def test_no_line_in_testdata_gives_an_error_parsing(self):
        objects = map(SpellObject, self.testlines)

    def test_acid_splash_object_has_correct_attributes(self):
        self.assertTrue(self.testlines[2].startswith("Acid Splash"), "Line 3 is not Acid Splash: %s" % self.testlines[2])
        acid_splash = SpellObject(self.testlines[2])
        self.assertEquals(acid_splash.name, 'Acid Splash')
        self.assertEquals(acid_splash.school, 'Conjuration')
        self.assertEquals(acid_splash.descriptor, 'Acid')
        self.assertEquals(acid_splash.spellres, 'No')
        self.assertEquals(acid_splash.refdoc, None)
