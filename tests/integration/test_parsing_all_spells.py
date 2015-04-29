from pcgen import find_all_pathfinder_spells
from pcgen.testcase import TestCase


class TestParseAllSpells(TestCase):

    def test_parse_all_spells(self):
        spells = find_all_pathfinder_spells()

        for spell in spells:
            self.assertIsNotNone(spell.sourcelong, "SOURCELONG for %s is None" % spell)
