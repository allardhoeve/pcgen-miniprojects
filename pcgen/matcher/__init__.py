import re
from fuzzywuzzy.process import extractOne


# arguments mirror fuzzywuzzy.extractOne
def match_spell(query, choices, processor=None, scorer=None, score_cutoff=0, suggestions=None):
    """
    Case-optimize the fuzzy-matcher.

    The matcher disregards case:
     - Magic Circle against Good -> Magic Circle Against Good

    And it uses canonical Pathfinder names, to instantly find spells:
     - Aid (Mass) -> Aid, Mass
     - Restoration (Lesser) -> Restoration, Lesser
     - Command (Greater) -> Command, Greater
     - Endure Elements (Communal) -> Endure Elements, Communal

    It also tries to match restricted spells to their normal counterparts:
     - Align Weapon (Chaos Only) -> Align Weapon

    Finally, it skips any Masterpieces (they are not on the PRD):
     - Masterpiece (Depths of the Mountain) -> None

    Arguments:
     - arguments are like fuzzywuzzy.process.extractOne
     - notable arguments:
       - query: the name of the spell to find
       - choices: the group to match the name to
       - suggestions: a dict-like that contains any overrides you wish to make
         - key is the spell you are looking for, value is the match
         - e.g. suggestions["Aid (Extended)"] = "Aid"

    Returns:
     - tuple of (name, certainty, method)
       - name: the name of the SRD spell matched or None
       - certainty: how certain is the match on a scale of 0 - 100
       - method: method used to match:
         - exact -> spell matched names exactly
         - fuzzy -> spell was matched by fuzzer with certainty > 80%
         - miss -> spell was matched by fuzzer, but too uncertain
         - reject -> spells are known not to be in the PRD
    """

    if suggestions and query in suggestions:
        return suggestions[query], 100, "suggestion"

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