from pcgen import PathfinderCampaign
from pcgenminiprojects.testcase import TestCase


class TestParseAllFeats(TestCase):

    def test_parse_all_feats(self):
        campaign = PathfinderCampaign()
        feats = campaign.fetch_all_feats()

        for feats in feats:
            self.assertIsNotNone(feats.sourcelong, "SOURCELONG for %s is None" % feats)
