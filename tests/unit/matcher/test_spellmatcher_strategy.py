from pcgen import matcher
from pcgen.testcase import TestCase
from prd import CaseInsensitiveDict


class TestSpellFuzzerMatcher(TestCase):

    def setUp(self):
        self.prdspells = CaseInsensitiveDict({
            'Beast Shape I': 1,
            'Beast Shape II': 2,
            'Beast Shape III': 3,
            'Beast Shape IV': 4,
            'Spell, Communal': 5,
            'Spell, Mass': 6,
            'Spell, Lesser': 7,
            'Spell, Greater': 8
        })

        self.suggestions = CaseInsensitiveDict({})

    def assertFuzzerMatchesExactly(self, spell, expected):
        self.assertFuzzerMatches(spell, expected, expectmethod="exact")

    def assertFuzzerMatchesSuggestion(self, spell, expected):
        self.assertFuzzerMatches(spell, expected, expectmethod="suggestion")

    def assertFuzzerMatchesFuzzily(self, spell, expected):
        self.assertFuzzerMatches(spell, expected, expectmethod="fuzzy")

    def assertFuzzerMatches(self, spell, expected, expectmethod=None):
        (candidate, probability, method) = matcher.match_spell(spell, self.prdspells, suggestions=self.suggestions)
        self.assertEqual(candidate, expected)

        if expectmethod is not None:
            self.assertEqual(method, expectmethod)

    ###
    # Tests
    ###

    def test_matcher_is_caseinsensitive(self):
        self.prdspells["Magic Circle Against Good"] = 1
        self.assertFuzzerMatchesExactly("Magic Circle against Good", "Magic Circle against Good")

    def test_beast_shape_III_is_correctly_correctly_matched(self):
        self.assertFuzzerMatchesExactly("Beast Shape III", "Beast Shape III")

    def test_beast_shape_III_animals_only_is_correctly_matched(self):
        self.assertFuzzerMatchesExactly("Beast Shape III (Animals Only)", "Beast Shape III")

    def test_align_weapon_chaos_only_is_correctly_matched(self):
        self.prdspells["Align Weapon"] = 1
        self.assertFuzzerMatchesExactly("Align Weapon (Chaos Only)", "Align Weapon")

    def test_communal_mass_lesser_and_greater_spells_are_matched(self):
        self.assertFuzzerMatchesExactly("Spell (Communal)", "Spell, Communal")
        self.assertFuzzerMatchesExactly("Spell (Mass)", "Spell, Mass")
        self.assertFuzzerMatchesExactly("Spell (Lesser)", "Spell, Lesser")
        self.assertFuzzerMatchesExactly("Spell (Greater)", "Spell, Greater")

    def test_burning_hands_acid_is_fuzzily_matched(self):
        self.prdspells["Burning Hands"] = 1
        self.assertFuzzerMatchesFuzzily("Burning Hands (Acid)", "Burning Hands")

    def test_masterpieces_are_never_matched(self):
        self.prdspells["Mount"] = 1
        self.assertFuzzerMatches("Masterpiece (Depths of the Mountain)", None)

    ###
    # Test loading suggestions
    ###

    def test_matcher_uses_suggestion_when_provided(self):
        self.prdspells["Burning Hands"] = 1  # make sure the suggestion is preferred to the fuzzer
        self.suggestions["Burning Hands (Acid)"] = "Burning Hands"
        self.assertFuzzerMatchesSuggestion("Burning Hands (Acid)", "Burning Hands")
