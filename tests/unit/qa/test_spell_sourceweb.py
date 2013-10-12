from pcgen.parser import SpellObject
from pcgen.qa import QASpellSourceWeb
from pcgen.testcase import TestCase


class TestSpellSourceWeb(TestCase):

    def setUp(self):
        self.sourceweb = QASpellSourceWeb()

        self.spells = [
            SpellObject("Acid Splash"),
            SpellObject("Acid Dart\t\tSOURCEWEB:invalidlink\t\tDESC:Henk"),
            SpellObject("Magic Missile\t\tSOURCEWEB:http://example.com/example"),
            SpellObject("Fireball\t\tSOURCEWEB:http://example.com/example")]

        self.srdspells = {
            "Acid Splash": "http://pcgen.nl/acidsplash.html",
            "Acid Dart": "http://pcgen.nl/aciddart.html",
            "Magic Missile": "http://pcgen.nl/magicmissile.html",
            "Fireball": "http://pcgen.nl/fireball.html"
        }

    def test_correct_adds_sourceweb_entry(self):
        spell = self.spells[0]
        result = self.sourceweb.correct(spell, self.srdspells)

        self.assertEqual(result, True)
        self.assertEqual(spell.sourceweb, "http://pcgen.nl/acidsplash.html")
        self.assertEqual(spell.lstline, "Acid Splash\t\tSOURCEWEB:http://pcgen.nl/acidsplash.html")

    def test_correct_fixes_invalid_sourceweb(self):
        spell = self.spells[1]
        result = self.sourceweb.correct(spell, self.srdspells)

        self.assertEqual(result, True)
        self.assertEqual(spell.sourceweb, "http://pcgen.nl/aciddart.html")
        self.assertEqual(spell.lstline, "Acid Dart\t\tSOURCEWEB:http://pcgen.nl/aciddart.html\t\tDESC:Henk")

    def test_correct_declines_fixing_valid_sourceweb(self):
        spell = self.spells[2]
        origsourceweb = spell.sourceweb
        origlstline = spell.lstline
        result = self.sourceweb.correct(spell, self.srdspells)

        self.assertEqual(result, False)
        self.assertEqual(spell.sourceweb, origsourceweb)
        self.assertEqual(spell.lstline, origlstline)

    def test_spellsourceweb_test_returns_tuples_of_wrong_spells(self):
        result = self.sourceweb.test(self.spells)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], (self.spells[0], "Missing SOURCEWEB"))
        self.assertEqual(result[1], (self.spells[1], "URL is not a valid HTTP link"))