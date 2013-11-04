from unipath import Path
from pcgen.campaign import PathfinderCampaign
from pcgen.testcase import TestCase


class TestCampaign(TestCase):

    def setUp(self):
        self.campaign = PathfinderCampaign()

    def test_find_spell_files_returns_tuples_of_lst_file_and_sourcedef(self):
        spellfiletuple = self.campaign.find_spell_listfiles()[0]

        self.assertTrue(spellfiletuple[0].endswith(".lst"))
        self.assertIn("sourcelong", spellfiletuple[1])
        self.assertIn("sourcefile", spellfiletuple[1])

    def test_find_spell_files_finds_all_campaign_components(self):
        spellfiletuples = self.campaign.find_spell_listfiles()
        spellfiles = map(lambda t: t[0], spellfiletuples)

        for path in [
            "pathfinder/core_rulebook/pfcr_spells_domain.lst",
            "pathfinder/core_rulebook/pfcr_spells.lst",
            "pathfinder/core_rulebook/pfcr_spells_mods.lst",
            "pathfinder/ultimate_magic/pfum_spells.lst",
            "pathfinder/ultimate_magic/pfum_spells_domain.lst",
            "pathfinder/ultimate_magic/pfum_spells_mod.lst",
            ]:
            self.assertIn(Path(self.campaign.root, path), spellfiles)