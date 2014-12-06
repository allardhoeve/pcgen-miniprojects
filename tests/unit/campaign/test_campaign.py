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
            "roleplaying_game/core_rulebook/cr_spells.lst",
            "roleplaying_game/ultimate_magic/um_spells.lst",
            ]:
            self.assertIn(Path(self.campaign.root, path), files)

    def test_find_feat_files_finds_all_campaign_components(self):
        filetuples = self.campaign.find_feat_listfiles()
        files = map(lambda t: t[0], filetuples)

        for path in [
            "roleplaying_game/core_rulebook/cr_feats.lst",
            "roleplaying_game/ultimate_magic/um_feats.lst",
            "roleplaying_game/ultimate_combat/uc_feats.lst"]:
            self.assertIn(Path(self.campaign.root, path), files)
