from unittest import skip
from pcgen import settings
from pcgen.testcase import TestCase
from prd import get_prd_feat_links


class TestPRD(TestCase):

    def setUp(self):
        with open(settings.PROJECTROOT.child("feats.html")) as fh:
            self.indexcontent = fh.read()

        self.mock_get = self.set_up_patch('requests.get')
        self.mock_get.return_value = self.indexcontent

    def test_get_prd_spell_links_fetches_prd_spell_index(self):
        get_prd_feat_links()
        self.mock_get.assert_called_once_with('http://paizo.com/pathfinderRPG/prd/indices/feats.html')

    def test_get_prd_spell_links_return_contains_iron_will(self):
        spells = get_prd_feat_links()
        self.assertEqual(spells["Iron Will"], "http://paizo.com/pathfinderRPG/prd/feats.html#iron-will")

    def test_get_prd_spell_links_finds_adjuring_step(self):
        spells = get_prd_feat_links()
        self.assertIn("Twin Thunders", spells)
        self.assertEqual(spells["Twin Thunders"], "http://paizo.com/pathfinderRPG/prd/ultimateCombat/ultimateCombatFeats.html#twin-thunders")

    def test_get_prd_spell_links_is_caseinsensitive(self):
        spells = get_prd_feat_links()
        self.assertIn("Iron Will", spells)
        self.assertIn("iron will", spells)
        self.assertIn("iRon WilL", spells)

    def test_get_prd_spells_skips_letter_indices(self):
        spells = get_prd_feat_links()
        self.assertNotIn("A Feats", spells)
