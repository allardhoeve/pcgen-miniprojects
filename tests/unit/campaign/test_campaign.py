from unipath import Path
from pcgen.campaign import PathfinderCampaign
from pcgen.testcase import TestCase


class TestCampaign(TestCase):

    def setUp(self):
        self.campaign = PathfinderCampaign()

    def test_find_pcc_files_finds_all_campaign_components(self):
        spells = self.campaign.find_spell_files(self.campaign.pcc)

        self.assertEqual(len(spells), 6)

        for path in [
            "core_rulebook/pfcr_spells_domain.lst",
            "core_rulebook/pfcr_spells.lst",
            "core_rulebook/pfcr_spells_mods.lst",
            "ultimate_magic/pfum_spells.lst",
            "ultimate_magic/pfum_spells_domain.lst",
            "ultimate_magic/pfum_spells_mod.lst",
            ]:
            self.assertIn(Path(self.campaign.root, path), spells)

    def notest_find_spell_list_files_finds_all_spells_in_campaign_pcc_recursively(self):
        campaign = PathfinderCampaign()
        spells = campaign.find_spell_list_files()

        self.assertIn(spells, "core_rulebook/pfcr_spells.lst")