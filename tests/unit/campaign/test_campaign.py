from unipath import Path
from pcgen.campaign import PathfinderCampaign
from pcgen.testcase import TestCase


class TestCampaign(TestCase):

    def setUp(self):
        self.campaign = PathfinderCampaign()

    def test_find_spell_files_finds_all_campaign_components(self):
        spellfiles = self.campaign.find_spell_listfiles()

        self.assertEqual(len(spellfiles), 6)

        for path in [
            "core_rulebook/pfcr_spells_domain.lst",
            "core_rulebook/pfcr_spells.lst",
            "core_rulebook/pfcr_spells_mods.lst",
            "ultimate_magic/pfum_spells.lst",
            "ultimate_magic/pfum_spells_domain.lst",
            "ultimate_magic/pfum_spells_mod.lst",
            ]:
            self.assertIn(Path(self.campaign.root, path), spellfiles)