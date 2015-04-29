from defusedxml import lxml
from pcgen import settings
from pcgen.testcase import TestCase
from pcgen.xml.parser import parse_spells_per_day


class TestParseSpellsPerDay(TestCase):

    def setUp(self):
        with open(settings.PROJECTROOT.child("fixture").child("Saenvan level 12.xml")) as file:
            self.xml = file.read()
            self.root = lxml.fromstring(self.xml)

    def test_parse_spells_per_day_per_level_parses_spells_per_day_correctly(self):
        ret = parse_spells_per_day(self.root)
        self.assertEqual(ret.keys(), ["cleric"])
        self.assertEqual(ret["cleric"][0], (4, 0))
        self.assertEqual(ret["cleric"][1], (6, 1))
        self.assertEqual(ret["cleric"][2], (6, 1))
        self.assertEqual(ret["cleric"][3], (6, 1))
        self.assertEqual(ret["cleric"][4], (4, 1))
        self.assertEqual(ret["cleric"][5], (4, 1))
        self.assertEqual(ret["cleric"][6], (3, 1))
        self.assertEqual(ret["cleric"][7], (0, 0))
        self.assertEqual(ret["cleric"][8], (0, 0))
        self.assertEqual(ret["cleric"][9], (0, 0))


