from unittest import skip
from pcgen import settings
from pcgen.testcase import TestCase
from prd import get_prd_spell_links


class TestPRD(TestCase):

    def setUp(self):
        with open(settings.DATADIR.child("spells.html")) as fh:
            self.indexcontent = fh.read()

        self.mock_get = self.set_up_patch('requests.get')
        self.mock_get.return_value = self.indexcontent

    def test_get_prd_spell_links_fetches_prd_spell_index(self):
        get_prd_spell_links()
        self.mock_get.assert_called_once_with('http://paizo.com/pathfinderRPG/prd/indices/spells.html')

    def test_get_prd_spell_links_return_contains_absorbing_touch(self):
        spells = get_prd_spell_links()
        self.assertEqual(spells["Absorbing Touch"], "http://paizo.com/pathfinderRPG/prd/advanced/spells/absorbingTouch.html#_absorbing-touch")

    def test_get_prd_spell_links_return_contains_absorbing_touch(self):
        spells = get_prd_spell_links()
        self.assertEqual(spells["Fox's Cunning"], "http://paizo.com/pathfinderRPG/prd/spells/foxSCunning.html#_fox-s-cunning")

    @skip("Not yet implemented")
    def test_get_prd_spells_skips_letter_indices(self):
        pass