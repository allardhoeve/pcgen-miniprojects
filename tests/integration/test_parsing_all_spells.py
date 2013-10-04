from pcgen import find_all_pathfinder_spells
from pcgen.testcase import TestCase


class TestParseAllSpells(TestCase):

    def test_parse_all_spells(self):
        find_all_pathfinder_spells()