from pcgen.campaign import PathfinderCampaign
from pcgen.parser import parse_spells


def find_all_pathfinder_spells():
    campaign = PathfinderCampaign()
    spell_listfiles = campaign.find_spell_listfiles()
    spells = []

    for (lst, source) in spell_listfiles:
        spells = spells + parse_spells(lst, source)

    return spells
