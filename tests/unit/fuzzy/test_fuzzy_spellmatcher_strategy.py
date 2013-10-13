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
            'Magic Vestment',
            'Shield',
        ]

    def assertFuzzerMatches(self, spell, expected):
        (candidate, probability) = fuzzy.match_spell(spell, self.prdspells)
        self.assertEqual(candidate, expected)

    def test_beast_shape_III_is_correctly_detected(self):
        self.assertFuzzerMatches("Beast Shape III", "Beast Shape III")

    def test_beast_shape_III_animals_only_is_correctly_detected(self):
        self.assertFuzzerMatches("Beast Shape III (Animals Only)", "Beast Shape III")

    def notest_magic_vestment_shield_use_is_correctly_detected(self):
        with open("testdata/spells.html") as fh:
            html = fh.read()
            self.prdspells = get_prd_spell_links(html)