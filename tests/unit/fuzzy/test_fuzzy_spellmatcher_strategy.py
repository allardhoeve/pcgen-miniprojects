from pcgen import fuzzy
from pcgen.testcase import TestCase
from prd import get_prd_spell_links


class TestSpellFuzzerMatcher(TestCase):

    def setUp(self):
        self.prdspells = [
            'Beast Shape I',
            'Beast Shape II',
            'Beast Shape III',
            'Beast Shape IV',
            'Spell, Communal',
            'Spell, Mass',
            'Spell, Lesser',
            'Spell, Greater',
        ]

    def assertFuzzerMatchesExactly(self, spell, expected):
        self.assertFuzzerMatches(spell, expected, expectmethod="exact")

    def assertFuzzerMatchesFuzzily(self, spell, expected):
        self.assertFuzzerMatches(spell, expected, expectmethod="fuzzy")

    def assertFuzzerMatches(self, spell, expected, expectmethod=None):
        (candidate, probability, method) = fuzzy.match_spell(spell, self.prdspells)
        self.assertEqual(candidate, expected)

        if not expectmethod is None:
            self.assertEqual(method, expectmethod)

    ###
    # Tests
    ###

    def test_beast_shape_III_is_correctly_correctly_matched(self):
        self.assertFuzzerMatchesExactly("Beast Shape III", "Beast Shape III")

    def test_beast_shape_III_animals_only_is_correctly_matched(self):
        self.assertFuzzerMatchesExactly("Beast Shape III (Animals Only)", "Beast Shape III")

    def test_align_weapon_chaos_only_is_correctly_matched(self):
        self.prdspells.append("Align Weapon")
        self.assertFuzzerMatchesExactly("Align Weapon (Chaos Only)", "Align Weapon")

    def test_communal_mass_lesser_and_greater_spells_are_matched(self):
        self.assertFuzzerMatchesExactly("Spell (Communal)", "Spell, Communal")
        self.assertFuzzerMatchesExactly("Spell (Mass)", "Spell, Mass")
        self.assertFuzzerMatchesExactly("Spell (Lesser)", "Spell, Lesser")
        self.assertFuzzerMatchesExactly("Spell (Greater)", "Spell, Greater")

    def test_burning_hands_acid_is_fuzzily_matched(self):
        self.prdspells.append("Burning Hands")
        self.assertFuzzerMatchesFuzzily("Burning Hands (Acid)", "Burning Hands")

    def test_masterpieces_are_never_matched(self):
        self.prdspells.append("Mount")
        self.assertFuzzerMatches("Masterpiece (Depths of the Mountain)", None)