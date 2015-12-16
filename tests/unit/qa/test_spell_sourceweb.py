from pcgen.parser import SpellParser
from pcgen.qa import QASourceLink
from pcgenminiprojects.testcase import TestCase


class TestSpellSOURCELINK(TestCase):

    def setUp(self):
        self.sourcelink = QASourceLink()

        self.spells = [
            SpellParser("Acid Splash\r"),  # NB: test removal of carriage return
            SpellParser("Acid Dart\t\tSOURCELINK:invalidlink\t\tDESC:Henk"),
            SpellParser("Magic Missile\t\tSOURCELINK:http://example.com/example"),
            SpellParser("Fireball\t\tSOURCELINK:http://example.com/example"),
        ]

        self.srdspells = {
            "Acid Splash": "http://pcgen.nl/acidsplash.html",
            "Acid Dart": "http://pcgen.nl/aciddart.html",
            "Magic Missile": "http://pcgen.nl/magicmissile.html",
            "Fireball": "http://pcgen.nl/fireball.html",
            "Endure Elements, Communal": "http://pcgen.nl/endure.html"
        }

        self.suggestions = {
            "links": {},
            "matcher": {}
        }

    def test_spellsourcelink_test_returns_tuples_of_wrong_spells(self):
        result = self.sourcelink.test(self.spells)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], (self.spells[0], "Missing SOURCELINK"))
        self.assertEqual(result[1], (self.spells[1], "URL is not a valid HTTP link"))

    def test_correct_adds_sourcelink_entry(self):
        spell = self.spells[0]
        result = self.sourcelink.correct(spell, self.srdspells)

        self.assertTrue(result)
        self.assertEqual(result["method"], "exact")
        self.assertEqual(result["lst"], "add")
        self.assertEqual(result["match"], "Acid Splash")
        self.assertEqual(result["certainty"], 100)
        self.assertEqual(spell.sourcelink, "http://pcgen.nl/acidsplash.html")
        self.assertEqual(spell.lstline, "Acid Splash\t\tSOURCELINK:http://pcgen.nl/acidsplash.html")

    def test_correct_fixes_invalid_sourcelink(self):
        spell = self.spells[1]
        result = self.sourcelink.correct(spell, self.srdspells)

        self.assertTrue(result)
        self.assertEqual(result["method"], "exact")
        self.assertEqual(result["lst"], "correct")
        self.assertEqual(spell.sourcelink, "http://pcgen.nl/aciddart.html")
        self.assertEqual(spell.lstline, "Acid Dart\t\tSOURCELINK:http://pcgen.nl/aciddart.html\t\tDESC:Henk")

    def test_correct_declines_fixing_valid_sourcelink(self):
        spell = self.spells[2]
        origsourcelink = spell.sourcelink
        origlstline = spell.lstline
        result = self.sourcelink.correct(spell, self.srdspells)

        self.assertFalse(result)
        self.assertEqual(spell.sourcelink, origsourcelink)
        self.assertEqual(spell.lstline, origlstline)

    def test_correct_fuzzymatches_spells_if_spell_misspelled(self):
        spell = SpellParser("Acid Dard")
        result = self.sourcelink.correct(spell, self.srdspells)

        self.assertTrue(result)
        self.assertEqual(result["method"], "fuzzy")
        self.assertEqual(spell.sourcelink, "http://pcgen.nl/aciddart.html")

    def test_correct_only_uses_fuzzymatch_if_probable_match(self):
        spell = SpellParser("Acid Ball")
        result = self.sourcelink.correct(spell, self.srdspells)

        self.assertFalse(result)
        self.assertEqual(spell.sourcelink, None)

    ###
    # Pass suggestions to the correcter
    ###

    def test_correct_takes_suggestions_and_passes_them_on_to_spell_matcher(self):
        # the spell Burning Hands (Acid) must be corrected to
        spell = SpellParser("Burning Hands (Acid)")
        self.srdspells["Burning Hands"] = "http://pcgen.nl/burning_hands.html"
        self.suggestions["matcher"]["Burning Hands (Acid)"] = "Burning Hands"

        result = self.sourcelink.correct(spell, self.srdspells, suggestions=self.suggestions)

        self.assertTrue(result)
        self.assertEqual(result["method"], "suggestion")
        self.assertEqual(result["match"], "Burning Hands")
        self.assertEqual(spell.sourcelink, "http://pcgen.nl/burning_hands.html")

    def test_correct_uses_suggestions_as_override_for_spells(self):
        spell = SpellParser("Burnsing Handses")
        self.suggestions["links"]["Burnsing Handses"] = "http://pcgen.nl/burnsing_handses.html"

        result = self.sourcelink.correct(spell, self.srdspells, suggestions=self.suggestions)

        self.assertTrue(result)
        self.assertEqual(result["method"], "suggestion")
        self.assertEqual(result["match"], "Burnsing Handses")
        self.assertEqual(spell.sourcelink, "http://pcgen.nl/burnsing_handses.html")
