import re
from fuzzywuzzy.fuzz import WRatio
from fuzzywuzzy.process import extractOne as match

assert match  # used by QA classes


def SpellRatio(s1, s2, *args, **kwargs):
    """
    Modified fuzzywuzzy.fuzz.WRatio

    If the spell description is a variant of another spell, the standard
    algorithm does not always correctly detect the name.

    Example:
      Beast Shape III (Animals Only) -> Beast Shape I

    We want to optimize the selection by removing the parenthesized string
    if it ends in Only. This denotes a variant spell in all current Pathfinder
    cases.

    Then, let WRatio decide.
    """
    s1 = re.sub("\([^)]+ only\)", "", s1, flags=re.I)
    return WRatio(s1, s2, *args, **kwargs)