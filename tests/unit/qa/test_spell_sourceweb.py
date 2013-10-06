from pcgen.parser import SpellObject
from pcgen.qa import QASpellSourceWeb
from pcgen.testcase import TestCase


class TestSpellSourceWeb(TestCase):

    def setUp(self):
        self.spells = [
            SpellObject("Acid Splash"),
            SpellObject("Acid Dart\t\tSOURCEWEB:invalidlink"),
            SpellObject("Magic Missile\t\tSOURCEWEB:http://example.com/example"),
            SpellObject("Fireball\t\tSOURCEWEB:http://example.com/example")]

    def test_spellsourceweb_test_returns_tuples_of_wrong_spells(self):
        sourceweb = QASpellSourceWeb()
        result = sourceweb.test(self.spells)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], (self.spells[0], "Missing SOURCEWEB"))
        self.assertEqual(result[1], (self.spells[1], "URL is not a valid HTTP link"))