from unittest import TestCase
import os

from pcgen.parser import SpellObject
from pcgen import parser


class TestObjectParse(TestCase):

    def setUp(self):
        cwd = os.path.dirname(os.path.abspath(__file__))
        self.test_spells = cwd + "/../../testdata/pfcr_spells.lst"

    def test_parse_spells_returns_spell_objects(self):
        ret = parser.parse_spells(self.test_spells)
        self.assertIsInstance(ret, list)

    def test_parse_spells_raises_exception_if_file_does_not_exist(self):
        self.assertRaises(IOError, parser.parse_spells, "a")

    def test_parse_spells_returns_list_of_spell_objects(self):
        ret = parser.parse_spells(self.test_spells)
        self.assertTrue(len(ret) > 0)
        self.assertIsInstance(ret[0], SpellObject)

    def test_parse_spells_returns_list(self):
        ret = parser.parse_spells(self.test_spells)
        self.assertTrue(len(ret) > 0)
