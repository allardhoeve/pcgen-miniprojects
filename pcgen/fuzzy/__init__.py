import re
from fuzzywuzzy.fuzz import WRatio
from fuzzywuzzy.process import extractOne


def match_spell(query, choices, processor=None, scorer=None, score_cutoff=0):
    """
    Case-optimize the fuzzy-matcher.

    Use canonical Pathfinder names, to instantly find spells:
     - Aid (Mass) -> Aid, Mass
     - Restoration (Lesser) -> Restoration, Lesser
     - Command (Greater) -> Command, Greater
     - Endure Elements (Communal) -> Endure Elements, Communal

    Also try to match restricted spells to their normal counterparts:
     - Align Weapon (Chaos Only) -> Align Weapon

    Finally, skip any Masterpieces (they are not on the PRD):
     - Masterpiece (Depths of the Mountain) -> None

    arguments:
     - arguments are like fuzzywuzzy.process.extractOne
     - notable arguments:
       - query: the name of the spell to find
       - choices: the group to match the name to

    returns:
     - tuple of (matchedname, certainty)
    """

    # Strip (Jadda Only) from query name
    query = re.sub("\([^)]+ only\)", "", query, flags=re.I)

    return extractOne(
        query,
        choices,
        processor=processor,
        scorer=scorer,
        score_cutoff=score_cutoff)