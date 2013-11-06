from unipath import Path
from pcgen.campaign import PathfinderCampaign
from pcgen.testcase import TestCase


class TestCampaign(TestCase):

    maxDiff = None

    def setUp(self):
        self.campaign = PathfinderCampaign()

    def test_find_spell_files_finds_all_campaign_components(self):
        filetuples = self.campaign.find_spell_listfiles()
        files = map(lambda t: t[0], filetuples)

        for path in [
            "pathfinder/core_rulebook/pfcr_spells_domain.lst",
            "pathfinder/core_rulebook/pfcr_spells.lst",
            "pathfinder/core_rulebook/pfcr_spells_mods.lst",
            "pathfinder/ultimate_magic/pfum_spells.lst",
            "pathfinder/ultimate_magic/pfum_spells_domain.lst",
            "pathfinder/ultimate_magic/pfum_spells_mod.lst",
            ]:
            self.assertIn(Path(self.campaign.root, path), files)

    def test_find_feat_files_finds_all_campaign_components(self):
        filetuples = self.campaign.find_feat_listfiles()
        files = map(lambda t: t[0], filetuples)

        for path in [
            "pathfinder/core_rulebook/pfcr_feats.lst",
            "pathfinder/ultimate_magic/pfum_feats.lst",
            "pathfinder/ultimate_combat/pfuc_feats.lst"]:
            self.assertIn(Path(self.campaign.root, path), files)