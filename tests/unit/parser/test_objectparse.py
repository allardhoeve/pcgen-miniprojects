from unittest import TestCase
from django.conf import settings
from unipath import Path

from pcgen.parser import SpellParser
from pcgen import parser


class TestObjectParse(TestCase):

    def setUp(self):
        self.test_spells = Path(settings.DATADIR, "pathfinder/paizo/roleplaying_game/core_rulebook/cr_spells.lst")

    def test_parse_spells_returns_spell_objects(self):
        ret = parser.parse_spells(self.test_spells)
        self.assertIsInstance(ret, list)

    def test_parse_spells_raises_exception_if_file_does_not_exist(self):
        self.assertRaises(IOError, parser.parse_spells, "a")

    def test_parse_spells_returns_list_of_spell_objects(self):
        ret = parser.parse_spells(self.test_spells)
        self.assertTrue(len(ret) > 0)
        self.assertIsInstance(ret[0], SpellParser)

    def test_parse_spells_returns_list(self):
        ret = parser.parse_spells(self.test_spells)
        self.assertTrue(len(ret) > 0)
