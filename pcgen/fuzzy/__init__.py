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
     - tuple of (name, certainty, method)
       - name: the name of the SRD spell matched or None
       - certainty: how certain is the match on a scale of 0 - 100
       - method: method used to match:
         - exact -> spell matched names exactly
         - fuzzy -> spell was matched by fuzzer with certainty > 80%
         - miss -> spell was matched by fuzzer, but too uncertain
         - reject -> spells are known not to be in the PRD
    """

    if query.startswith("Masterpiece ("):
        return None, 0, "reject"

    # Strip (Jadda Only) from query name
    query = re.sub("\([^)]+ only\)", "", query, flags=re.I).strip()

    # Replace (Communal), (Lesser), (Greater) and (Mass) by their canonical versions
    query = re.sub(" \((Communal|Mass|Lesser|Greater)\)", r", \1", query, re.I).strip()

    # Try an exact match
    if query in choices:
        return query, 100, "exact"

    (candidate, probability) = extractOne(
        query,
        choices,
        processor=processor,
        scorer=scorer,
        score_cutoff=score_cutoff)

    if (probability < 80):
        return None, 0, "miss"

    return candidate, probability, "fuzzy"